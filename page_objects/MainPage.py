import allure
from selenium.webdriver.common.by import By
from helpers import attribute_of_element_changed
from .BasePage import BasePage


class MainPage(BasePage):
    TOP_IMAGE_SLIDER = (By.CSS_SELECTOR, "#slideshow0")
    TOP_SLIDER_CONTENT = (By.CSS_SELECTOR, "#slideshow0 > .swiper-wrapper")
    BOTTOM_IMAGE_SLIDER = (By.CSS_SELECTOR, "#carousel0")
    BOTTOM_SLIDER_CONTENT = (By.CSS_SELECTOR, "#carousel0 > .swiper-wrapper")

    @allure.step("Check exist base elements on main page")
    def check_base_elements(self):
        # check exist elements
        self._element(self.TOP_IMAGE_SLIDER)
        self._element(self.BOTTOM_IMAGE_SLIDER)
        return self

    @allure.step("Check slider activity")
    def is_slider_active(self):
        # check slider is not static (top/bottom)
        self._wait_until(self.TOP_SLIDER_CONTENT, attribute_of_element_changed, attr="style")
        self._wait_until(self.BOTTOM_SLIDER_CONTENT, attribute_of_element_changed, attr="style")
        return self
