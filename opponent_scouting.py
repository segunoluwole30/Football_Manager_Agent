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


def capture_opponent_scouting(output_dir="screenshots/opponent/"):
    coords = UI_COORDS["opponent_scouting"]

    # First screenshot before clicking anything
    print("📸 Capturing initial opponent overview")
    pyautogui.screenshot(f"{output_dir}/opponent_1.png")

    # First 4 findings
    for i in range(1, 5):
        key = f"click_key_finding_{i}"
        x, y = coords[key]

        print(f"\n➡ Clicking key finding {i} at {x},{y}")
        click(x, y)

        print(f"📸 Screenshot key finding {i}")
        pyautogui.screenshot(f"{output_dir}/finding_{i}.png")

        print("⬅ Exiting")
        click(*coords["exit_button"])

    # Scroll down for more findings
    print("➡ Scrolling inside findings pane")
    hover(*coords["hover_inside_findings"])
    scroll(coords["scroll_down"])

    # Final key finding
    print("\n➡ Clicking last key finding")
    click(*coords["click_last_key_finding"])

    print("📸 Screenshot final finding")
    pyautogui.screenshot(f"{output_dir}/finding_last.png")

    print("⬅ Exiting final view")
    click(*coords["exit_button"])
