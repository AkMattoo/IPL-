# Quick Start Guide

## Run the Complete Analysis in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Analysis Script
```bash
cd src
python ipl_analytics.py
```

This will:
- Load all datasets
- Run all 7 analyses
- Save results to `reports/analysis_results/`
- Print summary statistics

### Step 3: Explore the Notebook
```bash
jupyter notebook notebooks/01_ipl_analysis.ipynb
```

Interactive exploration with visualizations!

## Expected Output
```
Running Toss Impact Analysis...
Finding Best Batsman Per Season...
Finding Best Bowler Per Season...
Analyzing Home vs Away Performance...
Analyzing Playoff Conversion...
Analyzing Pitch Evolution...
Analyzing Team Success...
Building Match Predictor...

✅ Analysis complete! Results saved to reports/analysis_results/
   Match Predictor Accuracy: 0.964
   Top Feature: team1_strength
```

## File Outputs
All outputs are saved in:
- `reports/analysis_results/` — CSV files
- `reports/figures/` — PNG visualizations
