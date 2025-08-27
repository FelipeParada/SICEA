import pdfplumber
from pathlib import Path
import pandas as pd
import re
from datetime import datetime


class AguasAndinasReader:
    def __init__(self):
        self.all_data = []

    @staticmethod
    def extract_info_from_text(text: str, file_pdf: str) -> dict:
        """
        Extract relevant information from PDF text
        """
        data_tmp = {'file': file_pdf}

        # Extract Total amount to pay
        total_match = re.search(r'TOTAL A PAGAR\s*\$\s*([\d.,]+)', text)
        if total_match:
            data_tmp['total_amount'] = total_match.group(1).replace('.', '')

        # Extract Account number
        account_match = re.search(r'Nro de cuenta\s*(\d+-\d+)', text)
        if not account_match:
            account_match = re.search(r'(\d{6}-\d)', text)
        if account_match:
            data_tmp['account_number'] = account_match.group(1)

        # Extract month and year from emission or due date
        date_match = re.search(r'FECHA EMISIÓN:(\d{2}-[A-Z]{3}-\d{4})', text)
        if not date_match:
            date_match = re.search(r'VENCIMIENTO\s*(\d{2}-[A-Z]{3}-\d{4})', text)

        if date_match:
            date_str = date_match.group(1)
            try:
                # Convert date (e.g., "11-FEB-2025") to datetime object
                date = datetime.strptime(date_str, '%d-%b-%Y')
                data_tmp['month'] = date.strftime('%B')  # Full month name
                data_tmp['year'] = date.year
                data_tmp['month_year'] = date.strftime('%m-%Y')  # MM-YYYY format
            except ValueError:
                data_tmp['month_year'] = date_str

        return data_tmp

    def process_bill(self, file_pdf: str) -> dict:
        """
        Process a PDF bill from Aguas Andinas and extract relevant information.
        """
        print(f"Processing bill: {file_pdf}")

        try:
            with pdfplumber.open(file_pdf) as pdf:
                complete_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        complete_text += text + "\n"

            # Extract specific information
            extracted_data = self.extract_info_from_text(complete_text, file_pdf)
            extracted_data['complete_text'] = complete_text

            # Add to the list of all processed bills
            self.all_data.append(extracted_data)

            return extracted_data

        except Exception as e:
            print(f"Error processing bill {file_pdf}: {e}")
            return {}

    def export_to_excel(self, output_filename: str = "aguas_andinas_bills.xlsx"):
        """
        Export all processed data to an Excel file
        """
        if not self.all_data:
            print("No data to export")
            return False

        try:
            # Create output directory if it doesn't exist
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)

            # Create DataFrame
            df = pd.DataFrame(self.all_data)

            # Select and order relevant columns
            columns_to_export = ['file', 'account_number', 'total_amount', 'month', 'year', 'month_year']
            # Keep only columns that exist in the data
            available_columns = [col for col in columns_to_export if col in df.columns]

            df_export = df[available_columns]

            # Save to Excel
            output_path = output_dir / output_filename
            df_export.to_excel(output_path, index=False)

            print(f"Data successfully exported to: {output_path}")
            return True

        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False

    def process_multiple_bills(self, pdf_files: list):
        """
        Process multiple PDF files
        """
        for pdf_file in pdf_files:
            self.process_bill(pdf_file)

    def clear_data(self):
        """
        Clear all stored data
        """
        self.all_data = []
        print("All data cleared")


class EnelReader:
    def __init__(self):
        self.data = {}

    def process_bill(self, file_pdf: str) -> dict:
        """
        Process a PDF bill from Enel and extract relevant information.
        """
        print(f"Processing bill: {file_pdf}")

        try:
            with pdfplumber.open(file_pdf) as pdf:
                complete_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        complete_text += text + "\n"
            self.data['complete_text'] = complete_text

            return self.data

        except Exception as e:
            print(f"Error processing bill: {e}")
            return {}


water_path = Path("./input/water_bills")

water_pdfs = [file for file in water_path.iterdir() if file.is_file()]

reader = AguasAndinasReader()
reader.process_multiple_bills(water_pdfs)
reader.export_to_excel()
print(f"Processed {len(reader.all_data)} bills")