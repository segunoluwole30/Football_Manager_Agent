import time
import os
from pathlib import Path

# --- Import your modules ---
# 1. Capture
from squad_reports import capture_squad_overview, capture_all_player_reports
from squad_planner import capture_squad_planner
from opponent_scouting import capture_opponent_scouting

# 2. Extract (Vision)
from opponent_image_extractor import extract_opponent_images
from team_image_extractor import extract_from_images  # Assuming 'extract_from_images' is the correct function name

# 3. Summarize
from opponent_summarizer import summarize_opponent_report
from summarize_team_report import summarize_team_report

# 4. Reason & Execute
from strategy_reasoning import generate_tactic_plan
from apply_tactics import apply_tactic_plan

def ensure_directories():
    Path("screenshots/team").mkdir(parents=True, exist_ok=True)
    Path("screenshots/opponent").mkdir(parents=True, exist_ok=True)

def countdown(seconds, message):
    print(f"\n{message}")
    for i in range(seconds, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)
    print("\nGo!")

def run_agent(skip_capture=False, skip_team_report=False):
    grand_total_input = 0
    grand_total_output = 0
    ensure_directories()

    # --- PHASE 1: DATA COLLECTION ---
    if not skip_capture:
        print("==========================================")
        print("       PHASE 1: VISUAL DATA COLLECTION    ")
        print("==========================================")
        countdown(5, "⚠️  Please switch to the Football Manager window immediately!")
        
        # 1. Team Data (CONDITIONAL)
        if not skip_team_report:
            print("\n📸 Capturing Squad Overview...")
            capture_squad_overview()
            
            print("\n📸 Capturing All Player Reports (Optional but included)...")
            # Note: Player reports take a long time, maybe make this optional
            capture_all_player_reports()
            
            print("\n📸 Capturing Squad Planner...")
            capture_squad_planner()
        else:
            print("\n⏭️ Skipping Team Report Capture. Using existing team_report_summary.txt.")

        print("Switch to Next opponent Screen")
        time.sleep(10)  # Short break between captures to allow for navigation to 

        # 2. Opponent Data (ALWAYS RUN on match day)
        print("\n📸 Capturing Opponent Scouting...")
        capture_opponent_scouting()
        
        print("\n✅ Capture complete. You can relax now.")
    
    # --- PHASE 2: PROCESSING (OCR & ANALYSIS) ---
    print("\n==========================================")
    print("       PHASE 2: ANALYZING REPORTS         ")
    print("==========================================")
    
    # Opponent Processing (ALWAYS RUN)
    print("🧠 Extracting text from Opponent images (GPT-4 Vision)...")
    in_tok, out_tok = extract_opponent_images() 
    grand_total_input += in_tok
    grand_total_output += out_tok
    print("📝 Summarizing Opponent Report...")
    in_tok, out_tok = summarize_opponent_report()
    grand_total_input += in_tok
    grand_total_output += out_tok
    
    # Team Processing (CONDITIONAL)
    if not skip_team_report:
        print("🧠 Extracting text from Team images (GPT-4 Vision)...")
        in_tok, out_tok = extract_from_images()
        grand_total_input += in_tok
        grand_total_output += out_tok

        print("📝 Summarizing Team Report...")
        in_tok, out_tok = summarize_team_report()
        grand_total_input += in_tok
        grand_total_output += out_tok
    else:
        print("⏭️ Skipping Team Report Extraction and Summarization. Using existing team summary.")


    # --- PHASE 3: STRATEGY GENERATION ---
    print("\n==========================================")
    print("       PHASE 3: TACTICAL PLANNING         ")
    print("==========================================")
    
    try:
        # Strategy reasoning uses both summaries, one of which is the existing team summary if skipped
        plan, in_tok, out_tok = generate_tactic_plan()
        grand_total_input += in_tok
        grand_total_output += out_tok
        print("\n🎯 GENERATED TACTICAL PLAN:")
        print(f"   Preset: {plan.get('preset')}")
        print(f"   Formation: {plan.get('formation')}")
        print(f"   Mentality: {plan.get('mentality')}")
        print(f"   Reasoning: {plan.get('reasoning')[:100]}...") # Print first 100 chars
    except Exception as e:
        print(f"❌ Error generating plan: {e}")
        return

    # --- PHASE 4: EXECUTION ---
    print("\n==========================================")
    print("       PHASE 4: EXECUTING TACTICS         ")
    print("==========================================")
    
    confirm = input("\nReady to apply tactics in FM? (y/n): ")
    if confirm.lower() == 'y':
        countdown(5, "⚠️  Switch back to FM! Applying tactics...")
        apply_tactic_plan(plan)
        print("\n✅ Mission Complete. Good luck with the match!")
    else:
        print("\n🛑 Execution aborted.")
    # --- FINAL COST REPORT ---
    print("\n==========================================")
    cost_input = (grand_total_input / 1_000_000) * 3.00
    cost_output = (grand_total_output / 1_000_000) * 12.00
    total_cost = cost_input + cost_output

    print(f"\n💵 MATCH COST ANALYSIS:")
    print(f"   Total Input Tokens: {grand_total_input}")
    print(f"   Total Output Tokens: {grand_total_output}")
    print(f"   Estimated Cost: ${total_cost:.4f}")

if __name__ == "__main__":
    # --- How to run ---
    # 1. Full Refresh (run at the start of a new season/after major transfers)
    run_agent(skip_capture=False, skip_team_report=False)
    
    # 2. Match Day Mode (default - only refresh opponent data)
    # run_agent(skip_capture=False, skip_team_report=True)

    # 3. Debug Mode (skip all captures, only re-run LLM logic based on existing files)
    # run_agent(skip_capture=True, skip_team_report=True)