import time
import pyautogui
from ui_coordinates import UI_COORDS


def click(x, y, delay=1):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)


def hover(x, y, delay=1):
    pyautogui.moveTo(x, y)
    time.sleep(delay)


def scroll(amount, delay=1):
    pyautogui.scroll(amount)
    time.sleep(delay)


def capture_squad_planner(output_dir="screenshots/team/"):
    coords = UI_COORDS["squad_planner"]

    print("➡ Opening Squad Planner")
    click(*coords["planner_button"])

    print("➡ Opening Report dropdown")
    hover(*coords["report_dropdown"])
    time.sleep(1)

    print("➡ Selecting Assistant Report")
    click(*coords["assistant_report"])

    print("➡ Navigating to Strengths & Weaknesses")
    hover(*coords["strengths_weaknesses"])
    time.sleep(1)

    # Scroll multiple pages
    for i in range(1, 10):
        print(f"📸 Taking Strengths & Weaknesses screenshot {i}")
        pyautogui.screenshot(f"{output_dir}/planner_report_{i}.png")

        print("➡ Scrolling down")
        scroll(coords["scroll_amount"])
