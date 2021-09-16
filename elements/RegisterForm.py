from selenium.webdriver.common.by import By

from page_objects.BasePage import BasePage


class RegisterForm(BasePage):
    MY_ACCOUNT_BTN = (By.CSS_SELECTOR, "a[title='My Account']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href*='account/register']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='account/login']")
    REGISTER_FORM = (By.CSS_SELECTOR, ".form-horizontal")
    INPUT_FIRSTNAME = (By.CSS_SELECTOR, "#input-firstname")
    INPUT_LASTNAME = (By.CSS_SELECTOR, "#input-lastname")
    INPUT_EMAIL = (By.CSS_SELECTOR, "#input-email")
    INPUT_TELEPHONE = (By.CSS_SELECTOR, "#input-telephone")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "#input-password")
    INPUT_CONFIRM = (By.CSS_SELECTOR, "#input-confirm")
    AGREE_CHECKBOX = (By.CSS_SELECTOR, "input[name='agree']")
    SUBMIT_BTN = (By.CSS_SELECTOR, "input[type='submit']")
    SUCCESS_REG_MSG = (By.XPATH, "//h1[contains(text(), 'Your Account Has Been Created!')]")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='account/logout']")
    SUCCESS_LOGOUT_MSG = (By.XPATH, "//h1[contains(text(), 'Account Logout')]")

    def go_to_register_page(self):
        self._element(self.MY_ACCOUNT_BTN).click()
        self._wait_until(self.REGISTER_LINK).click()
        return self

    def fill_form(self, test_user):
        self._wait_until(self.REGISTER_FORM)
        self._element(self.INPUT_FIRSTNAME).send_keys(f"{test_user}_FIRSTNAME")
        self._element(self.INPUT_LASTNAME).send_keys(f"{test_user}_LASTNAME")
        self._element(self.INPUT_EMAIL).send_keys(f"{test_user}@tst.com")
        self._element(self.INPUT_TELEPHONE).send_keys("777777777777777")
        self._element(self.INPUT_PASSWORD).send_keys("qwerty")
        self._element(self.INPUT_CONFIRM).send_keys("qwerty")
        return self

    def submit_form(self):
        self._element(self.AGREE_CHECKBOX).click()
        self._element(self.SUBMIT_BTN).click()
        self._wait_until(self.SUCCESS_REG_MSG)
        return self

    def logout(self):
        self._element(self.MY_ACCOUNT_BTN).click()
        self._wait_until(self.LOGOUT_LINK).click()
        self._wait_until(self.SUCCESS_LOGOUT_MSG)
        return self

    def go_to_login_page(self):
        self._element(self.MY_ACCOUNT_BTN).click()
        self._wait_until(self.LOGIN_LINK).click()
        return self

    def login_with(self, test_user):
        self._element(self.INPUT_EMAIL).send_keys(f"{test_user}@tst.com")
        self._element(self.INPUT_PASSWORD).send_keys("qwerty")
        self._element(self.SUBMIT_BTN).click()
        self._wait_until_not(self.INPUT_EMAIL)
        return self
