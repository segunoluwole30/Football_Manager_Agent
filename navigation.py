import time
import pyautogui

# def get_screen_resolution():
#     """Returns the current screen width and height as a tuple."""
#     return pyautogui.size()

# def take_screenshot(name="current_screen.png"):
#     """Captures the current game screen for debugging or verification."""
#     screenshot = pyautogui.screenshot()
#     screenshot.save(name)
#     return name

def main():
    print("⚽ Starting Football Manager navigation...")

    navigation_steps = [
        # ("Click the 'Home' button", (76, 27)),
        # ("Click the 'Tactics' button", (82, 264)),
        # ("Click the 'Quick Pick' button", (1611, 169)),
        # ("Click the top right button", (1807, 44)),
        # ("Click the button before 'Edit tactics button' in tactics page(e.g. where existing tactic is)", (524, 174)),
        # ("Hover over 'presets' button", (517, 292)),
        # ("Hover over 'Control Possession'", (795, 300)),
        # ("Hover over 4-2-3-1 DM in Control Possession", (1084, 300)),
        # ("Hover over 4-3-3 DM Wide in Control Possession", (1084, 350)),
        # ("Hover over 5-2-3 DM Wide in Control Possession", (1084, 400)),
        # ("Hover over 'Gegenpress'", (795, 350)),
        # ("Hover over 4-3-3 DM Wide in Gegenpress", (1072, 343)),
        # ("Hover over 4-2-3-1 DM AM Wide in Gegenpress", (1072, 385)),
        # ("Hover over 4-2-4 DM Wide in Gegenpress", (1072, 435)),
        # ("Hover over 'Tiki-Taka", (795,375)),
        # ("Hover over 4-3-3 DM Wide in Tiki-Taka", (1059, 388)),
        # ("Hover over 4-2-3-1 DM AM Wide in Tiki-Taka", (1059, 428)),
        # ("Hover over 5-2-3 DM Wide in Tiki-Taka", (1059, 468)),
        # ("Hover over 'Vertical Tiki-Taka", (795,400)),
        # ("Hover over 4-3-3 DM Wide in Vertical Tiki-Taka", (1078, 422)),
        # ("Hover over 4-4-2 Diamond Narrow in Vertical Tiki-Taka", (1078, 462)),
        # ("Hover over 4-2-3-1 DM AM Wide in vertical Tiki-Taka", (1078, 502)),
        # ("Hover over 'Wing Play", (795,450)),
        # ("Hover over 4-4-2 in Wing Play", (1048, 457)),
        # ("Hover over 4-3-3 DM Wide in Wing Play", (1048, 497)),
        # ("Hover over 5-2-3 DM Wide in Wing Play", (1048, 535)),
        # ("Hover over Route One", (795, 475)),
        # ("Hover over 4-4-2 in Route One", (1048, 497)),
        # ("Hover over 4-3-3 DM Wide in Route One", (1048, 535)),
        # ("Hover over 5-3-2 DM WB in Route One", (1048, 575)),
        # ("Hover over Fluid Counter Attack", (795, 520)),
        # ("Hover over 4-3-3 DM Wide in Fluid Counter Attack", (1065, 525)),
        # ("Hover over 4-2-3-1 DM Wide in Fluid Counter Attack", (1065, 565)),
        # ("Hover over 5-3-2 DM WB in Fluid Counter Attack", (1065, 605)),
        # ("Hover over Direct Counter Attack", (795, 555)),
        # ("Hover over 4-4-2 in Direct Counter Attack", (1048, 559)),
        # ("Hover over 4-3-3 DM Wide in Direct Counter Attack", (1048, 599)),
        # ("Hover over 5-3-2 DM WB in Direct Counter Attack", (1048, 639)),
        # ("Hover over Catenaccio", (795, 590)),
        # ("Hover over 5-2-3 DM Wide in Catenaccio", (1048, 599)),
        # ("Hover over 5-2-1-2 DM AM in Catenaccio", (1048, 639)),
        # ("Hover over 5-2-2-1 DM AM in Catenaccio", (1048, 679)),
        # ("Hover over Park the Bus", (795, 625)),
        # ("Hover over 4-4-2 in Park the Bus", (1048, 639)),
        # ("Hover over 4-2-4 DM Wide in Park the Bus", (1048, 679)),
        # ("Hover over 4-3-3 DM Wide in Park the Bus", (1048, 719)),

        ## Mentality ##
        # ("Click on Mentality", (352, 343)),
        # ("Hover over Very Defensive", (347, 398)),
        # ("Hover over Defensive", (357, 428)),
        # ("Hover over Cautious", (357, 468)),
        # ("Hover over Balanced", (357, 508)),
        # ("Hover over Positive", (357, 548)),
        # ("Hover over Attacking", (357, 588)),
        # ("Hover over Very Attacking", (357, 618)),

        # # ## Squad Reports ##
        # ("Click the 'Squad' button", (85,122)),
        # ("Click button next to PLAYERS", (385, 163)),
        # ("Click 'Reports' from dropdown", (416, 574)),
        # ("Click 'Quick Pick' button", (1622, 164)),
        # ("Screenshot the squad overview", None),
        # ("Hover over 'Squad overview' center", (960, 540)),
        # ("Scroll down the squad overview", -2000),
        # ("Screenshot the squad overview after scroll", None),
        # ("Scroll back up the squad overview", 2000),

        # ## Each Player Report ## 11 starters plus 12 substitutes = 23 players
        # ("Click on player in squad list", (446, 292)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 332)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (453, 370)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 408)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 443)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 478)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 515)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 555)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 595)),
        # ("Screenshot the player report", None), 
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 635)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 675)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 715)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 755)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 795)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 835)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 870)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 910)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 945)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),

        # ("Hover over 'Squad overview' center", (960, 540)),
        # ('Scroll down to see more players', -2000),

        # ("Click on next player in squad list", (446, 471)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 510)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 550)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 590)),
        # ("Screenshot the player report", None),
        # ("Click on back button", (233, 41)),
        # ("Click on next player in squad list", (446, 630)),
        # ("Screenshot the player report", None),


        # ## Squad Planner ##
        # ("Click the 'Squad Planner' button", (68, 173)),
        # ("Hover over 'Report' dropdown", (589, 96)),
        # ("Click Assistant Report", (605, 184)),
        # ("Hover over Strengths and Weaknesses", (1267, 235)),
        # ("Screenshot the Strengths and Weaknesses report", None),
        # ("Scroll down the Strengths and Weaknesses report", -2800),
        # ("Screenshot the Strengths and Weaknesses report", None),
        # ("Scroll down the Strengths and Weaknesses report", -2800),
        # ("Screenshot the Strengths and Weaknesses report", None),
        # ("Scroll down the Strengths and Weaknesses report", -2800),
        # ("Screenshot the Strengths and Weaknesses report", None),
        # ("Scroll down the Strengths and Weaknesses report", -2800),
        # ("Screenshot the Strengths and Weaknesses report", None),
        # ("Scroll down the Strengths and Weaknesses report", -2800),
        # ("Screenshot the Strengths and Weaknesses report", None),

        # ## Clean Slate Tactics ##
        # ("Click In Possession Tactics", (330, 387)),
        # ("Click Narrow Attacking Width", (490, 283)),
        # ("Click Fairly Narrow Attacking Width", (547, 294)),
        # ("Click ")

        ## Opponent Scouting Report ##
        # ("Hover over 'Data Hub' button", (90,309)),
        # ("Hover over 'Next Opponent' button", (677, 109)),
        # ("Hover over 'Ovierview' button", (701,138)),
        # ("Click 'Ovierview' button", (701,138)),
        ("Screenshot opponent overview", None),
        ("Click on first part of key findings", (1213, 686)),
        ("Screenshot opponent overview", None),
        (" Click Exit", (1495, 144)),
        ("Click on first part of key findings", (1213, 774)),
        ("Screenshot opponent overview", None),
        (" Click Exit", (1495, 144)),
        ("Click on first part of key findings", (1213, 862)),
        ("Screenshot opponent overview", None),
        (" Click Exit", (1495, 144)),
        ("Click on first part of key findings", (1213, 950)),
        ("Screenshot opponent overview", None),
        (" Click Exit", (1495, 144)),
        ("Hover inside key findings", ((1213, 950))),
        ("Scroll down", -2000),
        ("Click on first part of key findings", (1406, 946)),
        ("Screenshot opponent overview", None),
        (" Click Exit", (1495, 144)),

    ]

    for idx, (desc, coords) in enumerate(navigation_steps, start=1):
        if ("Click") in desc:
            print(f"\n🖱️ Step {idx}: {desc} at {coords}")
            pyautogui.click(coords[0], coords[1])
        elif ("Hover") in desc:
            print(f"\n🖱️ Step {idx}: {desc} at {coords}")
            pyautogui.moveTo(coords[0], coords[1], duration=0.2)
        elif ('Screenshot opponent') in desc:
             print(f"\n📸 Step {idx}: {desc}")
             pyautogui.screenshot(f"screenshots/opponent/screen_step_{idx}.png")
        elif ("Screenshot") in desc:
            print(f"\n📸 Step {idx}: {desc}")
            pyautogui.screenshot(f"screenshots/team/screen_step_{idx}.png")
  # optional debugging capture
            # time.sleep(1)  # wait for UI to update
        elif ("Scroll") in desc:
            print(f"\n🖱️ Step {idx}: {desc}")
            pyautogui.scroll(coords)
        time.sleep(1)  # wait for UI to update

    print("\n🏁 All navigation steps complete!")

if __name__ == "__main__":
    main()
