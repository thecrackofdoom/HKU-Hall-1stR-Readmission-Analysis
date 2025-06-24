import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Make plots look nicer
sns.set_theme(style="whitegrid")

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def individual_analysis(df):
    print("\n'College' column (Series): ", df.loc[df["year"] == 2024, "college"].unique())


if __name__ == "__main__":
    database_file = "Personal_Projects/HKUHall/admission_results.db"
    print("Using database file:", os.path.abspath(database_file))
    conn = create_connection(database_file)

    if conn:
        print(f"Successfully connected to {database_file}")

        # Fetch all data from the 'applicants' table into a Pandas DataFrame
        try:
            df = pd.read_sql_query("SELECT applicant_id, college, admission_status, room_type, degree, student_status, year FROM applicants", conn)
            print("Data loaded into DataFrame for analysis.")
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading data from database: {e}")
            df = pd.DataFrame() # Create an empty DataFrame to prevent further errors
        finally:
            conn.close()

        if not df.empty:
            individual_analysis(df)
            