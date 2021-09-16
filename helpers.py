class attribute_of_element_changed:
    def __init__(self, locator, attr):
        self.locator = locator
        self.attr = attr
        self.old_attr = None

    def __call__(self, driver):
        # фиксируем текущее значение атрибута и начинаем сверять на следующем цикле
        if not self.old_attr:
            self.old_attr = driver.find_element(*self.locator).get_attribute(self.attr)
            return False

        # если текущее значение атрибута на экране не равно исходному -> True
        if self.old_attr != driver.find_element(*self.locator).get_attribute(self.attr):
            return True
        return False
