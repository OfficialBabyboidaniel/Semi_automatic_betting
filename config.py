"""Configuration settings for the betting automation script."""

# URLs
LOGIN_URL = "https://vb.rebelbetting.com/login"
BET_LIST_URL = "https://vb.rebelbetting.com/"

# Selectors (placeholders - must be updated for actual site)
SELECTORS = {
    "bet_row": "div.bet-row",
    "bet_title": ".bet-title",
    "bet_odds": ".bet-odds",
    "place_button": ".place-bet-btn",
    "confirm_modal": "div.confirm-modal",
    "confirm_button": "button.confirm",
}

# Driver settings
HEADLESS = False
IMPLICIT_WAIT = 5