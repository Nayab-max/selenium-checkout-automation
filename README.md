# SauceDemo Checkout Automation

## Overview

This project contains a Selenium WebDriver automated test using Python and pytest. It verifies the end-to-end checkout flow on the SauceDemo demo website.

## Automated Test Scenario

1. Open SauceDemo.
2. Log in with the standard test account.
3. Add Sauce Labs Backpack to the cart.
4. Verify the cart quantity and product.
5. Enter checkout information.
6. Verify the checkout overview.
7. Finish checkout and verify the order confirmation message.

## Prerequisites

- Python 3
- Google Chrome
- Visual Studio Code or another code editor

## Setup Instructions

Clone or download this repository, then open a terminal in the project directory.

Install the dependencies:

```bash
python -m pip install selenium pytest
```

## Run the Test

Run the following command from the project directory:

```bash
python -m pytest -v
```

## Expected Result

The test should pass and display a result similar to:

```text
test_checkout_flow.py::test_user_can_checkout_one_product PASSED
```

## Test Website

https://www.saucedemo.com/

## Tools Used

- Python
- Selenium WebDriver
- pytest
- Google Chrome

## Notes

This is a demonstration test for the successful checkout flow. It does not cover negative scenarios such as invalid login or missing checkout information.