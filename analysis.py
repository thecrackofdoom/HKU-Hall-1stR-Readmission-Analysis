'''import sqlite3
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
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

if __name__ == "__main__":
    database_file = "Fun/admission_results.db" # !! IMPORTANT: Ensure this path is correct and accessible !!

    conn = create_connection(database_file)

    if conn:
        print(f"Successfully connected to {database_file}")

        # Fetch all data from the 'applicants' table into a Pandas DataFrame
        try:
            # We select all columns here, in case 'room_type' is needed for analysis later
            df = pd.read_sql_query("SELECT college, admission_status, room_type FROM applicants", conn)
            print("Data loaded into DataFrame for analysis.")
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading data from database: {e}")
            df = pd.DataFrame() # Create an empty DataFrame to prevent further errors
        finally:
            conn.close() # Always close the connection when done

        if not df.empty:
            # Clean up inconsistent status entries if any (e.g., 'successful' vs 'Successful')
            df['admission_status'] = df['admission_status'].str.capitalize()

            # --- Analysis 1: Re-confirming the counts from the summary (as provided by you) ---
            print("\n--- Re-confirming Admission Summary Counts from Database ---")
            summary_counts = df.groupby(['college', 'admission_status']).size().reset_index(name='count')
            print(summary_counts.to_string())

            # --- Analysis 2: Calculate and Visualize Percentage of Admission Status per College ---
            print("\n--- Generating Percentage of Admission Status per College Visualization ---")

            # Calculate counts of each admission status per college
            status_counts_per_college = df.groupby(['college', 'admission_status']).size().reset_index(name='count')

            # Calculate total applicants per college
            total_applicants_per_college = df.groupby('college').size().reset_index(name='total_college_applicants')

            # Merge to get total applicants per college in the status_counts_per_college DataFrame
            status_percentages_df = pd.merge(status_counts_per_college, total_applicants_per_college, on='college')

            # Calculate percentage
            status_percentages_df['percentage'] = (status_percentages_df['count'] / status_percentages_df['total_college_applicants']) * 100

            # Plotting using Seaborn
            plt.figure(figsize=(16, 9)) # Increased figure size for better readability with many colleges
            sns.barplot(
                x='college',
                y='percentage',
                hue='admission_status',
                data=status_percentages_df,
                palette='viridis' # Chosen palette for distinct colors
            )
            plt.title('Percentage of Admission Status per College', fontsize=16)
            plt.xlabel('College', fontsize=12)
            plt.ylabel('Percentage of Applicants (%)', fontsize=12)
            plt.xticks(rotation=60, ha='right', fontsize=10) # More rotation for long college names
            plt.yticks(fontsize=10)
            plt.legend(title='Admission Status', bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.) # Adjust legend position
            plt.tight_layout() # Adjust layout to prevent labels/legend from overlapping
            plt.show()

            # --- Analysis 3: Overall Admission Status Proportions (Pie Chart) ---
            print("\n--- Generating Overall Admission Status Proportions (Pie Chart) ---")
            overall_status_counts = df['admission_status'].value_counts()

            plt.figure(figsize=(8, 8))
            plt.pie(overall_status_counts, labels=overall_status_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
            plt.title('Overall Admission Status Proportions', fontsize=16)
            plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.show()

            # --- Analysis 4: Room Type Distribution for Successful Applicants (Bar Chart) ---
            print("\n--- Generating Room Type Distribution for Successful Applicants (Bar Chart) ---")
            # Filter for successful applicants with valid room_type
            successful_room_types = df[
                (df['admission_status'] == 'Successful') &
                (df['room_type'].notna()) &
                (df['room_type'] != '')
            ]

            if not successful_room_types.empty:
                room_type_counts = successful_room_types['room_type'].value_counts().sort_values(ascending=False)

                plt.figure(figsize=(10, 6))
                sns.barplot(x=room_type_counts.index, y=room_type_counts.values, palette='plasma') # Another distinct palette
                plt.title('Distribution of Room Types for Successful Applicants', fontsize=14)
                plt.xlabel('Room Type', fontsize=12)
                plt.ylabel('Number of Applicants', fontsize=12)
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.yticks(fontsize=10)
                plt.tight_layout()
                plt.show()
            else:
                print("  No room type data found for successful applicants to visualize.")

        else:
            print("No data found in the 'applicants' table to perform analysis. Ensure your parsing script ran successfully.")

    else:
        print("Could not establish database connection. Analysis cannot be performed.")'''
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

