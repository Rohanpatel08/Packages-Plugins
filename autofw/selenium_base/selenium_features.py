from selenium.webdriver import ActionChains, Keys
from contextlib import contextmanager

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select

from autofw.selenium_base.selenium_element_handler import SeleniumElement
from autofw.ui_base.ui_button_handler import UIButton
from autofw.ui_base.ui_checkbox_handler import UICheckBox
from autofw.ui_base.ui_image_handler import UIImage
from autofw.ui_base.ui_link_handler import UILink
from autofw.ui_base.ui_radiobutton_handler import UIRadioButton
from autofw.ui_base.ui_ratingbar_handler import UIRatingBar
from autofw.ui_base.ui_textbox_handler import UITextBox
from autofw.ui_base.ui_toggle_handler import UIToggleButton
from autofw.utilities.logger import logger


class SeleniumButton(SeleniumElement, UIButton):
    def submit(self):
        element = self.find_element()
        element.submit()

    def pause(self, duration):
        action = ActionChains(self.driver)
        action.pause(duration)

    def open_in_new_tab(self):
        """
        Open the given link in the element in a new tab and closes the new tab after the actions taken
        Used by putting in a for loop, all the actions to be taken on the new tab come inside the for loop
        :return:
        """
        curr_i = 0
        element = self.wait_for_element_clickable()
        try:
            element.send_keys(Keys.CONTROL + Keys.ENTER)
            curr = self.driver.current_window_handle
            windows = self.driver.window_handles
            curr_i = windows.index(curr)
            self.driver.switch_to.window(windows[curr_i + 1])
        except Exception as exc:
            logger.warning(f"Unable to open {self} in a new tab due to exception {exc.__class__.__name__}:{exc}")
        return curr_i

    @contextmanager
    def open_new_tab_and_back(self):
        curr_i = self.open_in_new_tab()
        yield
        self.driver.close()
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[curr_i])


class seleniumTextBox(SeleniumElement, UITextBox):
    """

    """


class seleniumDatePicker(SeleniumElement, UITextBox):

    def set_date(self):
        pass


class SeleniumToggle(SeleniumElement, UIToggleButton):
    """

    """


class SeleniumAlertBox(SeleniumElement, UITextBox):

    def get_alert_text(self):
        try:
            alert = Alert(self.driver)
            return alert.text

        except Exception as e:
            raise e

    def switch_to_alert_box(self):
        try:
            self.driver.switch_to.alert()
            return True
        except Exception as e:
            raise e

    def store_alert(self):
        try:
            ele = self.wait_for_alert_to_be_present()
            ele.storeAlert()

        except Exception as e:
            raise e


class SeleniumSwitchTo(SeleniumElement):

    def switch_to_frame(self, frame):
        try:
            self.driver.switch_to.frame(frame)
            return True
        except Exception as e:
            raise e

    def switch_to_active_element(self):
        try:
            self.driver.switch_to.active_element()
            return True
        except Exception as e:
            raise e

    def switch_to_window(self, window_index):
        try:
            self.driver.switch_to.window(self.driver.window_handles[window_index])
            return True
        except Exception as e:
            raise e

    def switch_to_default_window(self):
        try:
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            raise e


class SeleniumSeekBar(SeleniumElement, UIToggleButton):
    """

    """


class SeleniumRattingBar(SeleniumElement, UIRatingBar):
    """

    """


class SeleniumRadioButton(SeleniumElement, UIRadioButton):
    """

    """


class SeleniumOpenLink(SeleniumElement, UILink):
    pass


class SeleniumImage(SeleniumElement, UIImage):
    """

    """


class SeleniumDatePicker(SeleniumElement, UITextBox):
    """

    """

    def set_date(self):
        pass


class SeleniumComboBox(SeleniumElement, UITextBox):
    def select_checkbox_using_value(self, value):
        element = self.find_element()
        try:
            element.select_by_value(value)
            logger.info("Selected by combobox by value")
            return True

        except Exception as e:
            logger.error(f'Unable to select {self} by value')
            raise e

    def select_using_visible_text(self, text):
        element = self.find_element()
        try:
            multiselect = Select(element)
            multiselect.select_by_visible_text(text)
            logger.info(f'Selected the option with visible text for element {self} and text {text}')
        except Exception as e:
            logger.error(f'elected the option with visible text for element {self} and text {text}')
            raise e

    def deselect_using_visible_text(self, text):
        element = self.find_element()
        try:
            multiselect = Select(element)
            multiselect.deselect_by_visible_text(text)
            logger.info(f'Selected the option with visible text for element {self} and text {text}')
        except Exception as e:
            logger.error(f'elected the option with visible text for element {self} and text {text}')
            raise e

    def select_using_index(self, index):
        element = self.find_element()
        try:
            multiselect = Select(element)
            multiselect.select_by_index(index)
            logger.info(f'Selected the option with visible text for element {self} and index {index}')
        except Exception as e:
            logger.error(f'elected the option with visible text for element {self} and index {index}')
            raise e

    def deselect_using_index(self, index):
        element = self.find_element()
        try:
            multiselect = Select(element)
            multiselect.deselect_by_index(index)
            logger.info(f'Deselected the option with visible text for element {self} and index {index}')
        except Exception as e:
            logger.error(f'Deselected the option with visible text for element {self} and index {index}')
            raise e

    def deselect_all_options(self, ):
        element = self.find_element()
        try:
            multiselect = Select(element)
            multiselect.deselect_all()
            logger.info(f'Deselected all the options for element {self}')
        except Exception as e:
            logger.error(f'Unable to deselected all the options for element {self}')
            raise e

    def check_is_multiple(self):
        element = self.find_element()
        try:
            multiselect = Select(element)
            is_multiple = multiselect.is_multiple()
            logger.info(f'Deselected all the options for element {self}')
            return is_multiple
        except Exception as e:
            logger.error(f'Unable to deselected all the options for element {self}')
            raise e

    def get_all_options(self):
        element = self.find_element()
        try:
            multiselect = Select(element)
            is_multiple = multiselect.options
            logger.info(f'all the options for element {is_multiple}')
            return is_multiple
        except Exception as e:
            logger.error(f'Unable to get all the options for element {self}')
            raise e

    def get_first_selected_option(self):
        element = self.find_element()
        try:
            multiselect = Select(element)
            is_multiple = multiselect.first_selected_option.text
            logger.info(f'all the options for element {is_multiple}')
            return is_multiple
        except Exception as e:
            logger.error(f'Unable to get all the options for element {self}')
            raise e


class SeleniumCheckbox(SeleniumElement, UICheckBox):
    pass


class SeleniumScroll(SeleniumElement):

    def scroll_to_element(self):
        element = self.wait_for_element_presence()
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
