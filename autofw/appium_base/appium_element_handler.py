from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains

from autofw.utilities.logger import logger
from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.utilities.test_context import EIDriver


class LocatorBy(AppiumBy):
    INDEX = "index"
    TEXT = "text"
    CONTENT_DESCRIPTION = "content_description"


class AppiumElementHandler(UIElementHandler):
    SCROLL_LOCATOR = 'new UiScrollable(new UiSelector()).scrollIntoView({})'

    def __init__(self, locator_by, locator,  driver):
        if isinstance(driver, EIDriver):
            driver = driver.appium_driver
        super().__init__(locator_by, locator, driver)
        self._scroll_element_by = None

    def convert_locators(self):
        if self.locator_by == LocatorBy.INDEX:
            self._locator_by = LocatorBy.ANDROID_UIAUTOMATOR
            self._locator = "UiSelector().index(%d)" % int(self.locator)

        elif self.locator_by == LocatorBy.TEXT:
            self._locator_by = LocatorBy.ANDROID_UIAUTOMATOR
            self._locator = 'text("%s")' % self.locator

        elif self.locator_by == LocatorBy.CONTENT_DESCRIPTION:
            self._locator_by = LocatorBy.ANDROID_UIAUTOMATOR
            self._locator = 'UiSelector().description("%s")' % self.locator

        else:
            self._locator_by = self.locator_by
            self._locator = self.locator

    @property
    def scroll_element_by(self):
        if self._scroll_element_by is None:
            locator_by = LocatorBy.ANDROID_UIAUTOMATOR
            locator = None
            if self.locator_by == LocatorBy.ID:
                locator = self.SCROLL_LOCATOR.format(f'resourceId("{self.locator}")')
            elif self.locator_by == LocatorBy.CLASS_NAME:
                locator = self.SCROLL_LOCATOR.format(f'className("{self.locator}")')
            elif self.locator_by == LocatorBy.INDEX:
                locator = self.SCROLL_LOCATOR.format(f'index({self.locator})')
            elif self.locator_by == LocatorBy.CONTENT_DESCRIPTION:
                locator = self.SCROLL_LOCATOR.format(f'description("{self.locator}")')
            elif self.locator_by == LocatorBy.TEXT:
                locator = self.SCROLL_LOCATOR.format(f'text("{self.locator}")')
            self._scroll_element_by = locator_by, locator

        return self._scroll_element_by

    def scroll_into_view(self):
        try:
            element = self.driver.find_element(*self.scroll_element_by)
            return element
        except Exception as e:
            raise e

    def get_tag_name(self):  # appium element Handler

        """It will find the element and return the tag name of it.

        raises
        ------
        ElementNotVisibleException:
            If Element is not visible, function will raise this exception.
        ElementNotSelectableException:
            If Element can not be select, function will raise this exception
        NoSuchElementException:
            If Element can not be found, function will raise this exception
        Returns
        -------
        tagname: string
            It will return tagname of element after finding it.
        """
        try:

            element = self.find_element()

            tagname = element.tag_name
            logger.info(f"get_tag_name on {tagname} found")
            return tagname
        except Exception as e:
            raise e
            # logger.error(f"get_tag_name on {self} not found")
            # return False

    def click_on_element(self):  # appium element handler

        """It will find the element and click on it.

        raises
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
            element = self.find_element()
            element.click()
            logger.info(f"clicked on element :{self}")
            return True
        except:
            logger.error(f"Unable clicked on element :{self}")
            return False

    def get_size_of_element(self):  # appium ele
        """It will find the element and return the size of element.

        raises
        ------
        ElementNotVisibleException:
            If Element is not visible, function will raise this exception.
        ElementNotSelectableException:
            If Element can not be select, function will raise this exception
        NoSuchElementException:
            If Element can not be found, function will raise this exception
        Returns
        -------
        specification: dict
            It will return height & width of element after finding it.
        """
        try:
            element = self.find_element()
            size_of_element = element.size
            logger.info(f"function return the size of given element{size_of_element}")
            return size_of_element
        except:
            logger.error("Unable to return the size of given element")
            return False

    def swipe_by_coordinate(self, start_x, start_y, end_x, end_y):  # appium ele handler
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y)
            return True
        except:
            return False

# '''
# commented
# '''
# class AppiumButton(AppiumElementHandler):
#     def __init__(self, locator_by, locator, driver):
#         super().__init__(locator_by, locator, driver)
#
#     def click(self, timeout=10, poll_frequency=1):
#         element = self.wait_for_element_visible(timeout, poll_frequency)
#         try:
#             element.click()
#             logger.info(f"Clicked on {self}")
#         except Exception as exc:
#             logger.warning(f"Unable to click on {self} due to exception {exc.__class__.__name__}:{exc}")
#
#     def long_press_on_element(
#             self,
#     ):
#         """It will find the element and long press on it.
#
#         Parameters
#         ----------
#         locatorvalue: str
#             The locatorvalue is the value of the element locator
#         locatorType: str
#             The locatorType is the type of the element locator
#         Raises
#         ------
#         ElementNotVisibleException:
#             If Element is not visible, function will raises this exception.
#         ElementNotSelectableException:
#             If Element can not be select, function will raises this exception
#         NoSuchElementException:
#             If Element can not be found, function will raises this exception
#         Returns
#         -------
#         bool value
#         """
#         try:
#             # self.get_element()
#             actions = TouchAction(self.driver)
#             element = self.wait_for_element_clickable(timeout=10, poll_frequency=1)
#             actions.long_press(element)  # to access the element
#             actions.perform()
#             logger.info(
#                 # f"longPrass on Element with LocatorType: {self.locator_by} and with the locatorValue : {self.locator}"
#                 f"Succesfull long click"
#             )
#             return True
#         except:
#             import traceback
#             logger.error(
#                 # f"longPrass on Element with LocatorType: {self.locator_by} and with the locatorValue : {self.locator} is not working"
#                 f"UNSuccesfull long click"
#             )
#             traceback.print_exc()
#             return False
#
#     def click_and_hold_element(
#             self,
#     ):
#         """It will find the element and click and hold it.
#
#         Parameters
#         ----------
#         locatorvalue: str
#             The locatorvalue is the value of the element locator
#         locatorType: str
#             The locatorType is the type of the element locator
#         Raises
#         ------
#         ElementNotVisibleException:
#             If Element is not visible, function will raises this exception.
#         ElementNotSelectableException:
#             If Element can not be select, function will raises this exception
#         NoSuchElementException:
#             If Element can not be found, function will raises this exception
#         Returns
#         -------
#         bool value
#         """
#         import traceback
#         try:
#             # self._element = self.get_element()
#             element = self.wait_for_element_clickable(timeout=10, poll_frequency=1)
#             action = ActionChains(self.driver)
#             action.click_and_hold(element).perform()
#             logger.info(
#                 f"click_and_hold_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
#             )
#             return True
#         except:
#             logger.error(
#                 f"click_and_hold_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
#             )
#             traceback.print_exc()
#             return False
#
#     # def tap_and_hold_element(
#     #         self,
#     # ):
#     #     """It will find the element and tap and hold it.
#     #
#     #     Parameters
#     #     ----------
#     #     locatorvalue: str
#     #         The locatorvalue is the value of the element locator
#     #     locatorType: str
#     #         The locatorType is the type of the element locator
#     #     Raises
#     #     ------
#     #     ElementNotVisibleException:
#     #         If Element is not visible, function will raises this exception.
#     #     ElementNotSelectableException:
#     #         If Element can not be select, function will raises this exception
#     #     NoSuchElementException:
#     #         If Element can not be found, function will raises this exception
#     #     Returns
#     #     -------
#     #     bool value
#     #     """
#     #     try:
#     #         element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
#     #         element.tap_and_hold()
#     #
#     #
#     #         logger.info(
#     #             f"tap_and_hold_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
#     #         )
#     #         return True
#     #     except:
#     #         logger.error(
#     #             f"tap_and_hold_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
#     #         )
#     #         return False
#
#     def release_the_element(
#             self,
#     ):
#         """It will find the element which is on hold and release that element.
#
#         Parameters
#         ----------
#         locatorvalue: str
#             The locatorvalue is the value of the element locator
#         locatorType: str
#             The locatorType is the type of the element locator
#         Raises
#         ------
#         ElementNotVisibleException:
#             If Element is not visible, function will raises this exception.
#         ElementNotSelectableException:
#             If Element can not be select, function will raises this exception
#         NoSuchElementException:
#             If Element can not be found, function will raises this exception
#         Returns
#         -------
#         bool value
#         """
#         try:
#             # self._element = self.get_element()
#             element = self.wait_for_element_clickable(timeout=10, poll_frequency=1)
#             action = ActionChains(self.driver)
#             action.release(element)
#             logger.info(
#                 f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
#             )
#             return True
#         except:
#             logger.error(
#                 f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
#             )
#             import traceback
#             traceback.print_exc()
#             return False

