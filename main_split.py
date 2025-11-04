"""
Semi-Automatic Betting Script

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
  pip install selenium webdriver-manager python-dotenv undetected-chromedriver

Usage:
  - Set REBEL_USERNAME and REBEL_PASSWORD environment variables if you want to enable
    automated login. Otherwise, the script opens the login page and waits for you to log in
    manually and press Enter.
  - Edit SELECTORS in config.py to match the site's current DOM.
  run ---> 
  - cmd /c "venv_py310\Scripts\python.exe main_split.py"

  

"""

import os
import dotenv
from driver_utils import start_driver, automated_login, wait_for_manual_login, open_first_bet_card

dotenv.load_dotenv()


def main():
    driver = start_driver()
    try:
        username = os.getenv("REBEL_USERNAME")
        password = os.getenv("REBEL_PASSWORD")
        
        if username and password:
            print("REBEL_USERNAME found in env — attempting automated login (may fail).")
            automated_login(driver, username, password)
        else:
            wait_for_manual_login(driver)

        input("Login completed. Press Enter to continue with bet placement...")
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