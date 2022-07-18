
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def remove_element_from_basket(driver: WebDriver):
    waiter = WebDriverWait(driver, 10)
    try:
        # go inside basket
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.header__button--active'))).click()
    except Exception:
        """Already in baskets"""


def find_product(driver: WebDriver, product_name: str):
    input_ = driver.find_element(By.CSS_SELECTOR, '[class="search-form__input ng-untouched ng-pristine ng-valid"]')
    input_.send_keys(product_name + Keys.ENTER)
    waiter = WebDriverWait(driver, 10)
    waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.goods-tile__inner')))
    li_items = driver.find_elements(By.CLASS_NAME, 'catalog-grid__cell')
    for li_item in li_items:
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.goods-tile__inner'))).click()
        action = input('Choose this item?(yes, cancel, next)').strip()
        if action == 'next':
            driver.back()
        elif action == 'yes':
            button = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.buy-button.button.button--green')))
            button.click()
        elif action == 'cancel':
            driver.back()
            break


def main(driver: WebDriver):
    product_name = input('Enter a product which you want to find: ')
    driver.get('https://rozetka.com.ua/')
    find_product(driver, product_name)


if __name__ == '__main__':
    options = Options()
    options.set_preference("dom.push.enabled", False)
    driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
    try:
        main(driver)
    finally:
        driver.quit()
