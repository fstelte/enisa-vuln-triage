# ENISA Vulnerability Query Tool

This Python script is designed to query the ENISA (European Union Agency for Cybersecurity) vulnerability database for specific products and vendors. It generates reports in both CSV and HTML formats, providing a comprehensive overview of vulnerabilities, including their exploitation status and severity scores.

## Purpose

The main objectives of this script are:
1. To fetch vulnerability data from the ENISA API for specified products and vendors.
2. To generate detailed reports of vulnerabilities, both exploited and non-exploited.
3. Specify date ranges for vulnerability queries
4. To provide an easy-to-read HTML report with color-coded severity scores.
5. To offer a CSV export for further data analysis.

## Setup

### Creating a Virtual Environment

It's recommended to use a virtual environment for running this script. Here's how you can set it up:

1. Open a terminal and navigate to the project directory.
2. Create a virtual environment:
``` bash
python -m venv venv

```
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

### Installing Dependencies

After activating the virtual environment, install the required packages:
``` bash
pip install -r requirements.txt
```
This will install all necessary dependencies listed in the `requirements.txt` file.

### Configuring the products.xml File
The products.xml file is used to specify which products and vendors you want to query. Here's how to structure and fill this file:
1.  Open the products.xml file in a text editor.
2. Use the following format to add products and vendors:
``` xml 
<?xml version="1.0" encoding="UTF-8"?>
<products>
    <product>
        <name>Product Name</name>
        <vendor>Vendor Name</vendor>
        <end_date>2025-01-01</end_date>
        <start_date>2023-01-01</start_date>
    </product>
    <!-- Add more product entries as needed -->
</products>
```
3. For each product you want to query, add a new <product> element with nested <name> and <vendor> elements.
4. The <name> should contain the product name, and <vendor> should contain the vendor name.
5. You can add as many <product> elements as needed.
#### Example
``` xml
<?xml version="1.0" encoding="UTF-8"?>
<products>
    <product>
        <name>Windows</name>
        <vendor>Microsoft</vendor>
        <start_date>2023-01-01</start_date>
        <end_date>2023-12-31</end_date>
    </product>
    <product>
        <name>iOS</name>
        <vendor>Apple</vendor>
        <start_date>2023-06-01</start_date>
    </product>
    <product>
        <name>Android</name>
        <vendor>Google</vendor>
        <end_date>2023-05-31</end_date>
    </product>
</products>
```
## Running the Script

To run the script:

1. Ensure your virtual environment is activated.
2. Make sure your `products.xml` file is up to date with the products and vendors you want to query.
3. Run the script using:
``` bash
python get-vulnerabilities.py
```
4. The script will create a new directory with the current timestamp, containing the CSV and HTML reports for both exploited and non-exploited vulnerabilities.

## Output

The script generates four files in the output directory:
- `vulnerabilities_exploited.csv`
- `vulnerabilities_exploited.html`
- `vulnerabilities_not_exploited.csv`
- `vulnerabilities_not_exploited.html`

The HTML reports include color-coded severity scores for easy identification of high-risk vulnerabilities.

## Date Range Functionality
- If no dates are specified for a product, all vulnerabilities will be retrieved.
- If only a start date is specified, vulnerabilities from that date to the current date will be retrieved.
- If only an end date is specified, all vulnerabilities up to that date will be retrieved.
- If both start and end dates are specified, vulnerabilities within that range will be retrieved.

## Note

Ensure you have proper authorization to access the ENISA API before running this script.