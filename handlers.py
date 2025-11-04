"""Bookmaker-specific handlers for different betting platforms."""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bookmakers import ALTENAR_BOOKMAKERS


class BookmakerHandler:
    def handle(self, driver, bet_card):
        print("No custom handler for this bookmaker. Default behavior.")


class BetiniaHandler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling Betinia bet...")


class Bet365Handler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling Bet365 bet...")


class Sport888Handler(BookmakerHandler):
    def handle(self, driver, bet_card):
        print("Handling 888sport bet...")


class KambiHandler(BookmakerHandler):
    def handle_cookies(self, driver):
        """Handle cookie consent with preference for minimal cookies"""
        # Try minimal cookies first
        minimal_selectors = [
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ', 'abcdefghijklmnopqrstuvwxyzåäö'), 'endast nödvändiga')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ', 'abcdefghijklmnopqrstuvwxyzåäö'), 'neka alla')]",
            "[data-testid='uc-deny-all-button']"
        ]
        
        # Fallback to accept all
        accept_selectors = [
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ', 'abcdefghijklmnopqrstuvwxyzåäö'), 'godkänn')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ', 'abcdefghijklmnopqrstuvwxyzåäö'), 'acceptera alla')]",
            "[data-testid='uc-accept-all-button']"
        ]
        
        # Try minimal first
        for selector in minimal_selectors:
            try:
                if selector.startswith('//'):
                    cookie_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    cookie_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                # Random delay before clicking cookie button
                delay = random.uniform(0.5, 2)
                time.sleep(delay)
                cookie_btn.click()
                print(f"Clicked minimal cookie button")
                return True
            except:
                continue
                
        # Fallback to accept all
        for selector in accept_selectors:
            try:
                if selector.startswith('//'):
                    cookie_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    cookie_btn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                # Random delay before clicking cookie button
                delay = random.uniform(0.5, 2)
                time.sleep(delay)
                cookie_btn.click()
                print(f"Clicked accept all cookie button")
                return True
            except:
                continue
        return False
    
    def handle(self, driver, bet_card):
        print("Handling Kambi-powered bookmaker bet...")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BetOnBookmaker")))
            bet_link = driver.find_element(By.ID, "BetOnBookmaker")
            href = bet_link.get_attribute("href")
            print(f"Found Kambi bet link: {href}")
            
            # Random delay before opening link
            delay = random.uniform(1, 3)
            print(f"Waiting {delay:.1f} seconds before opening link...")
            time.sleep(delay)
            
            driver.execute_script(f"window.open('{href}', '_blank');")
            print("Opened the Kambi bet link in a new tab.")
            
            # Random delay before switching tabs
            delay = random.uniform(1, 3)
            print(f"Waiting {delay:.1f} seconds before switching tabs...")
            time.sleep(delay)
            
            # Switch to new tab
            driver.switch_to.window(driver.window_handles[-1])
            
            # Random delay before handling cookies
            delay = random.uniform(1, 3)
            print(f"Waiting {delay:.1f} seconds before handling cookies...")
            time.sleep(delay)
            
            # Handle cookies first
            if self.handle_cookies(driver):
                # Random delay after cookie handling
                delay = random.uniform(1, 3)
                print(f"Waiting {delay:.1f} seconds after cookie handling...")
                time.sleep(delay)
            
            # Click the "Lägg spel" button if it appears
            try:
                bet_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Lägg spel']"))
                )
                
                # Random delay before clicking bet button
                delay = random.uniform(1, 3)
                print(f"Waiting {delay:.1f} seconds before clicking bet button...")
                time.sleep(delay)
                
                bet_button.click()
                print("Clicked 'Lägg spel' button")
            except Exception as btn_e:
                print(f"Could not find or click 'Lägg spel' button: {btn_e}")
                
        except Exception as e:
            print(f"Could not find or open Kambi bet link: {e}")


class AltenarHandler(BookmakerHandler):
    session_selection = None

    def handle(self, driver, bet_card):
        print("Handling Altenar-powered bookmaker bet (Betinia/Altenar)...")
        if AltenarHandler.session_selection is None:
            active_bookies = [b for b in ALTENAR_BOOKMAKERS if b["active"]]
            AltenarHandler.session_selection = random.sample(active_bookies, min(5, len(active_bookies)))
            print("Selected Altenar bookies for this session:")
            for b in AltenarHandler.session_selection:
                print(f"- {b['url']}")
        print("Using these Altenar bookies for this bet:")
        for b in AltenarHandler.session_selection:
            print(f"- {b['url']}")


BOOKMAKER_HANDLERS = {
    "Betinia": AltenarHandler(),
    "Bet365": Bet365Handler(),
    "888sport": Sport888Handler(),
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