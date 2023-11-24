from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UIRatingBar(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def get_current_rating(self):
        """It will find the rating bar and return its current rating.

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
        current_rating : float
        """
        try:
            self.element = self.wait_for_element_visible()
            current_rating = self.element.get_attribute("text")
            logger.info(
                f"get_current_rating={current_rating} with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return current_rating
        except:
            logger.error(
                f"get_current_rating with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False

    def set_rating(self, rating_value):
        """It will find the raring bar and set the rating value on it.

        Parameters
        ----------
        locatorvalue: str
            The locatorvalue is the value of the element locator
        locatorType: str
            The locatorType is the type of the element locator
        rating_value: float
            the rating_value is the value that need to be set on rating bar.
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
            self.driver.set_value(self.element, 2 * rating_value)
            logger.info(
                f"set_value_of_seek_bar with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"set_value_of_seek_bar with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            return False