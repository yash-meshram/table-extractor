from extract_table import ANalyzePDF
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd


analyze_pdf = ANalyzePDF()

def google_generative_ai_llm(model: str = "gemini-2.0-flash", temperature: float = 0.0):
    '''define a google genrative ai model'''
    
    llm = ChatGoogleGenerativeAI(
        model = model,
        temperature = temperature
    )
    return llm

llm = google_generative_ai_llm(temperature = 0.7)

response = analyze_pdf.parse_table("data/0001-0250.pdf", llm)

print(response)

def pad_columns_to_equal_length(data_dict):
    max_len = max(len(v) for v in data_dict.values())
    for key in data_dict:
        # Pad shorter lists with empty string
        while len(data_dict[key]) < max_len:
            data_dict[key].append("")
    return data_dict

with pd.ExcelWriter("output_table.xlsx", engine="openpyxl") as writer:
    for page, table_data in response.items():
        if any(len(col) > 0 for col in table_data.values()):  # skip empty sheets
            padded_data = pad_columns_to_equal_length(table_data)
            df = pd.DataFrame(padded_data)
            # Excel sheet names must be <=31 chars and not contain some special characters
            safe_sheet_name = page[:31].replace('/', '-')
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)

print("✅ Excel file 'output_table.xlsx' created successfully.")