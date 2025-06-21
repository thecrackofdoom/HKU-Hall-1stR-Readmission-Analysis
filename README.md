
# HKU Hall & College 1st Round Readmission Analysis

A small visualization of hall&college readmission rate in HKU. Manually extracting data from unstructured PDF documents is time-consuming and error-prone. This project automates the process and provides reusable extraction templates.
## Description:
- Data from 21 PDF files are structured into similar templates (supports multiple PDF layouts), then processed through PDFplumber to extract IDs, College, Admission Status, and (Room Type, degree, student status) if available. 
- Data is stored in a .db file using sqlite3, which is suitable for small - medium applications.
- Visualization and analysis using pandas to identify key trends.
## Key Findings:
- 
## Scalability:
- Auto-classification of pdfs to select extraction templates
- Error checking 
- Yearly updates
## File structure:
 - extract.py: Main script to run the PDF parsing and database - population.
- process.py: Contains functions for parsing specific PDF formats.
- analysis.py: Connects to the database, performs analysis, and generates visualizations.
- Fun/data/: Directory containing the raw admission PDF files.
- Fun/admission_results.db: The SQLite database where extracted data is stored.

## Tech Stack

- Python 3.x
- pdfplumber (for PDF text extraction)
- re (for regular expressions)
- sqlite3 (for database management)
- pandas (for data manipulation)
- matplotlib (for plotting)
- seaborn (for enhanced visualizations)


## Authors

- [@thecrackofdoom](https://www.github.com/thecrackofdoom)

