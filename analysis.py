import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Make plots look nicer
sns.set_theme(style="whitegrid")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

database_file = "Fun/admission_results.db"
conn = create_connection(database_file)

if conn:
    # Fetch data into a Pandas DataFrame for easier manipulation and plotting
    df = pd.read_sql_query("SELECT * FROM applicants", conn)
    conn.close() # Close connection after fetching data

    print("Data loaded into DataFrame. Starting visualizations...")

    # --- Visualization 1: Admission Status Breakdown by College (Bar Chart) ---
    print("\n--- Generating Admission Status Breakdown by College ---")
    status_by_college = df.groupby(['college', 'admission_status']).size().unstack(fill_value=0)

    # Plotting
    status_by_college.plot(kind='bar', stacked=True, figsize=(12, 7))
    plt.title('Admission Status Breakdown by College')
    plt.xlabel('College')
    plt.ylabel('Number of Applicants')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Admission Status')
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    plt.show()

    # --- Visualization 2: Room Type Distribution for Successful Applicants (Bar Chart) ---
    print("\n--- Generating Room Type Distribution for Successful Applicants ---")
    successful_room_types = df[
        (df['admission_status'] == 'Successful') &
        (df['room_type'].notna()) &
        (df['room_type'] != '')
    ]

    if not successful_room_types.empty:
        room_type_counts = successful_room_types.groupby('room_type').size().sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=room_type_counts.index, y=room_type_counts.values, palette='viridis')
        plt.title('Distribution of Room Types for Successful Applicants')
        plt.xlabel('Room Type')
        plt.ylabel('Number of Applicants')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("  No room type data found for successful applicants to visualize.")

    # --- Visualization 3: Overall Admission Status Proportions (Pie Chart) ---
    print("\n--- Generating Overall Admission Status Proportions ---")
    overall_status_counts = df['admission_status'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(overall_status_counts, labels=overall_status_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Overall Admission Status Proportions')
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    # --- New Visualization: Percentage of Admission Status per College ---
    print("\n--- Generating Percentage of Admission Status per College ---")

    # Calculate counts of each admission status per college
    status_counts_per_college = df.groupby(['college', 'admission_status']).size().reset_index(name='count')

    # Calculate total applicants per college
    total_applicants_per_college = df.groupby('college').size().reset_index(name='total_college_applicants')

    # Merge to get total applicants per college in the status_counts_per_college DataFrame
    status_percentages_df = pd.merge(status_counts_per_college, total_applicants_per_college, on='college')

    # Calculate percentage
    status_percentages_df['percentage'] = (status_percentages_df['count'] / status_percentages_df['total_college_applicants']) * 100

    # Plotting using Seaborn
    plt.figure(figsize=(14, 8))
    sns.barplot(
        x='college',
        y='percentage',
        hue='admission_status',
        data=status_percentages_df,
        palette='Spectral' # Choose a color palette
    )
    plt.title('Percentage of Admission Status per College')
    plt.xlabel('College')
    plt.ylabel('Percentage of Applicants (%)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Admission Status', bbox_to_anchor=(1.05, 1), loc='upper left') # Place legend outside
    plt.tight_layout()
    plt.show()
else:
    print("Could not establish database connection. Cannot perform visualizations.")