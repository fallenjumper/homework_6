import allure
from selenium.webdriver.common.by import By
from .BasePage import BasePage
import random


class AdminPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "#input-username")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#input-password")
    FORGOTTEN_PASS_LINK = (By.CSS_SELECTOR, ".help-block > a")
    HEADER_TITLE = (By.CSS_SELECTOR, ".panel-title")
    SUBMIT_BTN = (By.CSS_SELECTOR, ".btn.btn-primary")
    ERROR_LOGIN_MSG = (By.XPATH, "//div[contains(text(), 'No match for Username and/or Password.')]")
    CATALOG_BTN = (By.CSS_SELECTOR, "#menu-catalog > a")
    PRODUCT_BTN = (By.CSS_SELECTOR, "#menu-catalog > ul > li > a[href*='product']")
    ADD_BTN = (By.CSS_SELECTOR, "a[data-original-title='Add New']")
    EDIT_BTN = (By.CSS_SELECTOR, "a[data-original-title='Edit']")
    DELETE_BTN = (By.CSS_SELECTOR, "button[data-original-title='Delete']")
    SAVE_BTN = (By.CSS_SELECTOR, "button[data-original-title='Save']")
    PRODUCT_CHECKBOX = (By.CSS_SELECTOR, "input[name*=selected]")
    PRODUCT_NAME_INPUT = (By.CSS_SELECTOR, "#input-name1")
    META_TITLE_INPUT = (By.CSS_SELECTOR, "#input-meta-title1")
    DATA_MENU_BTN = (By.CSS_SELECTOR, "a[href*=tab-data]")
    INPUT_MODEL = (By.CSS_SELECTOR, "#input-model")
    PRODUCTS_ROWS = (By.CSS_SELECTOR, "table > tbody > tr")
    ROW_ITEMS = (By.CSS_SELECTOR, "td")
    LIST_OF_PRODUCTS = None

    @allure.step("Check username placeholder")
    def check_placeholder(self):
        # check correct placeholder
        assert self._element(self.USERNAME_INPUT).get_attribute("placeholder") == "Username"
        return self

    @allure.step("Check type of pass field")
    def check_type_pass_field(self):
        # check password input type is pass
        assert self._element(self.PASSWORD_INPUT).get_attribute("type") == "password"
        return self

    @allure.step("Check text in link of forgotten password")
    def check_forgotten_link_text(self, url):
        # check correct link to restore password
        assert self._element(self.FORGOTTEN_PASS_LINK).get_attribute(
            "href") == f"{url}admin/index.php?route=common/forgotten"
        return self

    @allure.step("Wait fail message about incorrect creds")
    def wait_fail_login_msg(self):
        self._wait_until(self.ERROR_LOGIN_MSG)
        return self

    @allure.step("Try to login with username:{1} and password:{2}")
    def login_with(self, username, password):
        self._element(self.USERNAME_INPUT).send_keys(username)
        self._element(self.PASSWORD_INPUT).send_keys(password)
        self._element(self.SUBMIT_BTN).click()
        return self

    @allure.step("Go to products page")
    def go_to_products_page(self):
        self._element(self.CATALOG_BTN).click()
        self._wait_until(self.PRODUCT_BTN).click()
        assert self._get_title() == "Products"
        return self

    @allure.step("Check available products")
    def check_products_available(self, url, is_available_product):
        if not self.LIST_OF_PRODUCTS:
            raise ValueError("Список элементов для проверки пустой")
        for product_id in self.LIST_OF_PRODUCTS:
            product_url = url + f"index.php?route=product/product&product_id={product_id}"
            self._open_new_tab(product_url)
            if self._get_title() != "Product not found!" and not is_available_product:
                raise ValueError(f"Ожидается, что продукта c url:{product_url} нет, а он есть =)")
            elif self._get_title() == "Product not found!" and is_available_product:
                raise ValueError(f"Ожидается, что продукт с url:{product_url} есть, а его нет =)")
            self._close_last_window()
        return self

    @allure.step("Select checkbox product by id: {1}")
    def select_products_to_delete(self, product_id):
        for checkbox in self._elements(self.PRODUCT_CHECKBOX):
            if checkbox.get_attribute("value") == product_id:
                checkbox.click()

    @allure.step("Generate random list of products to future delete")
    def generate_random_list_products(self):
        # parse all id`s products from edit buttons links
        all_products = [product.get_attribute("href").split("=")[-1] for product in self._elements(self.EDIT_BTN)]
        self.LIST_OF_PRODUCTS = random.sample(
            # prevent delete items from main page(main page fixed items)
            [x for x in all_products if x not in ['30', '40', '42', '43']], k=4)
        return self

    @allure.step("Delete products by random list")
    def delete_products(self):
        for product_id in self.LIST_OF_PRODUCTS:
            self.select_products_to_delete(product_id)
        self._element(self.DELETE_BTN).click()
        self._accept_alert()
        return self

    @allure.step("Add new product with name: {1}")
    def add_new_product(self, name_product):
        # fill base inputs
        self._element(self.ADD_BTN).click()
        self._element(self.PRODUCT_NAME_INPUT).send_keys(name_product)
        self._element(self.META_TITLE_INPUT).send_keys(f"New Meta Title of {name_product}")
        # switch to data -> fill model -> save changes
        self._element(self.DATA_MENU_BTN).click()
        assert self._element(self.DATA_MENU_BTN).get_attribute("aria-expanded") == "true"
        self._element(self.INPUT_MODEL).send_keys(f"New input model of {name_product}")
        self._element(self.SAVE_BTN).click()
        # get id for new product from all product rows
        for row in self._elements(self.PRODUCTS_ROWS):
            items_on_row = self._sub_elements(row, self.ROW_ITEMS)
            if items_on_row[2].text == name_product:
                # save id to product list for future checks on availability
                self.LIST_OF_PRODUCTS = [
                    self._sub_elements(items_on_row[7], self.EDIT_BTN)[0].get_attribute("href").split("=")[-1]]
                break
        return self
