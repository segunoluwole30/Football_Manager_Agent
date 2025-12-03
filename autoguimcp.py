import asyncio
from pathlib import Path
from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
import pyautogui

client = AsyncOpenAI()

exe_path = Path(
    r"C:\Users\segun\OneDrive - Texas A&M University\Graduate School\Fall 2025\CSCE689(Programming LLMs)\Course Project\Football_Manager_Agent\venv\Scripts\mcp-pyautogui.exe"
)

@function_tool
def get_screen_resolution():
    """Returns the current screen width and height as a tuple."""
    return pyautogui.size()

async def main():
    async with MCPServerStdio(
        name="PyAutoGUI MCP Server",
        params={"command": str(exe_path), "args": []},
    ) as gui_server:

        coordinator = Agent(
            name="Coordinator",
            instructions=(
                "You are connected to the PyAutoGUI MCP tools and can use them to control the mouse and keyboard. "
                "You can also use the get_screen_resolution tool. "
            ),
            mcp_servers=[gui_server],
            tools=[get_screen_resolution],
            model="gpt-4.1-mini",  # vision-capable
        )

        screenshot_path = Path("squad.png")
        if not screenshot_path.exists():
            raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")

        # Upload image
        uploaded_file = await client.files.create(
            file=screenshot_path.open("rb"),
            purpose="vision"
        )


        # 🔹 Vision + Action combined input
        result = await Runner.run(
            coordinator,
            [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "return the coordinates of where Victor Valdes' name is located in the image"},
                        {"type": "input_image", "file_id": uploaded_file.id},
                    ],
                }
            ],
        )

        # result = await Runner.run(
        #     coordinator,
        #     "Take a screenshot ",
        # )

        print("\n✅ Final Action:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
