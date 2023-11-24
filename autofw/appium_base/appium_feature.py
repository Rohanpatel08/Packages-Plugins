from appium.webdriver.common.touch_action import TouchAction

from autofw.appium_base.appium_element_handler import AppiumElementHandler
from autofw.ui_base.ui_alert_dialog_box_handler import UIAlertDialogBox
from autofw.ui_base.ui_button_handler import UIButton
from autofw.ui_base.ui_checkbox_handler import UICheckBox
from autofw.ui_base.ui_image_handler import UIImage
from autofw.ui_base.ui_link_handler import UILink
from autofw.ui_base.ui_radiobutton_handler import UIRadioButton
from autofw.ui_base.ui_ratingbar_handler import UIRatingBar
from autofw.ui_base.ui_scrollview_handler import UIScrollView
from autofw.ui_base.ui_seekbar_handler import UISeekBar
from autofw.ui_base.ui_textbox_handler import UITextBox
from autofw.ui_base.ui_toggle_handler import UIToggleButton

from autofw.utilities.logger import logger


class AppiumAlertDialogBox(AppiumElementHandler, UIAlertDialogBox):
    pass


class AppiumButton(AppiumElementHandler, UIButton):
    pass


class AppiumCheckBox(AppiumElementHandler, UICheckBox):
    pass


class AppiumComboBox(AppiumElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        self.TextBoxImpl = AppiumTextBox(locator_by, locator, driver)

    def select_using_visible_text(self, visible_text):
        try:
            elements = self.find_elements()
            for i in elements:
                item_name = i.text
                if item_name == visible_text:
                    print(item_name)
                    i.click()
                    break
            logger.info(
                f"select_using_visible_text on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator}"
            )
        except:
            logger.error(
                f"select_using_visible_text on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )

    def select_using_index_value(self, index_value):
        """
        :param index_value:int
        :return:
        """
        try:
            all_element = self.wait_elements()
            all_element[int(index_value)].click()
            logger.info(
                f"select_using_index_value on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator}"
            )
        except:
            logger.error(
                f"select_using_index_value on Element with LocatorType:{self.locator_by} and with the locatorValue : {self.locator} is not working"
            )

    def send_input_value_in_combobox(self, input_value):
        self.TextBoxImpl.send_text(input_value)

    def clear_the_text_in_combobox(
            self,
    ):
        self.TextBoxImpl.clear_the_text_field()

    def long_press_key(self, value):
        self.TextBoxImpl.long_press_key(value)

    def hide_key_board(self):
        self.TextBoxImpl.hide_key_board()

    def is_keyboard_visible(self):
        self.TextBoxImpl.is_keyboard_visible()


# class AppiumDatePicker(AppiumElementHandler, UIDatePicker):
#     pass


class AppiumImage(AppiumElementHandler, UIImage):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        self.ButtonImpl = AppiumButton(locator_by, locator, driver)


class AppiumLink(AppiumElementHandler, UILink):
    pass


class AppiumRadioButton(AppiumElementHandler, UIRadioButton):
    pass


class AppiumRatingBar(AppiumElementHandler, UIRatingBar):
    pass


class AppiumScrollView(AppiumElementHandler, UIScrollView):
    pass


class AppiumSeekBar(AppiumElementHandler, UISeekBar):
    pass


class AppiumTextBox(AppiumElementHandler, UITextBox):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)

    def long_press_key(self, key_value, ):
        """It will find the key on keyboard and long press it.

        Parameters
        ----------
        key_value: int
            The key_value is the value of key which is going to use
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
            self.driver.long_press_keycode(key_value)
            logger.info("LongPress_KeyCode")
            return True
        except:
            logger.error("LongPress_KeyCode not found")
            return False

    def hide_key_board(
            self,
    ):
        """It will find the keyboard and hide it.

        Returns
        -------
        bool value
        """
        try:
            self.driver.hide_keyboard()
            logger.info("HideKeyBoard")
            return True
        except:
            import traceback
            logger.error("HideKeyBoard not found")
            traceback.print_exc()
            return False

    def is_keyboard_visible(
            self,
    ):

        """It will find that the keyboard is visible or not.

        Returns
        -------
        bool value
        """
        try:
            self.driver.is_keyboard_shown()
            logger.info("Keyboard found")
            return True
        except:
            logger.error("Keyboard_Shown not found")
            return False


class AppiumToggleButton(AppiumElementHandler, UIToggleButton):
    pass

# class AppiumTimePicker(AppiumElementHandler, UITimePicker):
#     pass