class CoOrdinates(AppiumElementHandler):
    # def __init__(self, start_x, start_y, end_x, end_y):
    #     self.start_x = start_x
    #     self.start_y = start_y
    #     self.end_x = end_x
    #     self.end_y = end_y

    def swipe_by_co(self, start_x, start_y, end_x, end_y):
        self.swipe_by_coordinate(start_x, start_y, end_x, end_y)
    # START_X =
    # START_Y =
    # END_X =
    # END_Y =


# class AppiumLink(AppiumButton):
#     def go_to_link(self, input_link):
#         """It will open the link which is inputted.
#
#         Parameters
#         ----------
#         input_link: str
#             The input_link is the link to be open
#
#         Returns
#         -------
#         bool value
#         """
#         try:
#             self.driver.get(input_link)
#             logger.info("go_to_link method open link which is inputted")
#             return True
#         except:
#             logger.error(
#                 "go_to_link method can't able to open link which is inputted"
#             )
#             return False


# class AppiumTextBox(AppiumElementHandler):
#     def __init__(self, locator_by, locator, driver):
#         super().__init__(locator_by, locator, driver)
#
#     def send_text(self, text, timeout=10, poll_frequency=1):
#         element = self.wait_for_element_visible(timeout, poll_frequency)
#         try:
#             element.send_keys(text)
#             logger.info(f"Sent text to {self}")
#         except Exception as exc:
#             logger.warning(f"Unable to send text to {self} due to exception {exc.__class__.__name__}:{exc}")
#
#     def clear_the_text_field(
#             self,
#     ):
#         """It will find the textbox and clear its value.
#
#         Parameters
#         ----------
#         locatorvalue: str
#             The locatorvalue is the value of the element locator
#         locatorType: str
#             The locatorType is the type of the element locator
#         raise
#         ------
#         ElementNotVisibleException:
#             If Element is not visible, function will raise this exception.
#         ElementNotSelectableException:
#             If Element can not be select, function will raise this exception
#         NoSuchElementException:
#             If Element can not be found, function will raise this exception
#         Returns
#         -------
#         bool value
#         """
#         try:
#             element = self.wait_for_element_visible(timeout=10, poll_frequency=1)
#             element.clear()
#             logger.info(
#                 f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} "
#             )
#             return True
#         except:
#             logger.error(
#                 f"release_the_element on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
#             )
#             import traceback
#             traceback.print_exc()
#             return False
#
#
#     def long_press_key(
#             self,
#             key_value,
#     ):
#         """It will find the key on keyboard and long press it.
#
#         Parameters
#         ----------
#         key_value: int
#             The key_value is the value of key which is going to use
#         raise
#         ------
#         ElementNotVisibleException:
#             If Element is not visible, function will raise this exception.
#         ElementNotSelectableException:
#             If Element can not be select, function will raise this exception
#         NoSuchElementException:
#             If Element can not be found, function will raise this exception
#         Returns
#         -------
#         bool value
#         """
#         try:
#             self.driver.long_press_keycode(key_value)
#             logger.info("LongPress_KeyCode")
#             return True
#         except:
#             logger.error("LongPress_KeyCode not found")
#             return False
#
#     def hide_key_board(
#             self,
#     ):
#         """It will find the keyboard and hide it.
#
#         Returns
#         -------
#         bool value
#         """
#         try:
#             self.driver.hide_keyboard()
#             logger.info("HideKeyBoard")
#             return True
#         except:
#             import traceback
#             logger.error("HideKeyBoard not found")
#             traceback.print_exc()
#             return False
#
#     def is_keyboard_visible(
#             self,
#     ):
#
#         """It will find that the keyboard is visible or not.
#
#         Returns
#         -------
#         bool value
#         """
#         try:
#             self.driver.is_keyboard_shown()
#             logger.info("Keyboard found")
#             return True
#         except:
#             logger.error("Keyboard_Shown not found")
#             return False

# class AppiumImageImpl(AppiumButton):
#     def __init__(self, locator_by, locator, driver):
#         super().__init__(locator_by, locator, driver)
#
#     def long_press_on_element(self):
#         self.long_press_on_element()
#
#     def click_and_hold_element(
#             self,
#     ):
#         self.ButtonImpl.click_and_hold_element()
#
#     def tab_and_hold_element(
#             self,
#     ):
#         self.ButtonImpl.tap_and_hold_element()
#
#     def release_the_element(
#             self,
#     ):
#         self.ButtonImpl.release_the_element()
#
#     def is_image_visible(self):
#         self.ElementImpl.is_element_visible()

    # def img_


