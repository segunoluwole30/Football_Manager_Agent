import os
import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# -----------------------
# Encode image as base64
# -----------------------
def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# -----------------------
# Prompt template
# -----------------------
TEAM_REPORT_PROMPT = """
You are analyzing multiple Football Manager screenshots of squad reports.

Your job:
- Pull out attributes, roles, ages, contract info, key strengths, weaknesses.
- Summarize player-by-player.
- Produce a clean, structured text report.

Format:
[PLAYER NAME]
- Position:
- Key Attributes:
- Strengths:
- Weaknesses:
- Notes:

Keep it concise but accurate.
"""


# -----------------------
# Main extractor function
# -----------------------
def extract_from_images():
    IMAGE_DIR = Path("screenshots/team")
    OUTPUT_FILE = Path("team_report_raw.txt")

    images = sorted([p for p in IMAGE_DIR.iterdir() if p.suffix.lower() in [".png", ".jpg"]])
    print(f"Found {len(images)} images.\n")

    if not images:
        print("No images found. Exiting.")
        return

    BATCH_SIZE = 4
    outputs = []

    for i in range(0, len(images), BATCH_SIZE):
        batch = images[i:i + BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1} with {len(batch)} images...")

        # Build message content
        content = [{"type": "text", "text": TEAM_REPORT_PROMPT}]

        for img_path in batch:
            print(f"Encoding {img_path.name} ...")
            base64_img = encode_image(img_path)
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_img}"
                    }
                }
            )

        # Call GPT-4.1 Vision
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": content}
            ]
        )

        # FIXED LINE
        text = response.choices[0].message.content
        outputs.append(text + "\n\n")


    # Write final report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(outputs)

    print(f"\nDone! Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_from_images()
