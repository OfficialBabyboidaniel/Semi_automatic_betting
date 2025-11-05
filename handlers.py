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
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Lägg spel']")) ## identifier for "Place Bet" is too weak, must add more selectors
                )
                
                # Random delay before clicking bet button
                delay = random.uniform(1, 3)
                print(f"Waiting {delay:.1f} seconds before clicking bet button...")
                time.sleep(delay)
                
                bet_button.click()
                print("Clicked 'Lägg spel' button")
                
                # Check for bet result after clicking
                delay = random.uniform(1, 3)
                print(f"Waiting {delay:.1f} seconds to check bet result...")
                time.sleep(delay)
                
                # Check for successful bet placement
                try:
                    success_element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-KambiBC-betslip-receipt-header__title"))
                    )
                    if "lagts" in success_element.text.lower():
                        print("✅ BET SUCCESSFULLY PLACED!")
                        
                        # Close current tab and return to betting page
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        print("Returned to betting page")
                        return True
                except:
                    # Check for limit message
                    try:
                        limit_element = WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-KambiBC-betslip-feedback__title"))
                        )
                        limit_text = limit_element.text.lower()
                        if "högsta" in limit_text or "limit" in limit_text:
                            print(f"Bet limit detected: {limit_text}")
                            
                            # Extract maximum allowed amount
                            try:
                                import re
                                max_amount_match = re.search(r'(\d+(?:[.,]\d+)?)', limit_text)
                                if max_amount_match:
                                    max_amount = max_amount_match.group(1).replace(',', '.')
                                    print(f"Maximum allowed bet: {max_amount}")
                                    
                                    # Click back button first
                                    back_button = WebDriverWait(driver, 3).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Tillbaka till spelkupongen']"))
                                    )
                                    back_button.click()
                                    
                                    delay = random.uniform(1, 2)
                                    time.sleep(delay)
                                    
                                    # Find and clear bet amount input field
                                    bet_input = WebDriverWait(driver, 3).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='betslip-stake-input']"))
                                    )
                                    bet_input.clear()
                                    bet_input.send_keys(max_amount)
                                    print(f"Entered maximum bet amount: {max_amount}")
                                    
                                    delay = random.uniform(1, 2)
                                    time.sleep(delay)
                                    
                                    # Click bet button again
                                    bet_button = WebDriverWait(driver, 3).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Lägg spel']"))
                                    )
                                    bet_button.click()
                                    print("Clicked bet button with maximum amount")
                                    
                                    # Check result again
                                    delay = random.uniform(2, 3)
                                    time.sleep(delay)
                                    
                                    try:
                                        success_element = WebDriverWait(driver, 3).until(
                                            EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-KambiBC-betslip-receipt-header__title"))
                                        )
                                        if "lagts" in success_element.text.lower():
                                            print("✅ BET SUCCESSFULLY PLACED WITH MAX AMOUNT!")
                                            driver.close()
                                            driver.switch_to.window(driver.window_handles[0])
                                            return True
                                    except:
                                        print("Bet with max amount may have failed")
                                        
                            except Exception as max_bet_e:
                                print(f"Could not place bet with max amount: {max_bet_e}")
                        else:
                            print(f"Bet feedback: {limit_text}")
                    except Exception as check_e:
                        print(f"No bet feedback found: {check_e}")
            except Exception as btn_e:
                print(f"Could not find or click 'Lägg spel' button: {btn_e}")
                return False
                
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