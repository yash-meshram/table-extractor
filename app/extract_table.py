import os
import pytesseract
from PIL import Image
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3
import os
from langchain_community.document_loaders import PyPDFLoader
from extract_text import extract_ocr_from_pdf

class ANalyzePDF:
    def __init__(self):
        self.table_schema1 = {
            "Page Number": {
                "Symbol": ["Symbol in the table text"], 
                "Part Name": ["Parts Name in the table text"],
                "Material": ["Material in the tale text"],
                "Quantity": ["Q'ty in the table text"],
                "Part Number": ["Parts No in the table text"]
            }
        }
        ["Symbol", "Parts Name", "Material", "Q'ty", "Parts No"]
        
        self.table_schema2 = {
            "Page Number": {
                "Company Name": "", 
                "Designed By": "", 
                "Checked": "", 
                "Approved": "", 
                "DWG No": "", 
                "Revision": "", 
                "Part Number (P/N)": "", 
                "Quantity": "", 
                "Description": "", 
                "Material": "", 
                "Dimension": "", 
                "Remarks": ""
            }
        }
        
    def extract_table_info(self, extracted_text, llm):
        '''Use LLM to extract structured table from the extracted text'''
        
        prompt = ChatPromptTemplate.from_template(
            """
            ## TABLE SCHEMA
            {table_schema}

            ## TABLE TEXT:
            {text}
            
            ## INSTRUCTION:
            Extract structured information from the 'TABLE TEXT' session and return it as valid JSON as a schema given in 'TABLE SCHEMA' session.
            only return the valid JSON.
            
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | llm
        response = chain.invoke(
            input = {
                "table_schema": self.table_schema1,
                "text": extracted_text
            }
        )
        return response
            

    def parse_table(self, pdf_paths, llm):
        '''extract the data from the images and return it in json format'''
        
        extracted_text = extract_ocr_from_pdf(pdf_paths)
        response = self.extract_table_info(extracted_text, llm)
        # json parser
        json_parser = JsonOutputParser()
        json_response = json_parser.parse(response.content)
        return json_response
    

    # def parse_tables_from_data_directory(self, data_directory: str, llm):
    #     '''extract the data from the all the images in the given data_directory and retun in json format'''
        
    #     pdf_paths = [
    #         os.path.join(data_directory, file_name)
    #         for file_name in os.listdir(data_directory)
    #         if file_name.endswith(("pdf", "PDF"))
    #     ]
    #     json_response = self.parse_tables(pdf_paths, llm)
    #     return json_response