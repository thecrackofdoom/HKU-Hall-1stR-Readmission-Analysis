'''

pdf = pdfplumber.open("Fun/data/1.pdf")
page = pdf.pages[0]
print(page.extract_text())
'''
import re
import sqlite3
import pdfplumber
import process as p
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
    sql = """
    INSERT OR REPLACE INTO applicants(applicant_id, college, admission_status, room_type, degree, student_status)
    VALUES(?,?,?,?,?,?)
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql, applicant_data)
        conn.commit()
        # print(f"Inserted or replaced applicant: {applicant_data[0]}")
    except sqlite3.Error as e:
        print(f"Error inserting/replacing applicant {applicant_data[0]} from {applicant_data[1]}: {e}")
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
    jcsv2 = ["LSK.pdf","SCSH.pdf","MH.pdf"]
    jcsv3 = ["SHC.pdf", "CSC.pdf", "LCC.pdf", "NC.pdf"]
    jcsv4 = ["DHC.pdf", "1.pdf", "2.pdf", "KCC.pdf"]
    sassoon = ["RCLee.pdf", "LHH.pdf","WL.pdf"]
    campus = ["Swire.pdf","SKYLee.pdf", "UH.pdf", "SJC.pdf"]
    college = "null"
    
    if path in jcsv3:
        return p.jcsv3(path)
    elif path in jcsv4:
        return p.jcsv4(path)
    elif path in jcsv2:
        return p.jcsv2(path)
    match path:
        case "LHTH.pdf":
            return p.lhth(path)
        case "LHH.pdf":
            return p.lhh(path)
        case "RCLee.pdf":
            return p.rclee(path)
        case "Ricci.pdf":
            return p.ricci(path)
        case "SKYLee.pdf":
            return p.skylee(path)
        case "SJC.pdf":
            return p.sjc(path)
        case "Starr.pdf":
            return p.starr(path)
        case "Swire.pdf":
            return p.swire(path)
        case "UH.pdf":
            return p.uh(path)
        case "WL.pdf":
            return p.wl(path)

        
            
if __name__ == "__main__":
    database_file = "Fun/admission_results.db"

    # 1. Connect to the database
    conn = create_connection(database_file)

    if conn:
        # 2. Create the table
        create_table(conn)
        
        """cursor = conn.cursor()
        cursor.execute("DELETE FROM applicants")
        conn.commit()
        print("Cleared existing data from 'applicants' table.")
        Not needed for production, but useful for testing."""
        
        added = ["SHC.pdf", "CSC.pdf", "LCC.pdf", "NC.pdf", "DHC.pdf", "1.pdf", "2.pdf", "KCC.pdf","LHTH.pdf","LHH.pdf","LSK.pdf","MH.pdf","RCLee.pdf","Ricci.pdf","SKYLee.pdf", "SJC.pdf","Starr.pdf","SCSH.pdf", "Swire.pdf", "UH.pdf", "WL.pdf"]
        adding = []
        for filename in adding:
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
    
