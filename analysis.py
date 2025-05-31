'''
import pdfplumber
pdf = pdfplumber.open("Fun/data/1.pdf")
page = pdf.pages[0]
print(page.extract_text())
'''
import sqlite3
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
    """Insert a new applicant into the applicants table."""
    sql = """
    INSERT INTO applicants(applicant_id, college, admission_status, room_type, degree, student_status)
    VALUES(?,?,?,?,?,?)
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql, applicant_data)
        conn.commit()
        print(f"Inserted applicant: {applicant_data[0]}")
    except sqlite3.IntegrityError:
        print(f"Applicant ID {applicant_data[0]} already exists, skipping insertion.")
    except sqlite3.Error as e:
        print(f"Error inserting applicant {applicant_data[0]}: {e}")
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
if __name__ == "__main__":
    database_file = "Fun/admission_results.db"

    # 1. Connect to the database
    conn = create_connection(database_file)

    if conn:
        # 2. Create the table
        create_table(conn)
        summary = get_admission_summary(conn)
        for row in summary:
            college, status, count = row
            print(f"College: {college}, Status: {status}, Count: {count}")
