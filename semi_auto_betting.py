"""
Semi-automatic betting helper for RebelBetting (example).

How it works (high level):
- Uses Selenium to open the site and let you log in (recommended: manual login for safety),
  or optionally perform an automated login using environment variables.
- Scans a configurable page for bet rows (CSS selectors are placeholders and must be
  adapted to the live site with your browser's inspector).
- Presents found bets to you in the console and asks which bets to place.
- Performs the placement actions (filling forms / clicking buttons) after your confirmation.

IMPORTANT:
- This is a template and uses placeholder selectors. You MUST inspect the site's DOM and
  adjust the selectors before using. Automating actions on third-party sites may violate
  their Terms of Service; you are responsible for compliance and for your account security.

Requirements:
  pip install selenium webdriver-manager python-dotenv

Usage:
  - Set REBEL_USERNAME and REBEL_PASSWORD environment variables if you want to enable
    automated login. Otherwise, the script opens the login page and waits for you to log in
    manually and press Enter.
  - Edit SELECTORS below to match the site's current DOM.
  - Run: python semi_auto_betting.py

"""

# --- ALTENAR BOOKMAKER COLLECTION ---
import random

ALTENAR_BOOKMAKERS = [
    {"url": "https://betinia.se/sv/sport?page=overview", "active": True, "betsPlaced": 0},
    {"url": "https://campobet.se/en/sport/prelive?page=overview", "active": True, "betsPlaced": 0},
    {"url": "https://quickcasino.se/sv/sports", "active": True, "betsPlaced": 0},
    {"url": "https://flaxcasino.se/sports?page=overview", "active": True, "betsPlaced": 0},
    {"url": "https://happycasino.se/sports?page=sports", "active": True, "betsPlaced": 0},
    {"url": "https://luckycasino.com/sv/sports", "active": True, "betsPlaced": 0},
    {"url": "https://www.casinocasino.com/sv/sports-book/sports", "active": True, "betsPlaced": 0},
    {"url": "https://svenbet.com/sports", "active": True, "betsPlaced": 0},
    {"url": "https://www.betrebels.com/sports", "active": True, "betsPlaced": 0},
    {"url": "https://www.videoslots.com/sv/sports/#/overview/", "active": True, "betsPlaced": 0},
    {"url": "https://www.kungaslottet.se/sports/#/overview/", "active": True, "betsPlaced": 0},
    {"url": "https://www.mrvegas.com/sv/sports/#/overview/", "active": True, "betsPlaced": 0},
    {"url": "https://www.dbet.com/sports/#/overview/", "active": True, "betsPlaced": 0},
    {"url": "https://frankfred.com/lobby/sport#/overview", "active": True, "betsPlaced": 0},
    {"url": "https://jubla.se/lobby/sport#/overview", "active": True, "betsPlaced": 0},
    {"url": "https://www.megariches.com/sv/sports/#/overview/", "active": True, "betsPlaced": 0},
    {"url": "https://onerush.com/se/lobby/sport#/overview", "active": True, "betsPlaced": 0},
    {"url": "https://www.racecasino.com/sv/sports-book/sports", "active": True, "betsPlaced": 0},
]

# Store session Altenar selection
SESSION_ALTENAR_SELECTION = []

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random
import dotenv

dotenv.load_dotenv()

# --- CONFIGURE ---
LOGIN_URL = "https://vb.rebelbetting.com/login"
BET_LIST_URL = "https://vb.rebelbetting.com/"  # change to the page where bets are listed
# Selectors below are placeholders. Inspect the page and update accordingly.
SELECTORS = {
    "bet_row": "div.bet-row",                  # CSS selector for a row/entry that represents a bet
    "bet_title": ".bet-title",                 # within bet_row, selector for readable title
    "bet_odds": ".bet-odds",                   # within bet_row, selector for odds
    "place_button": ".place-bet-btn",         # selector for the place button inside a bet_row
    # If placing a bet requires a confirmation modal, set selectors for the modal
    "confirm_modal": "div.confirm-modal",
    "confirm_button": "button.confirm",
}
# --- END CONFIG ---

