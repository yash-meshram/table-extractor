import pdfplumber
import pytesseract
import pandas as pd
from PIL import Image
import io

pdf_path = "data/0001-0250.pdf"

# Required keywords (case-insensitive match)
required_keywords1 = ["Symbol", "Parts Name", "Material", "Q'ty", "Parts No"]
# required_keywords2 = ["Designed", "Checked", "Approved", "DWG", Part Number (P/N), Quantity, "Description", "Material", "Dimension", "Remarks"]

# Helper to extract text from a page image using OCR
def ocr_page(page):
    img = page.to_image(resolution=300)
    pil_img = img.original
    text = pytesseract.image_to_string(pil_img)
    return text

# Extract OCR text from relevant pages only
def extract_ocr_from_pdf(pdf_path):
    # Required keywords (case-insensitive match)
    required_keywords1 = ["Symbol", "Parts Name", "Material", "Q'ty", "Parts No"]

    ocr_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # if i == 59:
            print(f"Processing Page {i+1}/{len(pdf.pages)}")
            text = ocr_page(page)
            if all(keyword.lower() in text.lower() for keyword in required_keywords1):
                ocr_texts[f"{i+1}"] = text
    return ocr_texts


# # Usage
# ocr_results = extract_ocr_from_pdf(pdf_path)

# # Optional: Print example output
# print(ocr_results["60"]) 
