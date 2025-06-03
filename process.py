def jcsv3(path):
    match path:
            case "SHC.pdf":
                college = "Shun Hing College"
            case "CSC.pdf":
                college = "Chi Sun College"
            case "LCC.pdf":
                college = "Lap Chee College"
            case "NC.pdf":
                college = "New College"
        with pdfplumber.open(f"Fun/data/{path}") as pdf:
            applicant_data = []
            for page in pdf.pages:
                text = page.extract_text()
                
                suc_start = text.find("Successful Applicants")
                un_start = text.find("Unsuccessful Applicants")
                section = text[suc_start:un_start]
                if text.find("Waitlisted Applicants") != -1:
                    wait_start = text.find("Waitlisted Applicants")
                    section = text[suc_start:wait_start]
                
                if college != "New College":
                    successful_pattern = r"\d{10}\s\w+"
                    matches = re.findall(successful_pattern, section)
                    for match in matches:
                        uid, room_type = match.split()
                        applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': room_type, 'Degree': None, 'Student_Status': None})
                else:
                    successful_pattern = r"\d{10}"
                    matches = re.findall(successful_pattern, section)
                    for match in matches:
                        uid = match
                        applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': "Double", 'Degree': None, 'Student_Status': None})
                
                if text.find("Waitlisted Applicants") != -1:
                    section = text[wait_start:un_start]
                    wait_pattern = r"\d{10}"
                    matches = re.findall(wait_pattern, section)
                    for match in matches:
                        uid = match
                        applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': None})

                section = text[un_start:]
                unsuccessful_pattern = r"\d{10}"
                matches = re.findall(unsuccessful_pattern, section)
                for match in matches:
                    uid = match
                    applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
        return applicant_data
