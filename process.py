import pdfplumber
import re

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
def jcsv4(path):
    match path:
            case "DHC.pdf":
                college = "DH Chen College"
            case "1.pdf":
                college = "1st College"
            case "2.pdf":
                college = "2nd College"
            case "KCC.pdf":
                college = "Karson Choi College"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        room_type = "Single"
        for page in pdf.pages:
            text = page.extract_text()

            suc_start = text.find("Successful Applicants")
            un_start = text.find("Unsuccessful Applicants")
            section = text[suc_start:un_start]
            if text.find("Waitlisted Applicants") != -1:
                wait_start = text.find("Waitlisted Applicants")
                section = text[suc_start:wait_start]
            
            #Successful Applicants
            successful_pattern = r"\d{10}"
            matches = re.findall(successful_pattern, section)
            for match in matches:
                uid = match
                applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': room_type, 'Degree': None, 'Student_Status': None})
            
            #Waitlisted Applicants
            if text.find("Waitlisted Applicants") != -1:
                section = text[wait_start:un_start]
                wait_pattern = r"\d{10}"
                matches = re.findall(wait_pattern, section)
                for match in matches:
                    uid = match
                    applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': None})

            # Unsuccessful Applicants
            section = text[un_start:]
            unsuccessful_pattern = r"\d{10}"
            matches = re.findall(unsuccessful_pattern, section)
            for match in matches:
                uid = match
                applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def jcsv2(path):
    match path:
        case "LSK.pdf":
            college = "Lee Shau Kee Hall"
        case "MH.pdf":
            college = "Morrison Hall"
        case "SCSH.pdf":
            college = "Suen Chi Sun Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        
        
        pattern = r"\d{10}\s\w+"
        matches = re.findall(pattern, text)
        for match in matches:
            uid, status = match.split()
            applicant_data.append({'UID': uid, 'College': college, 'Status': status, 'Room_Type': None, 'Degree': None, 'Student_Status': None})
            
    return applicant_data
def lhth(path):
    college = "Lady Ho Tung Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        
        suc_start = text.find("Successful lists")
        un_start = text.find("Unsuccessful lists")
        section = text[suc_start:un_start]
        
        #Successful Applicants
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
            
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def lhh(path):
    college = "Lee Hysan Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        print (text)
        a = text.find("Successful - Local Underffraduate")
        b = text.find("Unsuccessful - Local Underffraduate")
        c = text.find("Pending - Local Undergraduate")
        d = text.find("Successful - Non Local Underffraduate")
        e = text.find("Unsuccessful - Non Local Undergraduate")
        f = text.find("Successful - Postgraduate")
        g = text.find("Unsuccessful - Postgraduate")
        
        #Successful Local Applicants
        section = text[a:b]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': "Undergraduate", 'Student_Status': "Local"})
            
        # Unsuccessful Local Applicants
        section = text[b:c]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': "Undergraduate", 'Student_Status': "Local"})
        
        # Pending Local Applicants
        section = text[c:d]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': "Undergraduate", 'Student_Status': "Local"})
        
        # Successful Non-local Applicants
        section = text[d:e]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': "Undergraduate", 'Student_Status': "Non-local"})
        
        # Unsuccessful Non-local Applicants
        section = text[e:f]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': "Undergraduate", 'Student_Status': "Non-local"})
        
        # Successful Postgraduate Applicants
        section = text[f:g]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': "Postgraduate", 'Student_Status': None})
        
        # Unsuccessful Postgraduate Applicants
        section = text[g:]
        pattern = r"\d{10}"
        matches = re.findall(pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': "Postgraduate", 'Student_Status': None})
    return applicant_data
def rclee(path):
    college = "RC Lee Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        print (text)
        suc_start = text.find("Successful list")
        w_start = text.find("Local(Femaleand Male)")
        w_st = text.find("Non-Local (Femaleand Male)")
        un_start = text.find("Unsuccessful list")
        
        
        #Successful Applicants.
        section = text[suc_start:w_start]
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
        
        #Waitlisted Local Applicants
        section = text[w_start:w_st]
        wait_pattern = r"\d{10}"
        matches = re.findall(wait_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': "Local"})
        
        #Waitlisted Non-local Applicants
        section = text[w_st:un_start]
        wait_pattern = r"\d{10}"
        matches = re.findall(wait_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': "Non-local"})
        
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def ricci(path):
    college = "Ricci Hall"
    room_type = "Single"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        print(text)
        suc_start = text.find("offered")
        w_start = text.find("waitlisted.")
        un_start = text.find("unsuccessful")
        
        
        #Successful Applicants.
        section = text[suc_start:w_start]
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': room_type, 'Degree': None, 'Student_Status': None})

        #Waitlisted Applicants
        section = text[w_start:un_start]
        wait_pattern = r"\d{10}"
        matches = re.findall(wait_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
        
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def skylee(path):
    college = "Simon K.Y. Lee Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        
        suc_start = text.find("Successful")
        w_start = text.find("Waitlisted")
        un_start = text.find("Unsuccessful")
        
        
        #Successful Applicants
        section = text[suc_start:w_start]
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
        
        #Waitlisted Applicants
        section = text[w_start:un_start]
        wait_pattern = r"\d{10}"
        matches = re.findall(wait_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Waitlisted', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
            
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def sjc(path):
    college = "St John's College"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        
        suc_start = text.find("Successful")
        un_start = text.find("Unsuccessful")
        
        
        #Successful Applicants
        section = text[suc_start:un_start]
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': "Single", 'Degree': None, 'Student_Status': None})
        
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
def starr(path):
    college = "Starr Hall"
    with pdfplumber.open(f"Fun/data/{path}") as pdf:
        applicant_data = []
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            text += "\n"  # Ensure each page's text is separated
        
        suc_start = text.find("Successful List")
        un_start = text.find("Unsuccessful List")
        
        
        #Successful Applicants
        section = text[suc_start:un_start]
        successful_pattern = r"\d{10}"
        matches = re.findall(successful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Successful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
        
        # Unsuccessful Applicants
        section = text[un_start:]
        unsuccessful_pattern = r"\d{10}"
        matches = re.findall(unsuccessful_pattern, section)
        for match in matches:
            uid = match
            applicant_data.append({'UID': uid, 'College': college, 'Status': 'Unsuccessful', 'Room_Type': None, 'Degree': None, 'Student_Status': None})
    return applicant_data
