import os
import sys
import json
import time
import random
import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4

# ---------------------------
# CONFIGURATION & CONSTANTS
# ---------------------------
# Default version if version.txt is missing
DEFAULT_VERSION = "0.5.0"

# URL to your remote version.json file (use the raw URL)
VERSION_JSON_URL = "https://raw.githubusercontent.com/razberi-py/Auto-updater/main/version.json"

# ---------------------------
# LOCAL VERSION FUNCTIONS
# ---------------------------
def get_local_version():
    """
    Reads the current version from 'version.txt' in the current directory.
    If the file is missing or unreadable, returns the DEFAULT_VERSION.
    """
    try:
        with open("version.txt", "r", encoding="utf-8") as f:
            version = f.read().strip()
            if version:
                return version
    except Exception:
        pass
    return DEFAULT_VERSION

# ---------------------------
# HELPER FUNCTIONS FOR JSON PARSING
# ---------------------------
def get_clean_json(text):
    """
    If the downloaded text isn't valid JSON, try stripping out HTML using BeautifulSoup.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        soup = BeautifulSoup(text, 'html.parser')
        cleaned_text = soup.get_text().strip()
        return json.loads(cleaned_text)

def fetch_update_info():
    """
    Fetches and returns the update information from VERSION_JSON_URL.
    Returns the parsed JSON data (a dict) on success, or None on failure.
    """
    try:
        response = requests.get(VERSION_JSON_URL)
        if response.status_code != 200:
            print("Could not check for updates (HTTP status:", response.status_code, ")")
            return None

        content = response.text
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print("Initial JSON parse failed; attempting to clean HTML with BeautifulSoup...")
            data = get_clean_json(content)
        return data
    except Exception as e:
        print("Update check failed:", e)
        return None

# ---------------------------
# UPDATE PROCESS FUNCTIONS
# ---------------------------
def download_updates(files):
    """
    Downloads updated files as specified in the files list.
    Backs up the current file (if it exists) before replacing it.
    After updating, the script restarts.
    """
    for file_info in files:
        file_name = file_info.get("name")
        file_url = file_info.get("url")
        if not file_name or not file_url:
            print("Skipping a file update entry due to missing information.")
            continue

        try:
            print(f"Downloading updated version of '{file_name}' from {file_url} ...")
            file_response = requests.get(file_url)
            if file_response.status_code != 200:
                print(f"Failed to download {file_name} (HTTP status: {file_response.status_code})")
                continue
            updated_code = file_response.text
            # Backup current file if it exists
            if os.path.exists(file_name):
                backup_file = file_name + ".bak"
                os.rename(file_name, backup_file)
                print(f"Backed up the old {file_name} to {backup_file}")
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(updated_code)
            print(f"{file_name} updated successfully.")
        except Exception as e:
            print(f"Update failed for {file_name}:", e)
    
    print("\nAll available updates have been applied. Restarting the tool in 3 seconds...")
    time.sleep(3)
    os.execv(sys.executable, [sys.executable] + sys.argv)

def update_menu():
    """
    Checks for updates and then presents the user with options:
    - Update now
    - Display debug information (the raw update JSON)
    - Cancel
    """
    print("Checking for updates...")
    update_info = fetch_update_info()
    if update_info is None:
        input("Press Enter to return to the main menu...")
        return

    remote_version = update_info.get("latest_version", DEFAULT_VERSION)
    changelog = update_info.get("changelog", "No changelog provided.")
    files_to_update = update_info.get("files", [])
    local_version = get_local_version()

    if remote_version == local_version:
        print("You are running the latest version.")
        input("Press Enter to return to the main menu...")
        return

    print(f"\nUpdate available!")
    print(f"Local version: {local_version}")
    print(f"Latest version: {remote_version}\n")
    print("Changelog:")
    print(changelog)
    print("\nFiles to update:")
    for f in files_to_update:
        print(" -", f.get("name", "unknown"))
    print("\n")
    
    # Present options to the user
    while True:
        print("Options:")
        print("[U]pdate now")
        print("[D]isplay debug info")
        print("[C]ancel")
        choice = input("Choose an option (U/D/C): ").lower().strip()
        if choice == "u":
            download_updates(files_to_update)
            break  # Should not reach here as download_updates restarts the script.
        elif choice == "d":
            print("\n--- Debug Information ---")
            print(json.dumps(update_info, indent=2))
            print("--- End Debug Information ---\n")
        elif choice == "c":
            print("Update canceled.")
            break
        else:
            print("Invalid choice. Please select U, D, or C.")

    input("Press Enter to return to the main menu...")

# ---------------------------
# GAME FUNCTIONS
# ---------------------------
def blackjack():
    print("\n=== Blackjack ===")
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)
    player_cards = [deck.pop(), deck.pop()]
    dealer_cards = [deck.pop(), deck.pop()]
    print("Your cards:", player_cards, "=> total:", sum(player_cards))
    print("Dealer shows:", dealer_cards[0])
    decision = input("Do you want to hit? (y/n): ").lower()
    while decision == "y" and sum(player_cards) < 21:
        player_cards.append(deck.pop())
        print("Your cards:", player_cards, "=> total:", sum(player_cards))
        if sum(player_cards) > 21:
            print("Bust! You lose.")
            input("Press Enter to return to the main menu...")
            return
        decision = input("Hit again? (y/n): ").lower()
    print("Dealer's cards:", dealer_cards, "=> total:", sum(dealer_cards))
    while sum(dealer_cards) < 17:
        dealer_cards.append(deck.pop())
        print("Dealer draws... cards now:", dealer_cards, "=> total:", sum(dealer_cards))
    player_total = sum(player_cards)
    dealer_total = sum(dealer_cards)
    if dealer_total > 21 or player_total > dealer_total:
        print("You win!")
    elif player_total == dealer_total:
        print("Push!")
    else:
        print("Dealer wins!")
    input("Press Enter to return to the main menu...")

def coin_flip():
    print("\n=== Coin Flip ===")
    result = random.choice(["Heads", "Tails"])
    print("The coin lands on:", result)
    input("Press Enter to return to the main menu...")

def dice_roll():
    print("\n=== Dice Roll ===")
    result = random.randint(1, 6)
    print("You rolled a:", result)
    input("Press Enter to return to the main menu...")

def slot_machine():
    print("\n=== Slot Machine ===")
    symbols = ["Cherry", "Lemon", "Bell", "Seven"]
    spin = [random.choice(symbols) for _ in range(3)]
    print(" | ".join(spin))
    if spin.count(spin[0]) == 3:
        print("Jackpot! You win!")
    else:
        print("Better luck next time.")
    input("Press Enter to return to the main menu...")

def roulette():
    print("\n=== Roulette ===")
    result = random.randint(0, 36)
    color = "Red" if result % 2 == 0 else "Black"  # Simplified logic
    print(f"The ball lands on {result} ({color})")
    input("Press Enter to return to the main menu...")

# ---------------------------
# MAIN MENU & PROGRAM LOOP
# ---------------------------
def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        # Read the local version from version.txt every time the menu is shown.
        local_version = get_local_version()
        print("=== Python Casino ===")
        print("Version:", local_version)
        print("\nSelect a game:")
        print("1. Blackjack")
        print("2. Coin Flip")
        print("3. Dice Roll")
        print("4. Slot Machine")
        print("5. Roulette")
        print("6. Check for Updates")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            blackjack()
        elif choice == "2":
            coin_flip()
        elif choice == "3":
            dice_roll()
        elif choice == "4":
            slot_machine()
        elif choice == "5":
            roulette()
        elif choice == "6":
            update_menu()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # No automatic update check at startup; update check is done on demand.
    main_menu()
