from openai import OpenAI
from pathlib import Path

client = OpenAI()

# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------
INPUT_FILE = "opponent_report_raw.txt"        # long raw OCR-derived report
OUTPUT_FILE = "opponent_report_summary.txt"   # compressed tactical version
MODEL = "gpt-4.1"


# ------------------------------------------------------
# Summarization Template
# ------------------------------------------------------
OPPONENT_SUMMARY_PROMPT = """
You are an expert football tactical analyst. The text you will receive is a long,
unfiltered opponent scouting report extracted from Football Manager screenshots.

Your job is to convert it into a compact tactical summary that can be used by an
LLM agent to pick match tactics.

IMPORTANT RULES:
- Output must be under 300 words.
- Follow the template EXACTLY.
- Be concise: include only tactically relevant information.
- Do not add new sections.
- Do not include extra commentary.

TEMPLATE:

[TEAM OVERVIEW]
- Primary formations:
- Tactical style (describe in 1–2 lines):
- Pressing intensity:
- Defensive line:
- Possession tendencies:
- Transition habits:

[KEY PLAYERS]
List only the top 5 most influential players:
- PlayerName: position, strengths, weaknesses, threat level.

[STRENGTHS]
Bullet points summarizing tactical strengths.

[WEAKNESSES]
Bullet points summarizing weaknesses and areas to exploit.

[WHAT TO EXPECT IN MATCH]
- Expected attacking behavior:
- Expected defensive behavior:
- Expected speed of play:
- Key danger areas:

[HOW TO EXPLOIT THEM]
Give 4–6 bullets of specific tactical actions that will help beat this opponent.

Remember:
- Keep it under 300 words.
- Follow the sections exactly.
- Provide clear and actionable tactical insight.
"""


# ------------------------------------------------------
# Summarization Pipeline
# ------------------------------------------------------
def summarize_opponent_report():

    raw_path = Path(INPUT_FILE)
    if not raw_path.exists():
        print(f"❌ Missing {INPUT_FILE}. Cannot summarize.")
        return

    long_text = raw_path.read_text(encoding="utf-8")

    print(f"Loaded {len(long_text.split())} words from {INPUT_FILE}")
    print("Summarizing opponent scouting report...")

    # API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": OPPONENT_SUMMARY_PROMPT},
                    {"type": "text", "text": long_text}
                ]
            }
        ],
        max_tokens=600
    )

    summary = response.choices[0].message.content

    # Save final summary
    Path(OUTPUT_FILE).write_text(summary, encoding="utf-8")
    print(f"✅ Opponent summary saved to {OUTPUT_FILE}")

    # TRACK TOKENS HERE
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    print(f"💰 SUMMARY COST: Input: {input_tokens} | Output: {output_tokens}")
    
    # Return these values so agent_main can sum them
    return input_tokens, output_tokens


# ------------------------------------------------------
# Run script
# ------------------------------------------------------
if __name__ == "__main__":
    summarize_opponent_report()
