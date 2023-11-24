from autofw.ui_base.ui_element_handler import UIElementHandler
from autofw.ui_base.ui_textbox_handler import UITextBox
from autofw.utilities.logger import logger

class UIAlertDialogBox(UITextBox):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)


    def send_input_value_in_alert_box(self, input_value):
        self.send_text(input_value)

    def accept_the_alert(self):
        """It will find the alert box and accept it.

                Returns
                -------
                bool value
                """
        try:
            self.driver.switch_to.alert.accept()
            logger.info("accept_the_alert method accept alert successfully")
            return True
        except:
            logger.error("accept_the_alert method did not accept alert successfully")
            return False

    def dismiss_the_alert(self):
        """It will find the alert box and dismiss it.

        Returns
        -------
        bool value
        """
        try:
            self.driver.switch_to.alert.dismiss()
            logger.info("dismiss_the_alert method dismiss alert successfully")
            print("alert dismiss")
            return True
        except:
            logger.error(
                "dismiss_the_alert method did not dismiss alert successfully"
            )
            return False