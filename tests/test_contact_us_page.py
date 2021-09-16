from page_objects.ContactUsPage import ContactUsPage


def test_contact_us_page(browser, url):
    ContactUsPage(browser, url + "index.php?route=information/contact") \
        .compare_page_names() \
        .validate_err_fields() \
        .do_feedback() \
        .check_page_header()
