from autofw.utilities.test_context import EIDriver


class SeleniumBasePage:
    def __init__(self, driver):
        if isinstance(driver, EIDriver):
            self.driver = driver.selenium_driver
        else:
            self.driver = driver

    def refresh(self):
        """
        Switches the current tab
        :return: None
        """
        self.driver.refresh()

    def page_source(self):
        """
        Returns the url on the current tab
        :return: url (str)
        """
        return self.driver.page_source

    def page_title(self):
        """
        Returns the page title
        :return: page title (str)
        """
        return self.driver.title

    def back(self):
        """
        Takes the current tab back one page
        :return: None
        """
        self.driver.back()

    def forward(self):
        """
        Takes the current tab forward one page
        :return: None
        """
        self.driver.forward()

    def maximize_window(self):
        """
        Maximizes the current window
        :return: None
        """
        self.driver.maximize_window()

    def quit(self):
        """
        Closes the current window and ends the webdriver session
        :return: None
        """
        self.driver.quit()

    def close(self):
        """
        Closes the current tab while the webdriver session continues in the remaining tabs on the window
        :return: None
        """
        self.driver.close()

    def get_current_url(self):
        self.driver.current_url()

    def full_screen_window(self):
        self.driver.fullscreen_window()

    def add_cookie(self, name, value):
        self.driver.add_cookie({"name": name, "value": value})

    def get_cookie(self, name):
        try:
            cookie_info = self.driver.get_cookie(name)
            return cookie_info

        except Exception as e:
            raise e

    def get_all_cookies(self):
        try:
            cookie_info = self.driver.get_cookies()
            return cookie_info

        except Exception as e:
            raise e

    def delete_the_cookie(self, name):
        try:
            cookie_info = self.driver.delete_cookie(name)
            return cookie_info

        except Exception as e:
            raise e
