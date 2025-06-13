import pdfplumber
import pytesseract
import pandas as pd
from PIL import Image
import io
from concurrent.futures import ProcessPoolExecutor, as_completed


pdf_path = "data/0001-0250.pdf"

# Required keywords (case-insensitive match)
# required_keywords1 = ["Symbol", "Parts Name", "Material", "Q'ty", "Parts No"]
# required_keywords2 = ["Designed", "Checked", "Approved", "Dqg. No.", "Parts No.", "Quantity", "Description", "Material", "Dimension", "Remarks"]

# Helper to extract text from a page image using OCR
def ocr_page(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        img = page.to_image(resolution=300)
        pil_img = img.original
        text = pytesseract.image_to_string(pil_img)
        return text, page_number + 1

# Extract OCR text from relevant pages only
def extract_ocr_from_pdf(pdf_path):
    # Required keywords (case-insensitive match)
    required_keywords1 = ["Symbol", "Parts Name", "Material", "Q'ty", "Parts No"]
    ocr_texts1 = {}
    ocr_texts2 = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(ocr_page, pdf_path, i) for i in range(num_pages)]
        
        for future in as_completed(futures):
            text, page_num = future.result()
            print(f"Processing Page {page_num}/{num_pages+1}")
            if all(keyword.lower() in text.lower() for keyword in required_keywords1):
                ocr_texts1[str(page_num)] = text
    return ocr_texts1


# # Usage
# ocr_results = extract_ocr_from_pdf(pdf_path)

# # Optional: Print example output
# print(ocr_results["116"]) 
