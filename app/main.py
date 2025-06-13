from extract_table import ANalyzePDF
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import os
import streamlit as st



def get_table(file):

    os.makedirs("data/Temp", exist_ok=True)
    temp_path = f"data/Temp/{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())
    
    analyze_pdf = ANalyzePDF()

    def google_generative_ai_llm(model: str = "gemini-2.0-flash", temperature: float = 0.0):
        '''define a google genrative ai model'''
        
        llm = ChatGoogleGenerativeAI(
            model = model,
            temperature = temperature
        )
        return llm

    llm = google_generative_ai_llm(temperature = 0.7)

    # file_path = temp_path
    file_name = os.path.basename(temp_path)
    output_file_name = f"output_table_{file_name}.xlsx"

    response = analyze_pdf.parse_table(temp_path, llm)
    
    os.remove(temp_path)

    # print(response)

    def pad_columns_to_equal_length(data_dict):
        max_len = max(len(v) for v in data_dict.values())
        for key in data_dict:
            # Pad shorter lists with empty string
            while len(data_dict[key]) < max_len:
                data_dict[key].append("")
        return data_dict

    with pd.ExcelWriter(f"{output_file_name}", engine="openpyxl") as writer:
        for page, table_data in response.items():
            if any(len(col) > 0 for col in table_data.values()):  # skip empty sheets
                padded_data = pad_columns_to_equal_length(table_data)
                df = pd.DataFrame(padded_data)
                # Excel sheet names must be <=31 chars and not contain some special characters
                safe_sheet_name = page[:31].replace('/', '-')
                df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                
    return output_file_name

    # print(f"Excel file 'output_table_{file_name}.xlsx' created successfully.")



st.title("Table Extracter")

st.text("Extracting the table from the given pdf.\nTable columns = ['Symbol', 'Parts Name', 'Material', 'Q'ty', 'Parts No']")

uploaded_file = st.file_uploader("Upload pdf file", type=["pdf", "PDF"], accept_multiple_files = False)

if uploaded_file:
    submit = st.button("Submit")
    
    if submit:
        with st.spinner("Extracting Table..."):
            output_file_name = get_table(uploaded_file)
        st.success("Table Extracted Successfully!")
        
        with open(output_file_name, "rb") as f:
            st.download_button(
                label="Download Extracted Excel",
                data=f,
                file_name=output_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

