from openai import OpenAI
from pathlib import Path

client = OpenAI()

# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------
INPUT_FILE = "team_report_raw.txt"       # your long 3000+ word report
OUTPUT_FILE = "team_report_summary.txt"  # compact version
MODEL = "gpt-4.1"


# ------------------------------------------------------
# Summarization Template
# ------------------------------------------------------
SUMMARY_PROMPT = """
You are an expert football analyst.

You will receive a very long, unfiltered team analysis extracted from Football Manager screenshots.
Condense and structure it into a compact tactical evaluation that is easy for an LLM agent to use.

IMPORTANT RULES:
- Output must be under 350 words.
- Follow the template EXACTLY.
- Do not add new sections.
- Do not include any filler text.
- Be concise but tactically meaningful.

TEMPLATE:

[SQUAD SUMMARY]
- Overall squad quality:
- Style of play the attributes are suited for:
- Physical profile summary:
- Technical strengths:
- Technical weaknesses:

[KEY PLAYERS]
List only the 6 most tactically influential players:
- PlayerName: role, strengths, weaknesses, suitability.

[TACTICAL FIT]
- Best formations for this squad (pick 2):
- Pressing suitability (low/medium/high):
- Tempo suitability:
- Defensive line suitability:
- Transition strengths:
- Transition weaknesses:

[SQUAD ISSUES]
- Depth problems:
- Injury risks:
- Players out of position:
- Major tactical incompatibilities:

[RECOMMENDATION]
- Best overall tactical style to use:
- 1–2 alternative tactical styles:

REMEMBER:
The final answer must be UNDER 350 WORDS.
Return only the summary, nothing else.
"""


# ------------------------------------------------------
# Summarization Pipeline
# ------------------------------------------------------
def summarize_team_report():

    # Load long raw report
    raw_path = Path(INPUT_FILE)
    if not raw_path.exists():
        print(f"❌ Could not find {INPUT_FILE}")
        return

    long_text = raw_path.read_text(encoding="utf-8")

    print(f"Loaded {len(long_text.split())} words from {INPUT_FILE}")
    print("Sending to model for summarization...")

    # API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SUMMARY_PROMPT},
                    {"type": "text", "text": long_text}
                ]
            }
        ],
        max_tokens=800
    )

    # Extract text
    summary = response.choices[0].message.content

    # Save output
    Path(OUTPUT_FILE).write_text(summary, encoding="utf-8")
    print(f"✅ Summary written to {OUTPUT_FILE}")
    print("Done.")


# ------------------------------------------------------
# Run script
# ------------------------------------------------------
if __name__ == "__main__":
    summarize_team_report()
