import asyncio
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI

# Initialize OpenAI async client
client = AsyncOpenAI()

# Path to your local MCP server executable
exe_path = Path(
    r"C:\Users\segun\OneDrive - Texas A&M University\Graduate School\Fall 2025\CSCE689(Programming LLMs)\Course Project\Football_Manager_Agent\venv\Scripts\mcp-pyautogui.exe"
)

async def main():
    # Start the MCP PyAutoGUI server
    async with MCPServerStdio(
        name="PyAutoGUI MCP Server",
        params={"command": str(exe_path), "args": []},
    ) as gui_server:

        # 🧠 Vision agent — analyzes screenshots
        vision_agent = Agent(
            name="Vision Analyzer",
            instructions=(
                "Analyze screenshots and describe what's visible. "
                "Identify any buttons, text, or UI components relevant to a football management game."
            ),
            model="gpt-4.1-mini",  # modern, efficient vision-capable model
        )

        # 🤖 Coordinator agent — interacts with the PyAutoGUI MCP
        coordinator = Agent(
            name="Coordinator",
            instructions="Coordinate between the vision and GUI agents to achieve the user's goal.",
            mcp_servers=[gui_server],
        )

        # 📸 Load screenshot
        screenshot_path = Path("screen.png")
        if not screenshot_path.exists():
            raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")

        # 🔼 Upload screenshot to OpenAI
        uploaded_file = await client.files.create(
            file=screenshot_path.open("rb"),
            purpose="vision"
        )

        # 🧩 Request vision model analysis
        vision_response = await client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Describe what is visible in this screenshot."},
                        {"type": "input_image", "file_id": uploaded_file.id},
                    ],
                }
            ],
        )

        # 📝 Extract vision output
        analysis_text = vision_response.output[0].content[0].text
        print("\n🧠 Vision Analysis:")
        print(analysis_text)

        #🖱️ Use PyAutoGUI through Coordinator (if desired)
        follow_up = f"Click on the X button: {analysis_text}"
        action_result = await Runner.run(coordinator, follow_up)
        print("\n✅ Final Action:", action_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
