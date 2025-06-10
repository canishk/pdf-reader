import pdfplumber
import csv
import re

def extract_data(pdf_path='Brand Summary.pdf', csv_out='weekly_sales_summary.csv'):
    output_rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            date_match = re.search(r'STORE SUMMARY\s+(\d{1,2}/\d{1,2}/\d{4})', text, re.IGNORECASE)
            if date_match:
                store_summary_date = date_match.group(1)
                print(f"Store Summary Date: {store_summary_date}")
            
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        print(f"Processing row: {row}")
                        # Skip empty rows or rows with insufficient data
                        if not row or len(row) < 4:
                            continue
                        region, district, store, sales = row[0], row[1], row[2], row[3]
                        sales_clean = sales.replace("$", "").replace(",", "").strip()
                        if sales_clean.replace('.', '', 1).isdigit():
                            output_rows.append([store_summary_date, region, district, store, sales_clean])
            return write_to_csv(output_rows, csv_out)
    
    def write_to_csv(rows, csv_out):
        with open(csv_out, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Store Summary Date', 'Region', 'District', 'Store', 'Sales'])
            for row in rows:
                writer.writerow(row)
        print(f"Data written to {csv_out}")
        return csv_out

if __name__ == "__main__":
    extract_data()