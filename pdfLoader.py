import os
from langchain_community.document_loaders import PyPDFLoader

class PDFLoader:
    # Loading a single document
    async def load_pdf(file_path: str) -> list:
        loader = PyPDFLoader(file_path = file_path)
        pages = []
        async for page in loader.alazy_load():
            pages.append(page)
        return pages

    # Loading multiple documents
    async def load_pdfs(file_paths: list) -> list:
        document_pages = []
        for file_path in file_paths:
            loader = PyPDFLoader(file_path = file_path)
            async for page in loader.alazy_load():
                document_pages.append(page)
        return document_pages

    # Loading all PDFs in the given directory
    async def load_all_pdfs_from_directory(data_directory) -> list:
        file_paths = [
            os.path.join(data_directory, file_name)
            for file_name in os.listdir(data_directory)
            if file_name.endswith(".pdf")
        ]
        return await PDFLoader.load_pdfs(file_paths)
        
    
import asyncio
import nest_asyncio
if __name__ == "__main__":
    async def main():
        pages = await PDFLoader.load_all_pdfs_from_directory("data")
        print(pages[59])
    
    
    nest_asyncio.apply()

    asyncio.run(main())