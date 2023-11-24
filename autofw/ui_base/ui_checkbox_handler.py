# from ..appium_base import appium_feature
from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UICheckBox(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        # self.ComboBoxImpl = appium_feature.AppiumComboBox(locator_by, locator, driver)

    def check_mark_the_check_box(
            self,
    ):
        """It will find the checkbox and checked it.

        Parameters
        ----------
            locatorvalue: str
                The locatorvalue is the value of the element locator
            locatorType: str
                The locatorType is the type of the element locator
        raise
        ------
            ElementNotVisibleException:
                If Element is not visible, function will raise this exception.
            ElementNotSelectableException:
                If Element can not be select, function will raise this exception
            NoSuchElementException:
                If Element can not be found, function will raise this exception
        Returns
        -------
        bool value
        """
        try:
            if not self.is_check_box_checked():
                element = self.find_element()
                element.click()
            logger.info(
                f"check_mark_the_check_box with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"check_mark_the_check_box with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False

    def uncheck_the_check_box(
            self,
    ):
        """It will find the checkbox and uncheck it.

        Parameters
        ----------
            locatorvalue: str
                The locatorvalue is the value of the element locator
            locatorType: str
                The locatorType is the type of the element locator
        :raises
        ------
            ElementNotVisibleException:
                If Element is not visible, function will raise this exception.
            ElementNotSelectableException:
                If Element can not be select, function will raise this exception
            NoSuchElementException:
                If Element can not be found, function will raise this exception
        Returns
        -------
        bool value
        """
        try:
            if self.is_check_box_checked():
                element = self.find_element()
                element.click()
            logger.info(
                f"uncheck_the_check_box with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"uncheck_the_check_box with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False


    def is_check_box_checked(self):
        """It will find the checkbox and return its state.

        Parameters
        ----------
            locatorvalue: str
                The locatorvalue is the value of the element locator
            locatorType: str
                The locatorType is the type of the element locator
        raise
        ------
            ElementNotVisibleException:
                If Element is not visible, function will raise this exception.
            ElementNotSelectableException:
                If Element can not be select, function will raise this exception
            NoSuchElementException:
                If Element can not be found, function will raise this exception
        Returns
        -------
        bool value
        """
        try:
            element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
            bool_result = element.get_attribute("checked")
            logger.info(
                f"is_check_box_checked with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return bool(bool_result)
        except:
            logger.error(
                f"is_check_box_checked with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )

    def select_checkbox_using_visible_text(self, visible_text):
        self.ComboBoxImpl.select_using_visible_text(visible_text)

    def select_checkbox_using_index_value(self, index_value):
        self.ComboBoxImpl.select_using_index_value(index_value)