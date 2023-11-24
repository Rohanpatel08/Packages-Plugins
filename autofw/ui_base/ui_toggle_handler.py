from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UIToggleButton(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def toggle_the_button(self):
        """It will find the element and toggle it.

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
        bool value
        """
        try:
            # self._element = self.get_element()
            self.element = self.wait_for_element_visible()
            self.element.click()
            logger.info(
                f"toggle_the_button with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"toggle_the_button with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False

    def state_of_toggle_button(self):
        """It will find the toggle button and return its state.

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
        bool value
        """
        try:
            self.element = self.wait_for_element_visible()
            bool_result = self.element.get_attribute("checked")
            logger.info(
                f"toggle_the_button with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return bool(bool_result)
        except:
            logger.error(
                f"toggle_the_button with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )