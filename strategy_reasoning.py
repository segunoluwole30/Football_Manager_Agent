import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are an expert football tactical analyst. 
You recommend tactics based on:

1. The user's team strengths and weaknesses.
2. The opponent's scouting report.
3. Football Manager meta knowledge.
4. The available tactics listed below (MUST use):
   - Presets:
       - control_possession
       - gegenpress
       - tiki_taka
       - vertical_tiki_taka
       - wing_play
       - route_one
       - fluid_counter
       - direct_counter
       - catenaccio
       - park_the_bus

   - Formations (examples):
       - cp_4231_dm, cp_433_dm_wide, cp_523_dm_wide
       - gp_433_dm_wide, gp_4231_dm_am_wide, gp_424_dm_wide
       - tt_433_dm_wide, tt_4231_dm_am_wide, tt_523_dm_wide
       - vtt_433_dm_wide, vtt_442_diamond_narrow, vtt_4231_dm_am_wide
       - wp_442, wp_433_dm_wide, wp_523_dm_wide
       - etc.

You MUST output a JSON dict with keys:
{
  "preset": string,
  "formation": string,
  "mentality": string,
  "use_quick_pick": true,
  "reasoning": string
}

Mentailty must be one of:
["very_defensive", "defensive", "cautious", "balanced", "positive", "attacking", "very_attacking"]
"""

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def generate_tactic_plan(team_path="team_report_summary.txt",
                         opponent_path="opponent_report_summary.txt"):
    team_data = load_file(team_path)
    opponent_data = load_file(opponent_path)

    prompt = f"""
TEAM REPORT:
{team_data}

OPPONENT REPORT:
{opponent_data}

Based on these two reports, output the JSON tactic plan.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    )

    content = response.choices[0].message.content

    try:
        plan = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("LLM did not produce valid JSON:\n" + content)

    return plan