HEADLESS = False  # set True to run headless (not recommended during setup/selector tuning)
IMPLICIT_WAIT = 5

# --- BOOKMAKER HANDLER ARCHITECTURE ---
class BookmakerHandler:
    def handle(self, driver, bet_card):
        print("No custom handler for this bookmaker. Default behavior.")

class BetiniaHandler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling Betinia bet...")
        # Add Betinia-specific logic here

class Bet365Handler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling Bet365 bet...")
        # Add Bet365-specific logic here

class Sport888Handler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling 888sport bet...")
        # Add 888sport-specific logic here

# Clone handler for similar bookmakers

# Handler for all Kambi-powered bookmakers
class KambiHandler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling Kambi-powered bookmaker bet...")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BetOnBookmaker")))
            bet_link = driver.find_element(By.ID, "BetOnBookmaker")
            href = bet_link.get_attribute("href")
            print(f"Found Kambi bet link: {href}")
            driver.execute_script(f"window.open('{href}', '_blank');")
            print("Opened the Kambi bet link in a new tab.")
            time.sleep(2)
        except Exception as e:
            print(f"Could not find or open Kambi bet link: {e}")

# Handler for Altenar-powered bookmaker (Betinia)
class AltenarHandler(BookmakerHandler):
    session_selection = None

    def handle(self, driver, bet_card):
        print("Handling Altenar-powered bookmaker bet (Betinia/Altenar)...")
        if AltenarHandler.session_selection is None:
            # Choose 5 random active Altenar bookies for this session
            active_bookies = [b for b in ALTENAR_BOOKMAKERS if b["active"]]
            AltenarHandler.session_selection = random.sample(active_bookies, min(5, len(active_bookies)))
            print("Selected Altenar bookies for this session:")
            for b in AltenarHandler.session_selection:
                print(f"- {b['url']}")
        # Use only these 5 for all bets in this session
        # Example: print the URLs (replace with your bet logic)
        print("Using these Altenar bookies for this bet:")
        for b in AltenarHandler.session_selection:
            print(f"- {b['url']}")

BOOKMAKER_HANDLERS = {
    "Betinia": AltenarHandler(),  # Betinia uses Altenar
    "Bet365": Bet365Handler(),
    "888sport": Sport888Handler(),
    # Kambi-powered clones:
    "ATG": KambiHandler(),
    "BetMGM": KambiHandler(),
    "Casumo": KambiHandler(),
    "Expekt": KambiHandler(),
    "LeoVegas": KambiHandler(),
    "GoldenBull": KambiHandler(),
    "Paf": KambiHandler(),
    "SpeedyBet": KambiHandler(),
    "SvenskaSpel": KambiHandler(),
    "Unibet": KambiHandler(),
    "X3000": KambiHandler(),
}

def handle_bet_card(driver, bet_card):
    try:
        # After clicking, the DOM may change, so re-find the bookmaker element from the driver
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bookmaker")))
        bookmaker_div = driver.find_element(By.ID, "bookmaker")
        bookmaker_name = bookmaker_div.text.strip()
        print(f"Detected bookmaker: {bookmaker_name}")
        handler = BOOKMAKER_HANDLERS.get(bookmaker_name, BookmakerHandler())
        handler.handle(driver, bookmaker_div)
    except Exception as e:
        print(f"Could not determine bookmaker or handle bet: {e}")

# --- CONFIGURE ---
LOGIN_URL = "https://vb.rebelbetting.com/login"
BET_LIST_URL = "https://vb.rebelbetting.com/"  # change to the page where bets are listed
# Selectors below are placeholders. Inspect the page and update accordingly.
SELECTORS = {
    "bet_row": "div.bet-row",                  # CSS selector for a row/entry that represents a bet
    "bet_title": ".bet-title",                 # within bet_row, selector for readable title
    "bet_odds": ".bet-odds",                   # within bet_row, selector for odds
    "place_button": ".place-bet-btn",         # selector for the place button inside a bet_row
    # If placing a bet requires a confirmation modal, set selectors for the modal
    "confirm_modal": "div.confirm-modal",
    "confirm_button": "button.confirm",
}
# --- END CONFIG ---

