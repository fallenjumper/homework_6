import allure
from selenium.webdriver.common.by import By
from .BasePage import BasePage


class ProductPage(BasePage):
    CONTENT_NAME = (By.CSS_SELECTOR, ".row > div > h1")
    THUMBNAIL_PIC = (By.CSS_SELECTOR, ".thumbnail")
    BIG_PIC_THUMBNAIL = (By.CSS_SELECTOR, ".mfp-img")
    BIG_PIC_CLOSE_BTN = (By.CSS_SELECTOR, ".mfp-close")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#button-cart")
    ADD_TO_CART_ALERT = (By.CSS_SELECTOR, ".alert-success")
    CART_TOTAL_ROW = (By.CSS_SELECTOR, "#cart-total")
    QUANTITY_ITEMS_INPUT = (By.CSS_SELECTOR, "#input-quantity")
    CURRENCY_SELECTOR = (By.CSS_SELECTOR, "#form-currency > div > button")
    CURRENCY_LIST = (By.CSS_SELECTOR, ".currency-select")
    PRICE = (By.CSS_SELECTOR, ".col-sm-4 > ul > li > h2")
    TAX = (By.XPATH, "//li[starts-with(text(), 'Ex Tax:')]")
    last_price = None
    new_price = None
    tax_factor = 0.830573568
    currency_names = {'EUR': "€", 'USD': '$', 'GBP': '£'}
    currency_rates = {'EUR/USD': 1.2745326361,
                      'GBP/EUR': 1.2809643913,
                      'GBP/USD': 1.6326309224,
                      }

    @allure.step("Get {1} price of product")
    def get_price(self, price_type, current_currency):
        if price_type == "last":
            self.last_price = float(self._get_text(self.PRICE).replace(self.currency_names[current_currency], ''))
        elif price_type == "new":
            self.new_price = float(self._get_text(self.PRICE).replace(self.currency_names[current_currency], ''))
        return self

    @allure.step("Set {1} currency")
    def set_currency(self, currency):
        if currency not in self.currency_names.keys():
            raise ValueError("Некорректная валюта!")
        if self._get_text(self.CURRENCY_SELECTOR).strip() != self.currency_names[currency]:
            self._element(self.CURRENCY_SELECTOR).click()
            self._wait_until(self.CURRENCY_LIST)
            self._element_by_attribute_value(self.CURRENCY_LIST, "name", currency).click()
            self._wait_until_not(self.CURRENCY_LIST)
            assert self._get_text(self.CURRENCY_SELECTOR).strip() == self.currency_names[currency]
        return self

    @allure.step("Check new price when change currency from {1} to {2}")
    def check_new_price(self, rate_from, rate_to):
        if f'{rate_from}/{rate_to}' in self.currency_rates.keys():
            assert round(self.last_price * self.currency_rates[f'{rate_from}/{rate_to}'], 2) == self.new_price
        elif f'{rate_to}/{rate_from}' in self.currency_rates.keys():
            assert round(self.last_price / self.currency_rates[f'{rate_to}/{rate_from}'], 2) == self.new_price
        else:
            raise ValueError(f"Не найдена пара {rate_to} и {rate_from} в бд")
        return self

    @allure.step("Check tax to {1} currency")
    def check_tax(self, currency):
        cur_price_ex_tax = self._get_text(self.TAX).split(" ")[-1].replace(self.currency_names[currency], '')
        calculated_price_ex_tax = format(round(self.new_price * self.tax_factor / 0.05) * 0.05, '.2f')
        assert cur_price_ex_tax == calculated_price_ex_tax

    @allure.step("Add to cart")
    def add_to_cart(self, cart_total):
        # click add to cart and check reaction (set 2 items)
        qty_input = self._element(self.QUANTITY_ITEMS_INPUT)
        qty_input.clear()
        qty_input.send_keys(2)
        assert qty_input.get_attribute("value") == '2'
        self._element(self.SUBMIT_BUTTON).click()
        self._wait_until(self.ADD_TO_CART_ALERT)
        assert self._get_text(self.CART_TOTAL_ROW) == cart_total
        return self

    @allure.step("Loading big picture of product by click on thumbnail")
    def loading_picture_by_click(self):
        # wait loading big picture by click on thumbnail
        self._element(self.THUMBNAIL_PIC).click()
        self._wait_until(self.BIG_PIC_THUMBNAIL)

        # close after loading
        self._element(self.BIG_PIC_CLOSE_BTN).click()
        self._wait_until_not(self.BIG_PIC_THUMBNAIL)
        return self
