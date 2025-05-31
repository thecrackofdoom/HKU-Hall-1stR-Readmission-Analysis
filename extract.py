import pdfplumber
import re
path = "SHC.pdf"
with pdfplumber.open(f"Fun/data/{path}") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                success = []
                unsuccess = []
                
                suc_start = text.find("Successful Applicants")
                un_start = text.find("Unsuccessful Applicants")
                section = text[suc_start:un_start]
                
                successful_pattern = r"\d{10}\s\w+"
                matches = re.findall(successful_pattern, section)
                for match in matches:
                    uid, room_type = match.split()
                    success.append({'UID': uid, 'Room_Type': room_type})
                
                section = text[un_start:]
                print(section)
                unsuccessful_pattern = r"\d{10}"
                matches = re.findall(unsuccessful_pattern, section)
                for match in matches:
                    uid = match
                    unsuccess.append({'UID': uid})
                print(unsuccess)
                
                