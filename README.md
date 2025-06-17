# Capstone Project: Data Analysis and Visualization

This repository contains my capstone project where I designed, implemented, and executed a complete data pipeline.

I applied skills in data analysis and visualization to explore cleaned data, create meaningful visualizations, and present insights effectively.

# Project Topics

- **Data Analysis: ** Using Pandas to analyze cleaned datasets.
- **Data Visualization: ** Creating interactive and clear visualizations to highlight key findings.
- **Presentation: ** Delivering a comprehensive project including code, analysis, and visualizations.

# Project Components

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
    git clone git@github.com: ElenaCherpakova/capstone-data-analysis-visualization.git
    cd capstone-data-analysis-visualization

# Setup Instructions

1. **Create and activate a virtual environment:**

   - On macOS/Linux:

        ```bash
        python3 - m venv .venv
        source .venv/bin/activate
        ```

    - On Windows(PowerShell):

        ```bash
        python - m venv .venv
        source .venv/Scripts/activate
        code .
        ```
2. **Important:** Open the VSCode command pallette (ctrl-shift P).  In the `Python: Select Interpreter` option, choose the one with `.venv`.  You can use the search box at the top to find it.  If you have any terminal sessions open, close them, and open a new one.  You will see `(.venv)` in your terminal prompt.

3. **Install dependencies:**

   ```bash
    pip install - r requirements.txt
    ```

# Testing the SQL Command Program

```bash
python sql_commands.py
```
# Running Streamlit
```bash
streamlit run streamlit.py 
```
