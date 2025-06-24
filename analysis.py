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
    colleges = df.loc[df["year"] == 2024, "college"].unique()
    data = []
    for college in colleges:
        for year in df["year"].unique():
            college_yr = df[(df["college"] == college) & (df["year"] == year)]
            total_applicants = college_yr.shape[0]
            figures = college_yr.get('admission_status').value_counts().to_dict()
            for key, value in figures.items():
                data.append({
                    "year": year,
                    "college": college,
                    "admission_status": key,
                    "percentage": round(value / total_applicants * 100, 3)
                })
    plot_data = pd.DataFrame(data)
    
    colleges = plot_data["college"].unique()
    
    for college in colleges:
        college_data = plot_data[plot_data["college"] == college]
        plt.figure(figsize=(10, 6)) # Adjust figure size as needed

        sns.lineplot(
            x='year',
            y='percentage',
            hue='admission_status',
            data=college_data,
            marker='o', # Add markers to points
            linewidth=2 # Line thickness
        )

        plt.title(f"Admission Status Percentages for {college} (YoY)", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Percentage (%)", fontsize=12)
        plt.xticks(college_data['year'].unique()) # Ensure all relevant years are shown as ticks
        plt.ylim(0, 100) # Percentages are from 0 to 100
        plt.grid(True) # Add a grid for readability
        plt.legend(title='Admission Status', bbox_to_anchor=(1.05, 1), loc='upper left') # Place legend outside
        plt.tight_layout()
        plt.savefig(f"Personal_Projects/HKUHall/assets/{college.replace(' ', '_')}_Admission_YoY.png")
        plt.close() # Close the plot to free memory
        print(f"Generated {college.replace(' ', '_')}_Admission_YoY.png")
                
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
            