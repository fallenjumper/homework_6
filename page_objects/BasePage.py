import selenium.webdriver.remote.webelement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from elements.HeaderElements import HeaderElements


class BasePage:

    def __init__(self, browser, page_url):
        self.browser = browser
        self.browser.get(page_url)
        self.wait_timeout = 5

    def _accept_alert(self):
        return self.browser.switch_to.alert.accept()

    def _open_new_tab(self, url):
        self.browser.execute_script('window.open();')
        self.browser.switch_to.window(window_name=self.browser.window_handles[-1])
        self.browser.get(url)

    def _close_last_window(self):
        if len(self.browser.window_handles) > 1:
            self.browser.switch_to.window(window_name=self.browser.window_handles[-1])
            self.browser.close()
            self.browser.switch_to.window(window_name=self.browser.window_handles[0])
        else:
            raise ValueError("Opened only one tab. Can't close.")

    def _wait_until(self, locator, target_condition=EC.visibility_of_element_located, **kwargs):
        try:
            return WebDriverWait(self.browser, self.wait_timeout).until(target_condition(locator, **kwargs))
        except TimeoutException:
            raise AssertionError(f"Can`t find element by locator: {locator}")

    def _wait_until_not(self, locator, target_condition=EC.visibility_of_element_located, **kwargs):
        try:
            return WebDriverWait(self.browser, self.wait_timeout).until_not(target_condition(locator, **kwargs))
        except TimeoutException:
            raise AssertionError(f"Element did not leave the screen for a timeout: {self.wait_timeout}s")

    def _change_url_on_submit(self, btn_locator: tuple):
        old_url = self.browser.current_url
        self._element(btn_locator).click()
        self._wait_until(old_url, EC.url_changes)

    def _element(self, locator: tuple):
        try:
            return self.browser.find_element(*locator)
        except Exception as e:
            raise ValueError(f"Can`t find element by locator: {locator} with exception: {e}")

    def _elements(self, locator: tuple, number_of_element=None):
        result_elements = self.browser.find_elements(*locator)
        if not result_elements:
            raise ValueError(f"Can`t find elements by locator: {locator}")
        if number_of_element:
            return result_elements[number_of_element]
        return result_elements

    def _sub_elements(self, root_elements: selenium.webdriver.remote.webelement.WebElement, locator: tuple):
        result_elements = root_elements.find_elements(*locator)
        if not result_elements:
            raise ValueError(f"Can`t find elements by locator: {locator}")
        return result_elements

    def _get_text(self, locator: tuple):
        return self._element(locator).text

    def _element_by_attribute_value(self, locator: tuple, attribute, attribute_value):
        for elem in self._elements(locator):
            if elem.get_attribute(attribute) == attribute_value:
                return elem
        raise ValueError(f"Не удалось найти элемент, у которого аттрибут {attribute} равен {attribute_value}")

    def _get_title(self):
        return self.browser.title

    # check similar title, page_name, product_name
    def compare_page_names(self):
        page_name = self._elements(HeaderElements.PAGE_NAME, 1).text
        content_name = self._get_text(self.CONTENT_NAME)
        assert page_name == content_name == self._get_title()
        return self

    def check_page_header(self):
        # check placeholder on search box
        assert self._element(HeaderElements.SEARCH_TEXTBOX).get_attribute("placeholder") == "Search"

        # check list menu elements
        menu_elements = self._elements(HeaderElements.TOP_MENU_LIST)
        target_list_menu = ["Desktops", "Laptops & Notebooks", "Components", "Tablets", "Software", "Phones & PDAs",
                            "Cameras",
                            "MP3 Players"]
        current_list_menu = [i.text for i in menu_elements]
        assert target_list_menu == current_list_menu

        # check default not visibility items under menu
        dropdown_top_menu_lst = self._elements(HeaderElements.TOP_MENU_DROPDOWN_LIST)
        if not dropdown_top_menu_lst:
            raise ValueError("Не найден элемент")
        for element in dropdown_top_menu_lst:
            assert not element.is_displayed()
        return self
