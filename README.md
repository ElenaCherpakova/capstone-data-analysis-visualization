# Capstone Project: Data Analysis and Visualization

This repository contains my capstone project where I designed, implemented, and executed a complete data pipeline.

I applied skills in data analysis and visualization to explore cleaned data, create meaningful visualizations, and present insights effectively.

## Project Topics

- **Data Analysis:** Using Pandas to analyze cleaned datasets.  
- **Data Visualization:** Creating interactive and clear visualizations to highlight key findings.  
- **Presentation:** Delivering a comprehensive project including code, analysis, and visualizations.

## Project Components

- **Web Scraping Program:**  
  Scrapes data from the [Major League Baseball History website](https://www.baseball-almanac.com/yearmenu.shtml), assembles it into DataFrames, and stores the data as several CSV files.  

- **Database Import Program:**  
  Imports the CSV files into a MySQL database, with each CSV file stored as a separate table.

- **Database Query Program:**  
  A command-line tool to query the database using joins, for example, joining player statistics with event data.

- **Dashboard Program:**  
  Builds an interactive dashboard using Streamlit or Dash to visualize the data and allow users to explore insights.

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:ElenaCherpakova/capstone-data-analysis-visualization.git
   cd capstone-data-analysis-visualization

## Setup Instructions

1. **Create and activate a virtual environment:**

   - On macOS/Linux:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - On Windows (PowerShell):

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt


## Testing the SQL Command Program

To test SQL setup, run the `sqlcommand.py` program in a separate terminal session:

```bash
python sqlcommand.py