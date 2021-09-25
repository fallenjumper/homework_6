from page_objects.BasePage import BasePage
from selenium.webdriver.common.by import By


class ProductThumbs(BasePage):
    PRODUCT_THUMB = (By.CSS_SELECTOR, ".product-thumb")

    def check_count_thumbs(self, count_thumbs):
        assert len(self._elements(self.PRODUCT_THUMB)) == count_thumbs
        return self

    def check_elements_in_thumbs(self, count_elements):
        for _ in self._elements(self.PRODUCT_THUMB):
            elements_of_product_item = _.find_elements_by_css_selector("div")
            # check count items in thimb
            assert len(elements_of_product_item) == count_elements
            assert elements_of_product_item[0].get_attribute("class") == "image"
            assert elements_of_product_item[1].get_attribute("class") == "caption"
            assert elements_of_product_item[2].get_attribute("class") == "button-group"
            # check non empty description
            assert elements_of_product_item[1].find_element_by_css_selector("p").text != ""
        return self
