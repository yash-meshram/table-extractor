import pdfplumber

with pdfplumber.open("data/0001-0250.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
        #     for row in table:
        #         print(row)
            print(page.page_number, table)
