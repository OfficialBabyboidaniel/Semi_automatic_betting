"""WebDriver utilities and automation functions."""

import time
import os
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config import LOGIN_URL, HEADLESS, IMPLICIT_WAIT
from handlers import BOOKMAKER_HANDLERS


def start_driver():
    """Initialize and return Chrome driver"""
    options = uc.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Use webdriver-manager to get the correct ChromeDriver version
    driver_path = ChromeDriverManager().install()
    driver = uc.Chrome(driver_executable_path=driver_path, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    
    # Navigate to login page immediately
    print(f"Navigating to login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)
    print("Page loaded successfully!")
    return driver


def wait_for_manual_login(driver):
    """Open login page and wait for manual login"""
    print("Opening login page. Please log in manually in the browser window.")
    driver.get(LOGIN_URL)
    input("When you've completed login, press Enter here to continue...")


def automated_login(driver, username, password):
    """Attempt automated login"""
    driver.get(LOGIN_URL)
    try:
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Page loaded. Waiting 2 extra seconds for scripts...")
        time.sleep(2)
        
        user_input = driver.find_element(By.ID, "inputEmail")
        pass_input = driver.find_element(By.ID, "inputPassword")
        
        driver.execute_script('arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event("input", {bubbles:true})); arguments[0].dispatchEvent(new Event("change", {bubbles:true}));', user_input, username)
        time.sleep(0.2)
        driver.execute_script('arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event("input", {bubbles:true})); arguments[0].dispatchEvent(new Event("change", {bubbles:true}));', pass_input, password)
        time.sleep(0.2)
        
        try:
            submit = driver.find_element(By.CSS_SELECTOR, "button[type=submit], button.btn-primary")
            submit.click()
        except NoSuchElementException:
            pass
        time.sleep(2)
    except TimeoutException:
        print("Timed out waiting for login form — the automated login may not work. Please log in manually.")
        wait_for_manual_login(driver)


def open_first_bet_card(driver):
    """Find and open the first available bet card"""
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("Page loaded. Waiting 2 extra seconds for scripts...")
    time.sleep(2)
    
    try:
        selector = 'div.card-shadow-hover.d-flex.clickable'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        # Re-find elements to avoid stale reference
        bet_cards = driver.find_elements(By.CSS_SELECTOR, selector)
        if not bet_cards:
            print("No bet cards found with selector:", selector)
            return False
            
        # Get fresh reference and click immediately
        first_card = bet_cards[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_card)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Re-find element right before clicking to avoid stale reference
        fresh_cards = driver.find_elements(By.CSS_SELECTOR, selector)
        if fresh_cards:
            fresh_cards[0].click()
            print("Clicked the first bet card. Dispatching to bookmaker handler...")
            handle_bet_card(driver, None)  # Pass None since we don't need the element
            return True
        else:
            print("Bet card disappeared before clicking")
            return False
        
    except Exception as e:
        print(f"Failed to open first bet card: {e}")
        return False


def handle_bet_card(driver, bet_card):
    """Handle bet card after opening"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bookmaker")))
        bookmaker_div = driver.find_element(By.ID, "bookmaker")
        bookmaker_name = bookmaker_div.text.strip()
        print(f"Detected bookmaker: {bookmaker_name}")
        handler = BOOKMAKER_HANDLERS.get(bookmaker_name, BOOKMAKER_HANDLERS.get("default", None))
        if handler:
            handler.handle(driver, bookmaker_div)
        else:
            print("No handler found for this bookmaker.")
    except Exception as e:
        print(f"Could not determine bookmaker or handle bet: {e}")