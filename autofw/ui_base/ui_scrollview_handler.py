from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.logger import logger


class UIScrollView(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def wait_for_element_to_scroll(
            self,
    ):

        """Return the element after finding it.

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
        Element: object
            It will return Element after finding it.
        """
        if self.locator_by is not None and self.locator is not None:
            _locatorType = self.locator_by.lower()
            _wait = WebDriverWait(
                self.driver,
                10,
                poll_frequency=1,
                ignored_exceptions=[
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                    NoSuchElementException,
                ],
            )
            print()
            if _locatorType == "text":
                self._element = _wait.until(
                    lambda x: x.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("{self.locator}").instance(0));',
                    )
                )
            elif _locatorType == "id":
                self._element = _wait.until(
                    lambda x: x.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f"new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().resourceid({self.locator}).instance(0));",
                    )
                )
            else:
                print("this method only work with text & id locator type")
                logger.error("this method only work with text & id locator type")

        return self._element

    def get_element_to_scroll(
            self,
    ):  # private  method

        """Return the element after finding it.

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
        Element: object
            It will return Element after finding it.
        """
        try:
            self._element = self.wait_for_element_to_scroll()
            logger.info(
                f"get_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator}"
            )
        except:
            logger.error(
                f"get_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )
            assert False
        return self._element

    def scroll_into_element_view(self):
        """Return the element after finding it.

        note:- This method only work with locator type text & id.

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
            scroll_to_element = self.get_element_to_scroll()
            print(scroll_to_element)
            logger.info("scroll_into_element_view method scroll to visible element")
            return True
        except:
            logger.error("scroll_into_element_view method getting error")
            return False

    # other option for the text scrollview------------------------
    #   find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    # f'new UiScrollable(new UiSelector()).scrollIntoView(text("{self.locator}"))'))
