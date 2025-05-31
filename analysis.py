'''

pdf = pdfplumber.open("Fun/data/1.pdf")
page = pdf.pages[0]
print(page.extract_text())
'''
import re
import sqlite3
import pdfplumber
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn
def create_table(conn):
    try:
        # SQL statement to create a table
        sql_create_applicants_table = """
        CREATE TABLE IF NOT EXISTS applicants (
            applicant_id TEXT PRIMARY KEY,
            college TEXT NOT NULL,
            admission_status TEXT NOT NULL,
            room_type TEXT,
            degree TEXT,
            student_status TEXT
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_applicants_table)
        print("Table 'applicants' created or already exists.")
    except sqlite3.Error as e:
        print(e)
def insert_applicant(conn, applicant_data):
    """
    Insert a new applicant into the applicants table.
    applicant_data should be a tuple: (UID, College, Status, Room_Type, Degree, Student_Status)
    """
    sql = """
    INSERT INTO applicants(applicant_id, college, admission_status, room_type, degree, student_status)
    VALUES(?,?,?,?,?,?)
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql, applicant_data)
        conn.commit()
        # print(f"Inserted applicant: {applicant_data[0]}") # Uncomment for verbose logging
    except sqlite3.IntegrityError:
        # print(f"Applicant ID {applicant_data[0]} already exists, skipping insertion.")
        pass # Suppress output if it's expected behavior, as PRIMARY KEY handles duplicates
    except sqlite3.Error as e:
        print(f"Error inserting applicant {applicant_data[0]} from {applicant_data[1]}: {e}")


def get_all_applicants(conn):
    """Query all rows in the applicants table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applicants")
    rows = cursor.fetchall()
    return rows
def get_admission_summary(conn):
    """Get a summary of admission statuses per college."""
    sql_summary = """
    SELECT
        college,
        admission_status,
        COUNT(applicant_id) as count
    FROM
        applicants
    GROUP BY
        college, admission_status
    ORDER BY
        college, admission_status;
    """
    cursor = conn.cursor()
    cursor.execute(sql_summary)
    rows = cursor.fetchall()
    return rows
def process(path, conn):
    jcsv1 = ["LHTH.pdf","Starr.pdf","Ricci.pdf"]
    jcsv2 = ["LSK.pdf","SCSH.pdf","MH.pdf","SJC.pdf"]
    jcsv3 = ["SHC.pdf", "CSC.pdf", "LCC.pdf", "NC.pdf"]
    jcsv4 = ["DHC.pdf", "1.pdf", "2.pdf", "KCC.pdf"]
    sassoon = ["RCLee.pdf", "LHH.pdf","WL.pdf"]
    campus = ["Swire.pdf","SKYLee.pdf", "UH.pdf"]
    college = "null"
    if path in jcsv3:
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
    elif path in jcsv4:
        match path:
            case "DHC.pdf":
                college = "DH Chen College"
            case "1.pdf":
                college = "1st College"
            case "2.pdf":
                college = "2nd College"
            case "KCC.pdf":
                college = "Karson Choi College"
            
if __name__ == "__main__":
    database_file = "Fun/admission_results.db"

    # 1. Connect to the database
    conn = create_connection(database_file)

    if conn:
        # 2. Create the table
        create_table(conn)
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applicants")
        conn.commit()
        print("Cleared existing data from 'applicants' table.")
        
        for filename in ["SHC.pdf", "CSC.pdf", "LCC.pdf", "NC.pdf"]:
            extracted_applicants = process(filename, conn)
            print(f"  Found {len(extracted_applicants)} applicants for {filename}.")
            for applicant in extracted_applicants:
                insert_applicant(
                    conn,
                    (applicant['UID'], applicant['College'], applicant['Status'],
                     applicant['Room_Type'], applicant['Degree'], applicant['Student_Status'])
                )

            print(f"  Data from {filename} inserted/skipped successfully.")
        
        summary = get_admission_summary(conn)
        for row in summary:
            college, status, count = row
            print(f"College: {college}, Status: {status}, Count: {count}")
    
