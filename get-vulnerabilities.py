import xml.etree.ElementTree as ET
import requests
import csv
from datetime import datetime
import os
import time
import json
import html

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    products = []
    for product in root.findall('product'):
        name = product.find('name').text
        vendor = product.find('vendor').text
        products.append((name, vendor))
    return products

def query_api(product, vendor, exploited=None):
    base_url = "https://euvdservices.enisa.europa.eu/api/vulnerabilities"
    params = {
        "product": product,
        "vendor": vendor,
        "size": 100
    }
    if exploited is not None:
        params["exploited"] = str(exploited).lower()
    
    headers = {
        "User-Agent": "VulnerabilityQueryScript/1.0"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            print(f"Received data for {product} from {vendor}:")
            print(json.dumps(data, indent=2)[:500])  # Print first 500 characters of formatted JSON
            return data
        except json.JSONDecodeError:
            print(f"Error decoding JSON for {product} from {vendor}")
            print(f"Response content: {response.text[:200]}...")
            return None
    else:
        print(f"Error querying API for {product} from {vendor}: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        return None

def save_to_csv(data, filename):
    if not data:
        print(f"No data to save to {filename}")
        return

    # Collect all possible fields
    all_fields = set()
    for row in data:
        all_fields.update(row.keys())
    
    fieldnames = list(all_fields)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Ensure all values are strings and replace None with empty string
            cleaned_row = {k: str(v) if v is not None else '' for k, v in row.items()}
            # Add empty strings for missing fields
            for field in fieldnames:
                if field not in cleaned_row:
                    cleaned_row[field] = ''
            writer.writerow(cleaned_row)
    print(f"CSV data saved to {filename}")

def save_to_html(data, filename):
    if not data:
        print(f"No data to save to {filename}")
        return

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vulnerability Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; word-wrap: break-word; max-width: 300px; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            tr:hover { background-color: #f5f5f5; }
            .score-green { background-color: #90EE90; }
            .score-orange { background-color: #FFA500; }
            .score-red { background-color: #FF6347; }
            .score-darkred { background-color: #8B0000; color: white; }
        </style>
    </head>
    <body>
        <h1>Vulnerability Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Product</th>
    """
    
    # Add header, excluding 'enisaIdProduct' and 'enisaIdVendor'
    for key in data[0].keys():
        if key not in ['enisaIdProduct', 'enisaIdVendor']:
            html_content += f"<th>{html.escape(key)}</th>"
    
    html_content += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Add data rows, including product information
    for row in data:
        html_content += "<tr>"
        
        # Add product information
        products = row.get('enisaIdProduct', [])
        product_names = ', '.join(p['product']['name'] for p in products if 'product' in p and 'name' in p['product'])
        html_content += f"<td>{html.escape(product_names)}</td>"
        
        for key, value in row.items():
            if key not in ['enisaIdProduct', 'enisaIdVendor']:
                if key == 'baseScore':
                    score = float(value)
                    if 0.0 <= score <= 3.9:
                        color_class = 'score-green'
                    elif 4.0 <= score <= 6.9:
                        color_class = 'score-orange'
                    elif 7.0 <= score <= 8.9:
                        color_class = 'score-red'
                    else:
                        color_class = 'score-darkred'
                    html_content += f'<td class="{color_class}">{html.escape(str(value))}</td>'
                else:
                    html_content += f"<td>{html.escape(str(value))}</td>"
        html_content += "</tr>"
    
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(html_content)
    print(f"HTML data saved to {filename}")
def main():
    xml_file = "products.xml"
    products = parse_xml(xml_file)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    for exploited in [True, False]:
        all_results = []
        for product, vendor in products:
            results = query_api(product, vendor, exploited)
            if results:
                if isinstance(results, dict) and 'items' in results:
                    # Add product and vendor information to each item
                    for item in results['items']:
                        item['queried_product'] = product
                        item['queried_vendor'] = vendor
                    all_results.extend(results['items'])
                elif isinstance(results, list):
                    # Add product and vendor information to each item
                    for item in results:
                        item['queried_product'] = product
                        item['queried_vendor'] = vendor
                    all_results.extend(results)
                else:
                    print(f"Unexpected data structure for {product} {vendor}:")
                    print(json.dumps(results, indent=2)[:500])
            time.sleep(1)  # Wacht 1 seconde tussen requests
        
        if all_results:
            exploited_str = "exploited" if exploited else "not_exploited"
            csv_filename = os.path.join(output_dir, f"vulnerabilities_{exploited_str}.csv")
            html_filename = os.path.join(output_dir, f"vulnerabilities_{exploited_str}.html")
            
            save_to_csv(all_results, csv_filename)
            save_to_html(all_results, html_filename)
            print(f"Results saved to {csv_filename} and {html_filename}")
        else:
            print(f"No results found for {'exploited' if exploited else 'not exploited'} vulnerabilities")

if __name__ == "__main__":
    main()