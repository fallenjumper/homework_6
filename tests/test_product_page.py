import pytest
import itertools
from page_objects.ProductPage import ProductPage


@pytest.mark.parametrize("product_id,cart_total", [(43, "2 item(s) - $1,204.00"), (44, "2 item(s) - $2,404.00")])
def test_product_page(browser, url, product_id, cart_total):
    ProductPage(browser, url + f"index.php?route=product/product&product_id={product_id}") \
        .compare_page_names() \
        .add_to_cart(cart_total) \
        .loading_picture_by_click() \
        .check_page_header()


@pytest.mark.parametrize('currency_from,currency_to', itertools.permutations(['EUR', 'GBP', 'USD'], 2))
def test_change_currency(browser, url, currency_from, currency_to):
    ProductPage(browser, url + f"index.php?route=product/product&product_id=43") \
        .set_currency(currency_from) \
        .get_price("last", currency_from) \
        .set_currency(currency_to) \
        .get_price("new", currency_to) \
        .check_new_price(currency_from, currency_to) \
        .check_tax(currency_to)
