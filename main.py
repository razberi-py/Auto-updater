import os
import sys
import json
import time
import random
import requests  # install via: pip install requests

# ---------------------------
# CONFIGURATION & CONSTANTS
# ---------------------------
CURRENT_VERSION = "1.0.0"

# URL to your version file on GitHub (raw content)
# Replace these with your GitHub details and branch as needed.
VERSION_JSON_URL = "https://raw.githubusercontent.com/your-username/your-repo-name/main/version.json"

# URL to the updated script (if you want to auto-update)
UPDATED_SCRIPT_URL = "https://raw.githubusercontent.com/your-username/your-repo-name/main/casino.py"

# ---------------------------
# VERSION CHECK, CHANGELOG & AUTO-UPDATER USING JSON
# ---------------------------
def check_for_update():
    """
    Checks a JSON file on GitHub for the latest version.
    Displays the changelog if an update is available.
    """
    print("Checking for updates...")
    try:
        response = requests.get(VERSION_JSON_URL)
        if response.status_code != 200:
            print("Could not check for updates (HTTP status:", response.status_code, ")")
            return

        # Parse the JSON file. It should contain keys like "latest_version" and "changelog".
        data = response.json()
        latest_version = data.get("latest_version", CURRENT_VERSION)
        changelog = data.get("changelog", "No changelog provided.")

        if latest_version != CURRENT_VERSION:
            print(f"\nUpdate available!")
            print(f"Current version: {CURRENT_VERSION}")
            print(f"Latest version: {latest_version}\n")
            print("Changelog:")
            print(changelog)
            print("\n")
            do_update = input("Do you want to update now? (y/n): ").lower()
            if do_update == "y":
                download_update()
            else:
                print("Update canceled by user.")
        else:
            print("You are running the latest version.")
    except Exception as e:
        print("Update check failed:", e)

def download_update():
    """
    Downloads the updated script from a specified URL and replaces the current file.
    """
    try:
        print("Downloading updated version...")
        updated_code = requests.get(UPDATED_SCRIPT_URL).text
        current_file = sys.argv[0]
        backup_file = current_file + ".bak"
        os.rename(current_file, backup_file)
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(updated_code)
        print("Update downloaded and applied. Restarting...")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("Update failed:", e)

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
        print("=== Python Casino ===")
        print("Version:", CURRENT_VERSION)
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
            check_for_update()
            input("Press Enter to return to the main menu...")
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # Optionally, check for updates at startup.
    check_for_update()
    main_menu()
