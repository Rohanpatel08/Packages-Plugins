# from ..appium_base import appium_feature
from autofw.ui_base.ui_element_handler import UIElementHandler

from autofw.utilities.logger import logger


class UIRadioButton(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        # self.ComboBoxImpl = appium_feature.AppiumComboBox(locator_by, locator, driver)

    def get_all_Radio_options(self):
        ele_r = self.find_elements()
        for rbutton in ele_r:
            rbutton_t = rbutton.get_attribute("value")
            print(rbutton_t)
            logger.info(
                f'{rbutton_t}rbutton_t'
            )


    def is_element_selected(self):
        """It will find the radio button and return its state.

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
            element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
            bool_result = element.get_attribute("checked")
            logger.info(
                f"is_element_selected with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return bool(bool_result)
        except:
            logger.error(
                f"is_element_selected with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )

    def select_using_visible_text(self, visible_text):
        self.ComboBoxImpl.select_using_visible_text(visible_text)

    def select_using_index_value(self, index_value):
        self.ComboBoxImpl.select_using_index_value(index_value)