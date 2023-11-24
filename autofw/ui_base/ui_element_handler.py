import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from autofw.ui_base.ui_base_class import UIBaseClass
from autofw.utilities.framework_constants import TIMEOUT
from autofw.utilities.logger import logger


class UIElementHandler(UIBaseClass):
    def __init__(self, locator_by, locator, driver):
        self.locator_by = locator_by
        self.locator = locator
        self._locator_by = None
        self._locator = None
        super().__init__(driver)
        self.convert_locators()

    def convert_locators(self):
        raise NotImplementedError

    @property
    def element_by(self):
        return self._locator_by, self._locator

    def __str__(self):
        return f"<{self.__class__.__name__} by:{self.locator_by}, locator:{self._locator}>"

    def find_element(self):
        element = self.driver.find_element(self._locator_by, self._locator)
        return element

    def wait_for_element_visible(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.visibility_of_element_located(self.element_by))
        return element

    def wait_for_element_presence(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.presence_of_element_located(self.element_by))
        return element

    def wait_for_all_elements_presence(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.presence_of_all_elements_located(self.element_by))
        return element

    def wait_for_title_to_be_visible(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.title_is(self.element_by))
        return element

    def wait_for_title_contains(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.title_contains(self.element_by))
        return element

    def wait_for_alert_to_be_present(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.alert_is_present())
        return element

    def implicit_wait(self, duration):
        self.driver.implicitly_wait(duration)

    def wait_for_element_clickable(self, timeout=TIMEOUT, poll_frequency=1):
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        element = wait.until(ec.element_to_be_clickable(self.element_by))
        return element

    def wait_for_element_disappear(self, timeout=TIMEOUT, poll_frequency=1):
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency)
            wait.until(ec.invisibility_of_element(self.element_by))
            return True
        except Exception as exc:
            return False

    def find_elements(self):
        elements = self.driver.find_elements(self._locator_by, self._locator)
        return elements

    def wait_elements(self, timeout=TIMEOUT, poll_frequency=1):
        """
        Waits for the all the element corresponding to the object to be visible on page
        for timeout seconds.
        """
        wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency)
        elements = wait.until(ec.visibility_of_all_elements_located(self.element_by))
        return elements

    def is_displayed(self, timeout=TIMEOUT, poll_frequency=1):
        element = self.wait_for_element_visible(timeout, poll_frequency)
        try:
            element.is_displayed()
            return True
        except Exception as exc:
            return False

    def collect_elements(self, swipes=1, x_rel=0.5, y_start_rel=0.8, y_end_rel=0.5):
        elements = []
        for i in range(swipes):
            if i == 0:
                elements += self.wait_elements()
                for ele in elements:
                    yield ele
                continue
            time.sleep(5)
            self.swipe_vertical(x_rel=x_rel, y_start_rel=y_start_rel, y_end_rel=y_end_rel)
            time.sleep(5)
            eles = self.wait_elements()
            for ele in eles:
                if ele not in elements:
                    elements.append(ele)
                    yield ele

    def is_element_visible(self):  # Ui ele
        """It will find the element and return that the element is visible or not.

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
            print("start of is visible")
            element = self.find_element()
            is_dis = element.is_displayed()
            logger.info(f"{self}is element visible ")
            print("end of is visible")
            return is_dis
        except:
            logger.error(f"{self}is element not visible")

    def is_element_enable(self):  # ui
        """It will find the element and return that the element is eneble or not.

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
            element = self.find_element()
            is_enable = element.is_enabled()
            logger.info(f"Element {self} is enabled")
            return is_enable
        except:
            logger.error(f"Element {self} is not enabled")

    def get_attribute_value(self):  # need to make it dynamic #UI
        """It will find the element and return the attribute_value of given attribute.

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
        attribute value: string
            It will return attribute value of element's given attribute after finding it.
        """
        try:
            attribute = self.find_element().get_attribute("content-desc")
            logger.info(f"attribute value {self} located")
            return attribute
        except:
            logger.error(f"attribute value {self} located")
            return False

    def get_element_text(self):  # UI
        """It will find the element and return the text of element.

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
        fetched_text: string
            It will return text of element after finding it.
        """
        try:
            element = self.find_element()
            fetched_text = element.text
            logger.info(
                f"Text for {self} located {fetched_text}"
            )
            return fetched_text
        except:
            logger.error(f"Text for {self} not located")
            return False

    def drag_and_drop_element(self, startx, starty, endx, endy):  # ui ele
        """It will find the element and return the size of element.

        Parameters
        ----------
        startx: int
            The startx is the value of the start point coordinate for drag
        starty: int
            The starty is the value of the start point coordinate for drag
        endx: int
            The endx is the value of the start point coordinate for drop
        endy: int
            The endy is the value of the start point coordinate for drop
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
            # elementStart = self.find_element()
            # elementEnd = self.find_element()

            actions = TouchAction(self.driver)
            actions.long_press(None, startx, starty, ).move_to(None, endx, endy, ).release().perform()

            logger.info("drag_and_drop_element has been performed successful")
            return True

        except:
            logger.error("drag_and_drop_element has faced some error")
            return False

    def double_tap_on_element(self):  # UI ele
        """It will find the element and double tap on it.

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
            actions = TouchAction(self.driver)
            actions.tap(element, 2)
            actions.perform()

            logger.info(f" Taped on Element:{self}")
            return True
        except:
            logger.error(f" Unable to tap on Element:{self}")
            return False

    def double_click_on_element(self):  # ui ele
        """It will find the element and double click on it.

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
            element.double_click()
            # actions = ActionChains(self.driver)  # Aishwarya
            # actions.double_click(element)  # Aishwarya

            # element = self.find_element()
            # element.double_click()
            logger.info(f"double click on {self}")
            return True
        except:
            logger.error(f"Unable to double click on {self}")
            return False

    def tap_on_element(self):  # ui ele
        """It will find the element and tap on it.

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
            # element.tap()
            actions = TouchAction(self.driver)  # Aishwarya
            actions.tap(element)
            logger.info(f" Taped on Element {self}")
            return True
        except Exception as e:
            raise e
            # logger.error(f" Taped on Element {self}")
            # return False

    def set_value_in_element(self, value_to_set):  # ui element
        element = self.find_element()
        self.driver.set_value(element, value_to_set)

    def is_progress_bar_visible(self):
        """It will check if progress bar is visible or not.

        Returns
        -------
        bool value
        """
        try:
            visibility = self.is_element_visible()
            logger.info("s_progress_bar_visible is working fine")
            return visibility
        except:
            logger.error("is_progress_bar_visible is getting error")

    def get_element_specification(self):  # appium ele
        """It will find the element and return the specifications of element.

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
            It will return specification of element in height & width and coordinate after finding it.
        """
        try:
            element = self.find_element()
            specification = element.rect
            logger.info(f"function return the specification of given element{specification}")
            return specification
        except:
            logger.error("Unable to return the specification of given element")
            return False
