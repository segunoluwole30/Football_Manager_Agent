import time
import pyautogui
from ui_coordinates import UI_COORDS


# ---------------------------------------------------
# Basic mouse helpers
# ---------------------------------------------------

def click(section, key, delay=1):
    """Move cursor to (x,y) and left click."""
    x, y = UI_COORDS[section][key]
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(delay)


def hover(section, key, delay=1):
    """Move cursor to (x,y) without clicking."""
    x, y = UI_COORDS[section][key]
    pyautogui.moveTo(x, y)
    time.sleep(delay)


# ---------------------------------------------------
# High-level actions
# ---------------------------------------------------

def apply_preset_tactic(preset_key: str, formation_key: str):
    """
    Change tactics by:
    1. Clicking the existing tactic slot
    2. Hovering over the new preset
    3. Clicking the formation under that preset
    """
    print(f"[Tactics] Changing to preset: {preset_key}, formation: {formation_key}")

    # Step 1: Click existing tactic slot
    click("tactics", "existing_tactic_slot", delay=2)

    hover("presets_menu", "open_presets", delay=1)

    # Step 2: Hover over preset category
    hover("presets_menu", preset_key, delay=2)

    # Step 3: Click on formation inside that preset
    click("presets_menu", formation_key, delay=2)


def apply_mentality(mentality_key: str):
    """
    Change mentality by:
    1. Clicking on 'open_mentality'
    2. Clicking the selected mentality option
    """
    print(f"[Tactics] Setting mentality to: {mentality_key}")

    # Step 1: Open mentality dropdown
    click("mentality", "open_mentality", delay=1)

    # Step 2: Click desired mentality
    click("mentality", mentality_key, delay=1)


def quick_pick():
    """Clicks the Quick Pick button."""
    print("[Tactics] Applying Quick Pick")
    click("tactics", "quick_pick_button", delay=1)


# ---------------------------------------------------
# Unified entry point for the LLM decision
# ---------------------------------------------------

def apply_tactic_plan(plan: dict):
    """
    plan structure example:
    {
        "preset": "gegenpress",
        "formation": "gp_433_dm_wide",
        "mentality": "positive",
        "use_quick_pick": True
    }
    """

    preset = plan.get("preset")
    formation = plan.get("formation")
    mentality = plan.get("mentality")
    use_quick = plan.get("use_quick_pick", True)

    # Apply preset tactic + formation
    if preset and formation:
        apply_preset_tactic(preset, formation)

    # Apply mentality
    if mentality:
        apply_mentality(mentality)

    # Optional: Quick Pick
    if use_quick:
        quick_pick()

    print("[Tactics] Tactic plan applied successfully.")
