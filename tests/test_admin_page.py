from page_objects.AdminPage import AdminPage


def test_admin_page(browser, url):
    AdminPage(browser, url + "admin") \
        .check_placeholder() \
        .check_type_pass_field() \
        .check_forgotten_link_text(url) \
        .login_with("user", "wrong_pass") \
        .wait_fail_login_msg()


def test_delete_product(browser, url):
    AdminPage(browser, url + "admin") \
        .login_with("user", "bitnami") \
        .go_to_products_page() \
        .generate_random_list_products() \
        .check_products_available(url, is_available_product=True) \
        .delete_products() \
        .check_products_available(url, is_available_product=False)


def test_add_product(browser, url):
    AdminPage(browser, url + "admin") \
        .login_with("user", "bitnami") \
        .go_to_products_page() \
        .add_new_product("TST_PRODUCT") \
        .check_products_available(url, is_available_product=True)
