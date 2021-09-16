import pytest
from page_objects.CatalogPage import CatalogPage


@pytest.mark.parametrize("catalog_id", [24, 18])
def test_catalog_page(browser, url, catalog_id):
    result_url = url + f"index.php?route=product/category&path={catalog_id}"
    CatalogPage(browser, result_url) \
        .compare_page_names() \
        .check_counters_of_thumbs() \
        .check_change_layout() \
        .check_sort() \
        .check_page_header()
