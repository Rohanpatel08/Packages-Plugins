import time
from contextlib import contextmanager

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from autofw.utilities.logger import logger
from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.test_context import EIDriver


class SeleniumElement(UIElementHandler):
    """
    An instance of this class maps an element on the page. It wraps around the Selenium Webdriver class.
    """
    def __init__(self, locator_by, locator, driver):
        if isinstance(driver, EIDriver):
            driver = driver.selenium_driver
        super().__init__(locator_by, locator, driver)

    def convert_locators(self):
        self._locator_by = self.locator_by
        self._locator = self.locator

    def get_attribute(self, attribute, element=None):
        """
        Gets an value of the attibute passed for the current element.
        In case, the attribute is present and has no value, it return True
        :param attribute: attribute required
        :param element:
        :return: value (str) or True or False if value not present
        """
        if element is None:
            element = self.wait_for_element_visible()
        attr_value = None
        try:
            attr_value = element.get_attribute(attribute)
            logger.info(f"Attribute {attribute}={attr_value} extracted from {self}")
        except Exception as exc:
            logger.warning(f"Attribute for {self} could not be extracted due to "
                           f"exception {exc.__class__.__name__}:{exc}")
        if attr_value == 'true':
            return True
        elif attr_value == 'false':
            return False
        else:
            return attr_value

    def get_all_attributes(self):
        element = self.wait_for_element_visible()
        try:
            attr_value = element.get_property('attributes')
            logger.info(f"Attributes {attr_value} extracted from {self}")
        except Exception as exc:
            logger.warning(f"Attribute for {self} could not be extracted due to "
                           f"exception {exc.__class__.__name__}:{exc}")

    def highlight_located_element(self, effect_time, color, border):
        element = self.wait_for_element_visible()
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                   "border: {0}px solid {1};".format(border, color))

        original_style = element.get_attribute('style')
        time.sleep(effect_time)
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)

    def get_css_value(self, css_property):
        element = self.wait_for_element_visible()
        element.value_of_css_property(css_property)

    def scroll_to_element(self):
        element = self.wait_for_element_presence()
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def set_window_size(self, width, height):
        try:
            self.driver.set_window_size()
            logger.info(f"window size set to {width, height}")
            return True
        except:
            logger.info(f"Unable to set window size to {width, height}")


class SeleniumTextBox(SeleniumElement):
    def send_text(self, text):
        """
        Clears the current text in the text field and enters new text
        :param text: text ot be written
        :return: None
        """
        element = self.wait_for_element_visible()
        try:
            element.clear()
            element.send_keys(text)
            logger.info(f"Sent text to {self}")
        except Exception as exc:
            logger.warning(f"Unable to send text to {self} due to exception {exc.__class__.__name__}:{exc}")


class SeleniumText(SeleniumElement):
    def get_text(self):
        """
        Waits for the elemetn to be visible and gets the text in the current element
        :return: text (str)
        """
        return self.get_attribute('textContent')


class SeleniumButton(SeleniumText):
    def click(self):
        """
        Waits for the element to become clickable and clicks on it
        :return: True if successfully clicked and False otherwise
        """
        element = self.wait_for_element_clickable()
        try:
            element.click()
            logger.info(f"Clicked on {self}")
        except Exception as exc:
            logger.warning(f"Unable to click on {self} due to exception {exc.__class__.__name__}:{exc}")

    def open_in_new_tab(self):
        """
        Open the given link in the element in a new tab and closes the new tab after the actions taken
        Used by putting in a for loop, all the actions to be taken on the new tab come inside the for loop
        :return:
        """
        curr_i = 0
        element = self.wait_for_element_clickable()
        try:
            element.send_keys(Keys.CONTROL + Keys.ENTER)
            curr = self.driver.current_window_handle
            windows = self.driver.window_handles
            curr_i = windows.index(curr)
            self.driver.switch_to.window(windows[curr_i + 1])
        except Exception as exc:
            logger.warning(f"Unable to open {self} in a new tab due to exception {exc.__class__.__name__}:{exc}")
        return curr_i

    def close_current_tab(self):
        self.driver.close()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[0])

    @contextmanager
    def open_new_tab_and_back(self):
        curr_i = self.open_in_new_tab()
        yield
        self.driver.close()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[curr_i])


class SeleniumLink(SeleniumButton):
    pass
