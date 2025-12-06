import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import math

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
DATA_DIR = Path("evaluation")
AGENT_FILE = DATA_DIR / "agent.csv"
USER_FILE = DATA_DIR / "user.csv"
OUTPUT_DIR = Path("evaluation_results")  # Where to save plots/reports

def load_data():
    """
    Loads agent and user data from the evaluation directory.
    Assumes headers are now correct in both files.
    """
    if not AGENT_FILE.exists() or not USER_FILE.exists():
        print(f"❌ Error: Could not find files in {DATA_DIR}")
        print(f"   Looking for: {AGENT_FILE} and {USER_FILE}")
        return None, None

    print(f"📂 Loading data from {DATA_DIR}...")
    
    # Load CSVs (Standard load since headers are fixed)
    agent = pd.read_csv(AGENT_FILE)
    user = pd.read_csv(USER_FILE)
    
    # Standardize string columns for accurate merging
    # Trimming whitespace is critical for matching names like "Arsenal v Liverpool "
    for df in [agent, user]:
        df['match'] = df['match'].astype(str).str.strip()
        df['result'] = df['result'].astype(str).str.strip().str.upper()
        
    return agent, user

def calculate_points(result):
    """Converts W/D/L to 3/1/0 points."""
    if result == 'W': return 3
    if result == 'D': return 1
    return 0

def cohens_d(x, y):
    """Calculates Cohen's d (effect size) between two distributions."""
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2: return 0
    dof = nx + ny - 2
    pool_std = math.sqrt(((nx-1)*x.std()**2 + (ny-1)*y.std()**2) / dof)
    if pool_std == 0: return 0
    return (x.mean() - y.mean()) / pool_std

def main():
    # 1. Setup
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 2. Load Data
    agent_df, user_df = load_data()
    if agent_df is None: return

    # 3. Pre-process Metrics
    for df in [agent_df, user_df]:
        df['points'] = df['result'].apply(calculate_points)
        # Ensure numeric columns are strictly floats
        for c in ['goals_for', 'xg_for', 'possession']:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # 4. Merge for Paired Analysis (Compare specific matches)
    # We use an inner join to only compare matches that exist in BOTH files
    merged = pd.merge(
        agent_df[['match', 'goals_for', 'xg_for', 'points', 'result']], 
        user_df[['match', 'goals_for', 'xg_for', 'points', 'result']], 
        on='match', 
        suffixes=('_agent', '_user')
    )
    
    if merged.empty:
        print("❌ Error: No matching match names found between files. Check spelling in 'match' column.")
        return

    # 5. Calculate Aggregates
    stats = {
        'Matches Played':   len(merged),
        'Agent Total Pts':  merged['points_agent'].sum(),
        'User Total Pts':   merged['points_user'].sum(),
        'Agent Mean Goals': merged['goals_for_agent'].mean(),
        'User Mean Goals':  merged['goals_for_user'].mean(),
        'Agent Mean xG':    merged['xg_for_agent'].mean(),
        'User Mean xG':     merged['xg_for_user'].mean(),
    }
    
    # Effect sizes
    d_goals = cohens_d(merged['goals_for_agent'], merged['goals_for_user'])
    d_xg = cohens_d(merged['xg_for_agent'], merged['xg_for_user'])

    # 6. Generate Text Report
    report = []
    report.append("=== 📊 TACTICAL EVALUATION REPORT ===")
    report.append(f"Data Source: {DATA_DIR}")
    report.append(f"Matches Compared: {stats['Matches Played']}")
    
    report.append(f"\n[🏆 POINTS COMPARISON]")
    report.append(f"Agent: {stats['Agent Total Pts']} pts")
    report.append(f"User:  {stats['User Total Pts']} pts")
    diff = stats['Agent Total Pts'] - stats['User Total Pts']
    report.append(f"Diff:  {'+' if diff > 0 else ''}{diff} pts")
    
    report.append(f"\n[⚽ GOALS PER MATCH]")
    report.append(f"Agent: {stats['Agent Mean Goals']:.2f}")
    report.append(f"User:  {stats['User Mean Goals']:.2f}")
    report.append(f"Effect Size (Cohen's d): {d_goals:.2f} ({( 'Negligible' if abs(d_goals)<0.2 else 'Small' if abs(d_goals)<0.5 else 'Medium' if abs(d_goals)<0.8 else 'Large' )})")

    report.append(f"\n[📈 EXPECTED GOALS (xG)]")
    report.append(f"Agent: {stats['Agent Mean xG']:.2f}")
    report.append(f"User:  {stats['User Mean xG']:.2f}")
    
    report.append("\n[🆚 HEAD-TO-HEAD RESULTS]")
    report.append(f"{'Match':<30} | {'A_Res':<5} {'U_Res':<5} | {'A_G':<3} {'U_G':<3}")
    report.append("-" * 60)
    for _, row in merged.iterrows():
        match_name = row['match'][:29]
        report.append(f"{match_name:<30} | {row['result_agent']:<5} {row['result_user']:<5} | {row['goals_for_agent']:<3} {row['goals_for_user']:<3}")

    # Print and Save Report
    report_text = "\n".join(report)
    print(report_text)
    
    report_path = OUTPUT_DIR / "evaluation_summary.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    # 7. Generate Visualizations
    print(f"\n🎨 Generating plots in {OUTPUT_DIR}...")
    
    # Plot 1: Points Bar Chart
    plt.figure(figsize=(10, 6))
    x = np.arange(len(merged))
    width = 0.35
    plt.bar(x - width/2, merged['points_agent'], width, label='Agent', color='#4c72b0') # Blue
    plt.bar(x + width/2, merged['points_user'], width, label='User', color='#c44e52')   # Red
    plt.ylabel('Points (3=Win, 1=Draw, 0=Loss)')
    plt.title('Points Comparison per Match')
    plt.xticks(x, [m.split(' v ')[0] for m in merged['match']], rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'comparison_points.png')
    plt.close()
    
    # Plot 2: xG Performance
    plt.figure(figsize=(8, 6))
    plt.plot(merged['match'], merged['xg_for_agent'], marker='o', label='Agent xG', color='#4c72b0')
    plt.plot(merged['match'], merged['xg_for_user'], marker='x', linestyle='--', label='User xG', color='#c44e52')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Expected Goals (xG)')
    plt.title('xG Performance Trend')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'comparison_xg_trend.png')
    plt.close()

    print(f"✅ Done. Results saved to folder: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()