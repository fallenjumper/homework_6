from page_objects.MainPage import MainPage
from elements.ProductThumbs import ProductThumbs
from elements.RegisterForm import RegisterForm


def test_main_page(browser, url):
    MainPage(browser, url) \
        .check_base_elements() \
        .is_slider_active() \
        .check_page_header()
    ProductThumbs(browser, url) \
        .check_count_thumbs(count_thumbs=4) \
        .check_elements_in_thumbs(count_elements=3)


def test_register_user(browser, url):
    RegisterForm(browser, url) \
        .check_page_header() \
        .go_to_register_page() \
        .fill_form("USER") \
        .submit_form() \
        .logout() \
        .go_to_login_page() \
        .login_with("USER")