HEADLESS = False  # set True to run headless (not recommended during setup/selector tuning)
IMPLICIT_WAIT = 5


def start_driver():
    options = uc.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    # recommended: use a regular user profile for convenience (optional)
    # options.add_argument(r"--user-data-dir=C:\Users\YOURNAME\AppData\Local\Google\Chrome\User Data")

    # Use webdriver-manager to get the correct ChromeDriver version
    driver_path = ChromeDriverManager().install()
    driver = uc.Chrome(driver_executable_path=driver_path, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver


def wait_for_manual_login(driver):
    print("Opening login page. Please log in manually in the browser window.")
    driver.get(LOGIN_URL)
    input("When you've completed login, press Enter here to continue...")


def automated_login(driver, username, password):
    # This function is optional and fragile — prefer manual login. Adjust selectors if you use it.
    driver.get(LOGIN_URL)
    try:
        # Wait for either username/email or password field to appear
       # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputPassword")))
        # Wait for full page load, then extra 2 seconds
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Page loaded. Waiting 2 extra seconds for scripts...")
        time.sleep(2)
        user_input = driver.find_element(By.ID, "inputEmail")
        pass_input = driver.find_element(By.ID, "inputPassword")
        # Set values using JavaScript and dispatch events
        driver.execute_script('arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event("input", {bubbles:true})); arguments[0].dispatchEvent(new Event("change", {bubbles:true}));', user_input, username)
        time.sleep(0.2)
        driver.execute_script('arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event("input", {bubbles:true})); arguments[0].dispatchEvent(new Event("change", {bubbles:true}));', pass_input, password)
        time.sleep(0.2)
        # Try to find and click the submit button
        try:
            submit = driver.find_element(By.CSS_SELECTOR, "button[type=submit], button.btn-primary")
            submit.click()
        except NoSuchElementException:
            pass
        time.sleep(2)
        # try to find a submit button
        # try:
        #     submit = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
        #     submit.click()
        # except NoSuchElementException:
        #     pass
        # # wait for a URL change or an element that indicates login
        # time.sleep(3)
    except TimeoutException:
        print("Timed out waiting for login form — the automated login may not work. Please log in manually.")
        wait_for_manual_login(driver)

def open_first_bet_card(driver):
    """
    Finds and clicks the first bet card div with the shared classes (card-shadow-hover d-flex clickable).
    """

    # Wait for full page load, then extra 2 seconds
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("Page loaded. Waiting 2 extra seconds for scripts...")
    time.sleep(2)
    try:
        # CSS selector for a div with all three classes (order doesn't matter)
        selector = 'div.card-shadow-hover.d-flex.clickable'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        bet_cards = driver.find_elements(By.CSS_SELECTOR, selector)
        if not bet_cards:
            print("No bet cards found with selector:", selector)
            return False
        # Re-locate the first card right before clicking to avoid stale reference
        first_card = driver.find_elements(By.CSS_SELECTOR, selector)[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_card)
        time.sleep(random.uniform(0.5, 1.5))
        first_card.click()
        print("Clicked the first bet card. Dispatching to bookmaker handler...")
        handle_bet_card(driver, first_card)
        return True
    except Exception as e:
        print(f"Failed to open first bet card: {e}")
        return False

def main():
    driver = start_driver()
    try:
        username = os.getenv("REBEL_USERNAME")
        password = os.getenv("REBEL_PASSWORD")
        if username and password:
            print("REBEL_USERNAME found in env — attempting automated login (may fail).")
            automated_login(driver, username, password)
            ##input("If automated login did not finish, manually log in and press Enter to continue...")
        else:
            wait_for_manual_login(driver)

        
        print("Opening the first bet card (by shared classes)...")
        opened = open_first_bet_card(driver)
        if opened:
            print("Done. Review your account on the site to confirm the first bet card was opened.")
        else:
            print("No bet card was opened.")
    finally:
        input("Press Enter to close the browser and exit...")
        driver.quit()


if __name__ == '__main__':
    main()
