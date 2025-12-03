import json
from pathlib import Path
import sys
from openai import OpenAI

client = OpenAI()  # Assumes OPENAI_API_KEY is set in environment


def load_text(path: Path) -> str:
    if not path.exists():
        print(f"❌ Missing file: {path}")
        sys.exit(1)
    return path.read_text()


def build_prompt(team_text: str, opponent_text: str) -> str:
    return f"""
You are an expert football tactics analyst specializing in Football Manager.

Your job is to analyze:
1. Our team report
2. The opponent scouting report

Then recommend:
- Optimal formation (e.g., 4-2-3-1, 4-3-3, 3-5-2)
- Mentality (Balanced, Positive, Cautious, Attacking, etc.)
- Key tactical instructions (5–8 bullet points)
- A short explanation why this setup is optimal

Return ONLY a JSON object with the following structure:

{{
  "formation": "...",
  "mentality": "...",
  "instructions": ["...", "..."],
  "reasoning": "..."
}}

-----------------------------
OUR TEAM REPORT:
{team_text}

-----------------------------
OPPONENT SCOUTING REPORT:
{opponent_text}

Generate the best tactical setup.
"""


def generate_tactical_plan(team_text: str, opponent_text: str) -> dict:
    """Call the LLM to produce structured JSON output."""
    prompt = build_prompt(team_text, opponent_text)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You analyze football tactics and generate structured JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    text_output = response.choices[0].message.content

    try:
        plan = json.loads(text_output)
        return plan
    except json.JSONDecodeError:
        print("❌ Model returned invalid JSON:\n", text_output)
        raise


def save_plan(plan: dict, opponent_name: str):
    out_dir = Path("plans")
    out_dir.mkdir(exist_ok=True)

    out_path = out_dir / f"{opponent_name.lower().replace(' ', '_')}_plan.json"

    with out_path.open("w") as f:
        json.dump(plan, f, indent=4)

    print(f"\n✅ Tactical plan saved to: {out_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python tactics_reasoning.py <opponent_name>")
        sys.exit(1)

    opponent_name = sys.argv[1]

    # Paths
    team_path = Path("team_report_summary.txt")
    opponent_path = Path(f"scouting_report_{opponent_name}.txt")

    print("📥 Loading input files...")
    team_text = load_text(team_path)
    opponent_text = load_text(opponent_path)

    print("\n🧠 Generating tactical plan...")
    plan = generate_tactical_plan(team_text, opponent_text)

    print("\n📋 Tactical Plan:")
    print(json.dumps(plan, indent=4))

    save_plan(plan, opponent_name)


if __name__ == "__main__":
    main()
