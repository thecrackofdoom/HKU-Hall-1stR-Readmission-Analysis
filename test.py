import pdfplumber
import re
path = "LHTH.pdf"
with pdfplumber.open(f"Fun/data/{path}") as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

            success = []
            unsuccess = []
            
            suc_start = text.find("Successful lists")
            print(suc_start)
            
            un_start = text.find("Unsuccessful lists")
            section = text[suc_start:un_start]
            print(section)
            
            successful_pattern = r"\d{10}"
            matches = re.findall(successful_pattern, section)
            for match in matches:
                uid = match
                success.append({'UID': uid})
            #print(success)
            
            section = text[un_start:]
            #print(section)
            unsuccessful_pattern = r"\d{10}"
            matches = re.findall(unsuccessful_pattern, section)
            for match in matches:
                uid = match
                unsuccess.append({'UID': uid})
            #print(unsuccess)
                
                