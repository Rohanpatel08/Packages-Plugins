from appium.webdriver.common.touch_action import TouchAction
from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UISeekBar(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def status_of_seek_bar(self):
        """It will find the seek bar and return its state.

        Parameters
        ----------
        locatorvalue: str
            The locatorvalue is the value of the element locator
        locatorType: str
            The locatorType is the type of the element locator
        Raises
        ------
        ElementNotVisibleException:
            If Element is not visible, function will raises this exception.
        ElementNotSelectableException:
            If Element can not be select, function will raises this exception
        NoSuchElementException:
            If Element can not be found, function will raises this exception
        Returns
        -------
        seekbar_state : int
        """
        try:
            self.element = self.wait_for_element_visible()
            seekbar_state = self.element.get_attribute("text")
            logger.info(
                f"status_of_seek_bar {seekbar_state} is with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return seekbar_state
        except:
            logger.error(
                f"status_of_seek_bar with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False


    def set_value_of_seek_bar(self, value_to_set):
        """It will find the seek bar and set the argument value on it.

        Parameters
        ----------
        locatorvalue: str
            The locatorvalue is the value of the element locator
        locatorType: str
            The locatorType is the type of the element locator
        value_to_set: str
            the value_to_set is the value that need to be set on seekbar
        Raises
        ------
        ElementNotVisibleException:
            If Element is not visible, function will raises this exception.
        ElementNotSelectableException:
            If Element can not be select, function will raises this exception
        NoSuchElementException:
            If Element can not be found, function will raises this exception
        Returns
        -------
        bool value
        """
        try:
            startX = self.get_element_specification()["x"]
            startY = self.get_element_specification()["y"] + (self.get_element_specification()["height"]/2)
            endX = (self.get_element_specification()["width"] / 100) * (int(value_to_set) + 1)
            endY = self.get_element_specification()["y"] + (self.get_element_specification()["height"]/2)
            actions = TouchAction(self.driver)
            actions.long_press(None, startX, startY).move_to(None, endX, endY).release().perform()

            logger.info(
                f"set_value_of_seek_bar with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"set_value_of_seek_bar with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False
