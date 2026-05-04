# IPL Data Analysis Project

## Project Objective
Analyze IPL match data using Python, Pandas, and Matplotlib.

## Dataset
File used: `matches(3).csv`

Rows: 636  
Columns: 18

## Key Questions Answered
1. How many IPL matches were played each season?
2. Which teams won the most matches?
3. What is the most common toss decision?
4. Does winning the toss help in winning the match?
5. Who won the most Player of the Match awards?
6. Which venues hosted the most IPL matches?
7. Which teams have the highest win percentage?

## Main Insights
- Total matches analyzed: 636
- Season range: 2008 to 2017
- Most winning team: Mumbai Indians
- Top Player of the Match award winner: CH Gayle
- Most common toss decision: field
- Toss winner also won match in: 51.34%

## Files Included
- `ipl_analysis_project.py` - main Python project file
- `cleaned_ipl_matches.csv` - cleaned dataset
- `ipl_analysis_summary.xlsx` - Excel summary tables
- `project_summary.csv` - key metrics
- `charts/` - all generated charts

## How to Run
Install required libraries:

```bash
pip install pandas matplotlib openpyxl
```

Run the project:

```bash
python ipl_analysis_project.py
```

## Explanation
This project uses Pandas for data cleaning and analysis, and Matplotlib for data visualization.
The project analyzes IPL match trends, team performance, toss impact, player performance, and venue distribution.