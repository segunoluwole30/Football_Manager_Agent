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


# ----------------------------------------------------
#   SQUAD OVERVIEW + PLAYER REPORTS
# ----------------------------------------------------

def capture_squad_overview(output_dir="screenshots/team/"):
    coords = UI_COORDS["squad_reports"]

    print("➡ Clicking Squad button")
    click(*coords["squad_button"])

    print("➡ Opening Players dropdown")
    click(*coords["players_dropdown"])

    print("➡ Selecting Reports option")
    click(*coords["reports_dropdown_option"])

    print("➡ Quick Pick")
    click(*coords["quick_pick_button"])

    print("📸 Taking first squad overview screenshot")
    pyautogui.screenshot(f"{output_dir}/squad_overview_1.png")

    print("➡ Scrolling down squad overview")
    hover(*coords["overview_center"])
    scroll(coords["scroll_amount"])

    print("📸 Taking second overview screenshot")
    pyautogui.screenshot(f"{output_dir}/squad_overview_2.png")

    print("➡ Scrolling back up")
    scroll(coords["scroll_amount_up"])


def capture_all_player_reports(output_dir="screenshots/team/"):
    coords = UI_COORDS["player_reports"]

    for i in range(1, 24):  # 1 through 23
        #special scroll adjustment for player 19-23 to get remaining substitutes
        scroll_coords = UI_COORDS["squad_reports"]
        if (i == 19):
            hover(*scroll_coords["overview_center"])
            scroll(scroll_coords["scroll_amount"])
        key = f"player_{i}"
        if key not in coords:
            continue

        x, y = coords[key]
        print(f"\n➡ Clicking player {i} at {x}, {y}")
        click(x, y)

        print(f"📸 Screenshot player {i}")
        pyautogui.screenshot(f"{output_dir}/player_{i}.png")

        print("⬅ Clicking back")
        click(*coords["back_button"])

        time.sleep(0.5)
