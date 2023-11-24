from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger



class UITextBox(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def send_text(self, text, timeout=10, poll_frequency=1):
        element = self.wait_for_element_visible(timeout, poll_frequency)
        try:
            element.send_keys(text)
            logger.info(f"Sent text to {self}")
        except Exception as exc:
            logger.warning(f"Unable to send text to {self} due to exception {exc.__class__.__name__}:{exc}")

    def clear_the_text_field(
            self,
    ):
        """It will find the textbox and clear its value.

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
            element.clear()
            logger.info(
                f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
            )
            return True
        except:
            logger.error(
                f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            import traceback
            traceback.print_exc()
            return False