if __name__ == "__main__":
    database_file = "Fun/admission_results.db" # !! IMPORTANT: Ensure this path is correct and accessible !!

    conn = create_connection(database_file)

    if conn:
        print(f"Successfully connected to {database_file}")

        # Fetch all data from the 'applicants' table into a Pandas DataFrame
        try:
            # Select all relevant columns including 'year'
            df = pd.read_sql_query("SELECT applicant_id, college, admission_status, room_type, degree, student_status, year FROM applicants", conn)
            print("Data loaded into DataFrame for analysis.")
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading data from database: {e}")
            df = pd.DataFrame() # Create an empty DataFrame to prevent further errors
        finally:
            conn.close() # Always close the connection when done

        if not df.empty:
            # Clean up inconsistent status entries (e.g., 'successful' vs 'Successful')
            df['admission_status'] = df['admission_status'].str.capitalize()
            # Ensure 'year' is numeric and handles potential missing/malformed values
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

            # --- Analysis 1: Re-confirming the counts from the summary (as provided by you) ---
            print("\n--- Re-confirming Admission Summary Counts from Database ---")
            summary_counts = df.groupby(['year', 'college', 'admission_status']).size().reset_index(name='count')
            print(summary_counts.to_string())

            # --- Analysis 2: Total Applicants Per Year ---
            print("\n--- Generating Total Applicants Per Year Visualization ---")
            total_applicants_per_year = df.groupby('year').size().reset_index(name='total_applicants')
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='year', y='total_applicants', data=total_applicants_per_year, marker='o')
            plt.title('Total Applicants Per Year', fontsize=16)
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Number of Applicants', fontsize=12)
            plt.xticks(total_applicants_per_year['year'].unique()) # Ensure all years are ticks
            plt.grid(True)
            plt.tight_layout()
            plt.show()

            # --- Analysis 3: Overall Admission Status Proportions Per Year (Stacked Bar Chart) ---
            print("\n--- Generating Overall Admission Status Proportions Per Year Visualization ---")
            overall_status_yearly = df.groupby(['year', 'admission_status']).size().unstack(fill_value=0)
            overall_status_yearly_percentage = overall_status_yearly.apply(lambda x: x / x.sum(), axis=1) * 100

            plt.figure(figsize=(12, 7))
            overall_status_yearly_percentage.plot(kind='bar', stacked=True, colormap='viridis')
            plt.title('Overall Admission Status Proportions Per Year', fontsize=16)
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Percentage of Applicants (%)', fontsize=12)
            plt.xticks(rotation=0) # No rotation needed for years
            plt.legend(title='Admission Status', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()

            # --- Analysis 4: Percentage of Admission Status per College (Yearly Comparison) ---
            print("\n--- Generating Percentage of Admission Status per College (Yearly Comparison) Visualization ---")

            # Calculate counts of each admission status per college per year
            status_counts_per_college_year = df.groupby(['year', 'college', 'admission_status']).size().reset_index(name='count')

            # Calculate total applicants per college per year
            total_applicants_per_college_year = df.groupby(['year', 'college']).size().reset_index(name='total_college_applicants')

            # Merge to get total applicants per college per year in the status_counts_per_college_year DataFrame
            status_percentages_df_yearly = pd.merge(status_counts_per_college_year, total_applicants_per_college_year, on=['year', 'college'])

            # Calculate percentage
            status_percentages_df_yearly['percentage'] = (status_percentages_df_yearly['count'] / status_percentages_df_yearly['total_college_applicants']) * 100

            # Option A: Faceting by Year (good if you have 2-4 years)
            g = sns.catplot(
                x='college',
                y='percentage',
                hue='admission_status',
                col='year',
                data=status_percentages_df_yearly,
                kind='bar',
                col_wrap=2, # Wrap columns after 2 plots per row
                height=5, aspect=1.8, # Adjust height and aspect for readability
                palette='viridis',
                sharey=True,
                legend_out=True # Place legend outside for multi-plot
            )
            g.set_axis_labels("College", "Percentage of Applicants (%)")
            g.set_titles("Year: {col_name}")
            g.set_xticklabels(rotation=75, ha='right')
            plt.suptitle('Percentage of Admission Status per College by Year', y=1.02, fontsize=18) # Adjust suptitle position
            plt.tight_layout(rect=[0, 0, 1, 0.98]) # Adjust layout for suptitle
            plt.show()


            # --- Analysis 5: Room Type Distribution for Successful Applicants (Overall and Per Year) ---
            print("\n--- Generating Room Type Distribution for Successful Applicants (Overall & Per Year) ---")
            successful_room_types = df[
                (df['admission_status'] == 'Successful') &
                (df['room_type'].notna()) &
                (df['room_type'] != '')
            ]

            if not successful_room_types.empty:
                # Overall Room Type Distribution
                plt.figure(figsize=(10, 6))
                room_type_counts_overall = successful_room_types['room_type'].value_counts().sort_values(ascending=False)
                sns.barplot(x=room_type_counts_overall.index, y=room_type_counts_overall.values, palette='cubehelix')
                plt.title('Overall Distribution of Room Types for Successful Applicants', fontsize=14)
                plt.xlabel('Room Type', fontsize=12)
                plt.ylabel('Number of Applicants', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()

                # Room Type Distribution Per Year (if enough data)
                if len(successful_room_types['year'].unique()) > 1:
                    plt.figure(figsize=(12, 7))
                    sns.countplot(
                        x='room_type',
                        hue='year',
                        data=successful_room_types,
                        palette='mako',
                        order=successful_room_types['room_type'].value_counts().index # Order by overall frequency
                    )
                    plt.title('Room Type Distribution for Successful Applicants by Year', fontsize=14)
                    plt.xlabel('Room Type', fontsize=12)
                    plt.ylabel('Number of Applicants', fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                    plt.legend(title='Year')
                    plt.tight_layout()
                    plt.show()
                else:
                    print("  Not enough year data for room type distribution by year.")
            else:
                print("  No room type data found for successful applicants to visualize.")

        else:
            print("No data found in the 'applicants' table to perform analysis. Ensure your parsing script ran successfully.")

    else:
        print("Could not establish database connection. Analysis cannot be performed.")