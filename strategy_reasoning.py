import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are an expert football tactical analyst for Football Manager. 
You must output a tactical plan in JSON format.

### RULE 1: CONSISTENCY IS CRITICAL
You must select a **Preset** and a **Formation** that are compatible. 
In the list below, formations are grouped by their required Preset.
You CANNOT mix them (e.g., you cannot use a 'cp_' formation with a 'fluid_counter' preset).

### AVAILABLE TACTICS (Use these keys exactly)

1. PRESET: "control_possession"
   - Formations: "cp_4231_dm", "cp_433_dm_wide", "cp_523_dm_wide"

2. PRESET: "gegenpress"
   - Formations: "gp_433_dm_wide", "gp_4231_dm_am_wide", "gp_424_dm_wide"

3. PRESET: "tiki_taka"
   - Formations: "tt_433_dm_wide", "tt_4231_dm_am_wide", "tt_523_dm_wide"

4. PRESET: "vertical_tiki_taka"
   - Formations: "vtt_433_dm_wide", "vtt_442_diamond_narrow", "vtt_4231_dm_am_wide"

5. PRESET: "wing_play"
   - Formations: "wp_442", "wp_433_dm_wide", "wp_523_dm_wide"

6. PRESET: "fluid_counter"
   - Formations: "fc_433_dm_wide", "fc_4231_dm_wide", "fc_532_dm_wb" 
   

7. PRESET: "direct_counter"
   - Formations: "dc_442", "dc_433_dm", "dc_532_dm_wb"

8. PRESET: "route_one"
   - Formations: "ro_442", ro_433_dm_wide, "ro_532_dm_wb"

9. PRESET: "park_the_bus"
   - Formations: "ptb_424_dm_wide", "ptb_442", "ptb_433_dm_wide"

### INSTRUCTIONS
1. Analyze the USER TEAM REPORT and OPPONENT REPORT.
2. Select the best **Preset** from the list above.
3. Select a **Formation** FROM THAT SPECIFIC PRESET GROUP ONLY.
4. Choose a **Mentality**: ["very_defensive", "defensive", "cautious", "balanced", "positive", "attacking", "very_attacking"]

### OUTPUT FORMAT (JSON ONLY)
{
  "preset": "exact_preset_key_from_above",
  "formation": "exact_formation_key_from_above",
  "mentality": "selected_mentality",
  "use_quick_pick": true,
  "reasoning": "Explain why this specific combination beats the opponent."
}
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
