"""
Duluth Tourism PDF Data Extraction Script
Author: Nick Christopherson
Date: 2025

This script extracts tourism data from Minnesota Department of Revenue 
Annual Sales Tax PDFs for St. Louis County (Duluth area).
"""

import pandas as pd
import numpy as np
import pdfplumber
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')


class TourismDataExtractor:
    """Extract tourism data from Minnesota Department of Revenue PDFs."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the extractor."""
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "raw")
        self.processed_dir = os.path.join(data_dir, "processed")
        
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        print("🚀 Tourism Data Extractor initialized")
    
    def extract_number(self, text: str) -> Optional[float]:
        """Extract numeric value from text string."""
        if not text:
            return None
        
        text = str(text).replace(',', '').replace('$', '').replace('%', '')
        match = re.search(r'[\d,]+\.?\d*', text)
        if match:
            try:
                return float(match.group().replace(',', ''))
            except:
                return None
        return None
    
    def extract_tourism_data_from_pdf(self, pdf_path: str, year: int) -> Dict:
        """Extract tourism data from a single PDF file."""
        tourism_data = {
            'year': year,
            'county': 'St. Louis',
            'accommodation_establishments': None,
            'accommodation_gross_sales': None,
            'food_service_establishments': None,
            'food_service_gross_sales': None,
            'recreation_establishments': None,
            'recreation_gross_sales': None,
            'museums_establishments': None,
            'museums_gross_sales': None,
            'total_leisure_hospitality_establishments': None,
            'total_leisure_hospitality_gross_sales': None,
            'total_leisure_hospitality_tax': None,
            'data_found': False
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                print(f"📄 Processing {os.path.basename(pdf_path)} - {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    
                    if text and ('st. louis county' in text.lower() or 'st. louis' in text.lower()):
                        
                        tables = page.extract_tables()
                        
                        for table in tables:
                            if table and len(table) > 1:
                                if table[0] and any(cell and 'st. louis county' in str(cell).lower() for cell in table[0]):
                                    print(f"🎯 Found St. Louis County table on page {page_num + 1}")
                                    tourism_data['data_found'] = True
                                    
                                    for i, row in enumerate(table[2:], start=2):
                                        if row and row[0]:
                                            industry = str(row[0]).strip().lower()
                                            
                                            if '721 accommodation' in industry:
                                                tourism_data['accommodation_establishments'] = self.extract_number(row[1])
                                                tourism_data['accommodation_gross_sales'] = self.extract_number(row[2])
                                            
                                            elif '722 food services' in industry:
                                                tourism_data['food_service_establishments'] = self.extract_number(row[1])
                                                tourism_data['food_service_gross_sales'] = self.extract_number(row[2])
                                            
                                            elif '713 amusement' in industry:
                                                tourism_data['recreation_establishments'] = self.extract_number(row[1])
                                                tourism_data['recreation_gross_sales'] = self.extract_number(row[2])
                                            
                                            elif '712 museums' in industry:
                                                tourism_data['museums_establishments'] = self.extract_number(row[1])
                                                tourism_data['museums_gross_sales'] = self.extract_number(row[2])
                                            
                                            elif 'leisure and hospitality total' in industry:
                                                tourism_data['total_leisure_hospitality_establishments'] = self.extract_number(row[1])
                                                tourism_data['total_leisure_hospitality_gross_sales'] = self.extract_number(row[2])
                                                tourism_data['total_leisure_hospitality_tax'] = self.extract_number(row[5])
                                    
                                    return tourism_data
                        
        except Exception as e:
            print(f"❌ Error processing {pdf_path}: {str(e)}")
        
        return tourism_data
    
    def process_all_pdfs(self) -> pd.DataFrame:
        """Process all PDF files in the raw directory."""
        extracted_data = []
        
        pdf_files = [f for f in os.listdir(self.raw_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"📁 No PDF files found in {self.raw_dir}")
            return pd.DataFrame()
        
        print(f"🚀 PROCESSING {len(pdf_files)} PDFs")
        
        for pdf_file in pdf_files:
            year = None
            for y in [2019, 2020, 2021, 2022, 2023, 2024]:
                if str(y) in pdf_file:
                    year = y
                    break
            
            if year:
                pdf_path = os.path.join(self.raw_dir, pdf_file)
                print(f"\n📅 PROCESSING {year}: {pdf_file}")
                data = self.extract_tourism_data_from_pdf(pdf_path, year)
                extracted_data.append(data)
        
        df = pd.DataFrame(extracted_data)
        
        if not df.empty:
            df = df.sort_values('year')
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str = "duluth_tourism_complete.csv") -> str:
        """Save the extracted data to CSV."""
        output_path = os.path.join(self.processed_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"\n💾 Data saved to: {output_path}")
        return output_path


def main():
    """Main execution function."""
    print("🏔️  DULUTH TOURISM DATA EXTRACTION")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    extractor = TourismDataExtractor()
    tourism_df = extractor.process_all_pdfs()
    
    if not tourism_df.empty:
        output_file = extractor.save_data(tourism_df)
        print(f"\n🎯 SUCCESS! Tourism data extracted and saved.")
    else:
        print(f"\n❌ No data extracted. Check your PDF files.")


if __name__ == "__main__":
    main()
