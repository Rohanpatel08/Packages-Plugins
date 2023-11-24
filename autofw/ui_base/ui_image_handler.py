from autofw.ui_base.ui_button_handler import UIButton
from autofw.ui_base.ui_element_handler import UIElementHandler


class UIImage(UIElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        # self.ButtonImpl = UIButton(locator_by, locator, driver)

    def long_press_on_element(self):
        self.ButtonImpl.long_press_on_element()

    def click_and_hold_element(self,):
        self.ButtonImpl.click_and_hold_element()

    # def tab_and_hold_element(self,):
    #     self.ButtonImpl.tap_and_hold_element()

    def release_the_element(self,):
        self.ButtonImpl.release_the_element()

    def is_image_visible(self):
        self.is_element_visible()
