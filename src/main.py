
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def remove_product_from_basket(browser: WebDriver):
    index = int(input('Enter index of product to remove (start from 1): '))
    browser.find_element(By.ID, f'cartProductActions{index - 1}').click()
    delete_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.context-menu-actions__button')),
    )
    delete_button.click()
    print('Product has been deleted successfully')


def move_to_product_page(item_index: int, waiter: WebDriverWait) -> None:
    li_items = waiter.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'catalog-grid__cell')))
    item = li_items[item_index]
    item.click()


def find_product(browser: WebDriver):
    browser.get('https://rozetka.com.ua/')
    product_name = input('Enter a product which you want to find: ')
    input_ = browser.find_element(By.CSS_SELECTOR, '[class="search-form__input ng-untouched ng-pristine ng-valid"]')
    input_.send_keys(product_name + Keys.ENTER)
    waiter = WebDriverWait(browser, 10, ignored_exceptions=[StaleElementReferenceException])
    try:
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.goods-tile__inner')))
    except TimeoutException:
        print('Nothing found try again\n')
        return
    item_index = 0
    while True:
        move_to_product_page(item_index, waiter)
        action = input('Choose this item?(yes, cancel, next): ').lower().strip()
        if action == 'next' or action == 'n':
            item_index += 1
            browser.back()
        elif action == 'yes' or action == 'y':
            button = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.buy-button.button.button--green')))
            button.click()
            break
        elif action == 'cancel' or action == 'c':
            browser.back()
            break
    is_continue_searching = input('Search one more product? (yes, no): ')
    if is_continue_searching in ('yes', 'y', '\n'):
        find_product(browser)


def show_basket_content(browser: WebDriver, waiter: WebDriverWait):
    li_items = waiter.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cart-list__item.ng-star-inserted')))
    if li_items:
        print('\nYour basket contains this products:')
    else:
        print('Your basket is empty')
    for li_item in li_items:
        a_link = li_item.find_element(By.CSS_SELECTOR, '.cart-product__title')
        print('--', a_link.get_attribute("title"))
    print()


def manage_user_basket(browser: WebDriver):
    waiter = WebDriverWait(browser, 10)
    try:
        # go inside basket
        waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.header__button--active'))).click()
    except Exception:
        """Already in baskets"""
    show_basket_content(browser, waiter)

    action = input('Choose next action (remove, buy, add): ').lower().strip()
    if action in ('remove', 'r'):
        remove_product_from_basket(browser)
    elif action in ('buy', 'b'):
        browser.find_element(By.CSS_SELECTOR, '.cart-receipt__submit.ng-star-inserted').click()
    if action in ('add', 'a'):
        find_product(browser)


def main(browser: WebDriver):
    find_product(browser)
    manage_user_basket(browser)


if __name__ == '__main__':

    options = Options()
    options.set_preference("dom.push.enabled", False)
    browser = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
    try:
        main(browser)
    except Exception as error:
        browser.quit()
        raise error
