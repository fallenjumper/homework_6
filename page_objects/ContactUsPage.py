from selenium.webdriver.common.by import By
from .BasePage import BasePage
import allure


class ContactUsPage(BasePage):
    CONTENT_NAME = (By.CSS_SELECTOR, ".row > div > h1")
    INPUT_NAME = (By.CSS_SELECTOR, "#input-name")
    INPUT_EMAIL = (By.CSS_SELECTOR, "#input-email")
    INPUT_ENQUIRY = (By.CSS_SELECTOR, "#input-enquiry")
    ERROR_NAME_MSG = (By.XPATH, "//div[contains(text(), 'Name must be between 3 and 32 characters!')]")
    ERROR_EMAIL_MSG = (By.XPATH, "//div[contains(text(), 'E-Mail Address does not appear to be valid!')]")
    ERROR_ENQUIRY_MSG = (By.XPATH, "//div[contains(text(), 'Enquiry must be between 10 and 3000 characters!')]")
    SUBMIT_BTN = (By.CSS_SELECTOR, ".btn.btn-primary")

    @allure.step("validate all errors on empty fields")
    def validate_err_fields(self):
        self._element(self.SUBMIT_BTN).click()
        self._element(self.ERROR_NAME_MSG)
        self._element(self.ERROR_EMAIL_MSG)
        self._element(self.ERROR_ENQUIRY_MSG)
        return self

    @allure.step("do feedback and submit")
    def do_feedback(self):
        self._element(self.INPUT_NAME).send_keys('Name')
        self._element(self.INPUT_EMAIL).send_keys("user@mail.to")
        self._element(self.INPUT_ENQUIRY).send_keys("blablablablablablabla")
        self._change_url_on_submit(self.SUBMIT_BTN)
        return self
