
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

WAIT_SECONDS = 15
STEP_DELAY = 1.5


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()

    # Browser settings
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--guest")
    options.add_argument("--disable-features=PasswordLeakDetection")

    # Disable Chrome password manager prompts
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)

    # Optional headless mode
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)

    yield browser

    browser.quit()


def wait_for(driver, condition):
    return WebDriverWait(driver, WAIT_SECONDS).until(condition)


def pause():
    """Slow down execution so browser steps are visible."""
    time.sleep(STEP_DELAY)


def test_user_can_checkout_one_product(driver):

    # Step 1: Open website
    driver.get(BASE_URL)
    pause()

    # Step 2: Enter username
    wait_for(
        driver,
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys(USERNAME)
    pause()

    # Enter password and login
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    pause()

    driver.find_element(By.ID, "login-button").click()

    # Verify login and inventory page
    wait_for(driver, EC.url_contains("inventory.html"))

    wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    )
    assert "inventory.html" in driver.current_url
    pause()

    # Step 3: Add product to cart
    product_name = "Sauce Labs Backpack"

    driver.find_element(
        By.ID, "add-to-cart-sauce-labs-backpack"
    ).click()
    pause()

    # Step 4: Verify cart badge
    badge = wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    assert badge.text == "1"
    pause()

    # Step 5: Open cart and verify product
    driver.find_element(
        By.CLASS_NAME, "shopping_cart_link"
    ).click()

    wait_for(driver, EC.url_contains("cart.html"))

    cart_product = wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    assert cart_product.text == product_name
    pause()

    # Step 6: Proceed to checkout
    driver.find_element(By.ID, "checkout").click()

    wait_for(driver, EC.url_contains("checkout-step-one.html"))
    pause()

    # Enter checkout details
    wait_for(
        driver,
        EC.visibility_of_element_located((By.ID, "first-name"))
    ).send_keys("Test")
    pause()

    driver.find_element(By.ID, "last-name").send_keys("User")
    pause()

    driver.find_element(By.ID, "postal-code").send_keys("12345")
    pause()

    driver.find_element(By.ID, "continue").click()

    # Step 7: Verify order overview
    wait_for(driver, EC.url_contains("checkout-step-two.html"))

    overview_product = wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    assert overview_product.text == product_name

    subtotal = driver.find_element(
        By.CLASS_NAME, "summary_subtotal_label"
    ).text

    total = driver.find_element(
        By.CLASS_NAME, "summary_total_label"
    ).text

    assert subtotal.startswith("Item total:")
    assert total.startswith("Total:")
    pause()

    # Step 8: Finish checkout
    driver.find_element(By.ID, "finish").click()

    wait_for(driver, EC.url_contains("checkout-complete.html"))

    # Step 9: Verify successful order
    confirmation = wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    )

    assert confirmation.text == "Thank you for your order!"

    # Keep confirmation visible briefly
    pause()
