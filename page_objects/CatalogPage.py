from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .BasePage import BasePage
from elements.ProductThumbs import ProductThumbs
import allure


class CatalogPage(BasePage):
    CONTENT_NAME = (By.CSS_SELECTOR, ".row > div > h2")
    BOTTOM_COUNTER = (By.CSS_SELECTOR, ".text-right")
    SORT_SELECTOR = (By.CSS_SELECTOR, "#input-sort")
    LEFT_MENU_ACTIVE_LINK = (By.CSS_SELECTOR, ".list-group-item.active")
    LAYOUT_CLASS = (By.CSS_SELECTOR, ".product-layout")
    LIST_VIEW_BTN = (By.CSS_SELECTOR, "#list-view")

    @allure.step("Check counters of thumbs")
    def check_counters_of_thumbs(self):
        count_thumbs = len(self._elements(ProductThumbs.PRODUCT_THUMB))
        text_bottom_counter = self._get_text(self.BOTTOM_COUNTER)
        # check correct count product thumbs and bottom counter
        assert f"Showing 1 to {count_thumbs} of {count_thumbs} (1 Pages)" == text_bottom_counter
        # check counter on left menu
        assert f"{self._get_title()} ({count_thumbs})" == self._get_text(self.LEFT_MENU_ACTIVE_LINK)
        return self

    @allure.step("Check sorting")
    def check_sort(self):
        old_sort = self._elements(ProductThumbs.PRODUCT_THUMB)
        sort_selector = Select(self._element(self.SORT_SELECTOR))
        sort_selector.select_by_index(2)
        assert old_sort != self._elements(ProductThumbs.PRODUCT_THUMB)
        return self

    @allure.step("Check change layout page")
    def check_change_layout(self):
        old_layout = self._element(self.LAYOUT_CLASS).get_attribute("class").split(" ")[1]
        self._element(self.LIST_VIEW_BTN).click()
        new_layout = self._element(self.LAYOUT_CLASS).get_attribute("class").split(" ")[1]
        assert old_layout == "product-grid"
        assert new_layout == "product-list"
        return self
