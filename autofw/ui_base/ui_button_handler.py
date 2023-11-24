from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains

from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UIButton(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def click(self, timeout=10, poll_frequency=1):
        element = self.wait_for_element_visible(timeout, poll_frequency)
        try:
            element.click()
            logger.info(f"Clicked on {self}")
        except Exception as exc:
            logger.warning(f"Unable to click on {self} due to exception {exc.__class__.__name__}:{exc}")

    def long_press_on_element(self, ):
        """It will find the element and long press on it.

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
            actions = TouchAction(self.driver)
            element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
            actions.long_press(element,5)  # to access the element
            actions.perform()
            logger.info(f"Successfully performed long click")
            return True
        except:
            import traceback
            logger.error(f"Unable to perform long click")
            traceback.print_exc()
            return False

    def click_and_hold_element(self, ):
        """It will find the element and click and hold it.

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
        import traceback
        try:
            element = self.wait_for_element_clickable(timeout=10, poll_frequency=1)
            # element = self.wait_for_text_to_be_present_in_element(timeout=10, poll_frequency=1, text_="aishwarya")
            action = ActionChains(self.driver)
            action.click_and_hold(element).perform()
            logger.info(f"click_and_hold_element on Element: {self}")
            return True
        except:
            logger.error(f"Unable to click_and_hold_element on Element: {self}")
            traceback.print_exc()
            return False

    # def tap_and_hold_element(self, ):
    #     """It will find the element and tap and hold it.
    #
    #     Parameters
    #     ----------
    #     locatorvalue: str
    #         The locatorvalue is the value of the element locator
    #     locatorType: str
    #         The locatorType is the type of the element locator
    #     Raises
    #     ------
    #     ElementNotVisibleException:
    #         If Element is not visible, function will raises this exception.
    #     ElementNotSelectableException:
    #         If Element can not be select, function will raises this exception
    #     NoSuchElementException:
    #         If Element can not be found, function will raises this exception
    #     Returns
    #     -------
    #     bool value
    #     """
    #     try:
    #         element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
    #         element.tap_and_hold()
    #         logger.info(f"tap_and_hold_element on Element :{self}")
    #         return True
    #     except:
    #         logger.error(f"Unable to tap_and_hold_element on Element :{self}")
    #         return False

    def release_the_element(self,):
        """It will find the element which is on hold and release that element.

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
            element = self.wait_for_element_clickable(timeout=10, poll_frequency=1)
            action = ActionChains(self.driver)
            action.release(element)
            logger.info(f"release_the_element on Element/:{self} ")
            return True
        except:
            logger.error(f"Unable to release_the_element:{self.locator_by} ")
            import traceback
            traceback.print_exc()
            return False