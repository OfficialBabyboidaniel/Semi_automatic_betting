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
            # delay = random.uniform(1, 3)
            # print(f"Waiting {delay:.1f} seconds before handling cookies...")
            # time.sleep(delay)
            
            # Handle cookies first
            # if self.handle_cookies(driver):
                # Random delay after cookie handling
                # delay = random.uniform(1, 3)
                # print(f"Waiting {delay:.1f} seconds after cookie handling...")
                # time.sleep(delay)
            
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
                        print("Keeping window open for review...")
                        return True
                except:
                    # Check for limit message - try multiple approaches
                    print("Bet placement failed, checking for limit message...")
                    
                    # Wait a moment for any overlays to appear
                    time.sleep(1)
                    
                    # Try to find any error/feedback elements
                    limit_detected = False
                    max_amount = None
                    
                    # Method 1: Look for overlay error
                    try:
                        overlay = driver.find_element(By.CSS_SELECTOR, ".mod-KambiBC-betslip__overlay--error")
                        print("Found error overlay")
                        limit_detected = True
                    except:
                        pass
                    
                    # Method 2: Look for feedback elements
                    try:
                        feedback_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='feedback']") 
                        if feedback_elements:
                            print(f"Found {len(feedback_elements)} feedback elements")
                            limit_detected = True
                    except:
                        pass
                    
                    # Method 3: Look for currency spans
                    try:
                        currency_spans = driver.find_elements(By.CSS_SELECTOR, "span[class*='currency']")
                        for span in currency_spans:
                            text = span.text
                            if 'kr' in text and any(char.isdigit() for char in text):
                                max_amount = text.replace(' kr', '').replace(',', '.')
                                print(f"Found currency amount: {max_amount}")
                                limit_detected = True
                                break
                    except:
                        pass
                    
                    if limit_detected:
                        print("Limit detected, attempting to handle...")
                        
                        # Try to find and click close/back button
                        close_selectors = [
                            "button[aria-label*='Stäng']",
                            "button[aria-label*='tillbaka']", 
                            "button[aria-label*='Tillbaka']",
                            ".close", 
                            "[data-dismiss]"
                        ]
                        
                        for selector in close_selectors:
                            try:
                                close_btn = driver.find_element(By.CSS_SELECTOR, selector)
                                close_btn.click()
                                print(f"Clicked close button: {selector}")
                                break
                            except:
                                continue
                        
                        time.sleep(2)
                        
                        # If we have max_amount, try to place bet with it
                        if max_amount:
                            try:
                                # Try multiple selectors for the bet input field
                                input_selectors = [
                                    "input[data-testid='betslip-stake-input']",
                                    "input[class*='stake-input']",
                                    "input[type='number']",
                                    ".mod-KambiBC-betslip__system-stake-input input",
                                    "input[class*='betslip']"
                                ]
                                
                                bet_input = None
                                for selector in input_selectors:
                                    try:
                                        bet_input = WebDriverWait(driver, 3).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                        )
                                        print(f"Found input with selector: {selector}")
                                        break
                                    except:
                                        continue
                                
                                if bet_input:
                                    bet_input.clear()
                                    bet_input.send_keys(max_amount)
                                    print(f"Entered max amount: {max_amount}")
                                    time.sleep(1)
                                else:
                                    print("Could not find bet input field")
                                    return False
                                
                                # Try multiple selectors for the bet button
                                bet_selectors = [
                                    "button[aria-label='Lägg spel'][data-touch-feedback='true']",
                                    "button[aria-label='Lägg spel']",
                                    ".mod-KambiBC-betslip__place-bet-btn",
                                    "button[class*='place-bet']"
                                ]
                                
                                bet_clicked = False
                                for selector in bet_selectors:
                                    try:
                                        bet_button = driver.find_element(By.CSS_SELECTOR, selector)
                                        bet_button.click()
                                        print(f"Clicked bet button with selector: {selector}")
                                        bet_clicked = True
                                        break
                                    except Exception as e:
                                        print(f"Failed with selector {selector}: {e}")
                                        continue
                                
                                if not bet_clicked:
                                    print("Could not find bet button with any selector")
                                
                                if bet_clicked:
                                    time.sleep(2)
                                    
                                    # Check for success
                                    try:
                                        success = driver.find_element(By.CSS_SELECTOR, ".mod-KambiBC-betslip-receipt-header__title")
                                        if "lagts" in success.text.lower():
                                            print("✅ BET PLACED WITH MAX AMOUNT!")
                                            print("Keeping window open for review...")
                                            return True
                                    except:
                                        print("Could not verify bet success")
                            except Exception as e:
                                print(f"Could not place bet with max amount: {e}")
                    else:
                        print("No limit detected, unknown error")
            except Exception as btn_e:
                print(f"Could not find or click 'Lägg spel' button: {btn_e}")
                try:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
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