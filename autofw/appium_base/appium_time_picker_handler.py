import time
from datetime import datetime

from autofw.appium_base.appium_element_handler import AppiumElementHandler
from autofw.appium_base.appium_feature import AppiumTextBox
from autofw.utilities.logger import logger


class AppiumTimePicker(AppiumElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        self.TextBoxImpl = AppiumTextBox(locator_by, locator, driver)

    def send_input_value(self, input_value):
        self.TextBoxImpl.send_text(input_value)

    def clear_the_text_field(
            self,
    ):
        self.TextBoxImpl.clear_the_text_field()

    def set_time(self, hour, minute):
        """It will find the raring bar and set the rating value on it.

        Parameters
        ----------
        hour: int
            the hour is the value that need to be set on clock.
        minute: int
             the min is the value that need to be set on clock
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
        # dict_key_value = {key to be press : it's keycode} every key has unique keycode to be pressed
        dict_key_value = {
            0: 7,
            1: 8,
            2: 9,
            3: 10,
            4: 11,
            5: 12,
            6: 13,
            7: 14,
            8: 15,
            9: 16,
        }
        try:
            if (0 <= hour <= 24) and (0 <= minute < 60):
                hour = f"{hour:02}"  # To convert into two digits, for Ex -> "3 = 03"
                minute = f"{minute:02}"
                if hour == "24":
                    hour = 00
                    # To convert 24-hour format into 12-hour format
                    lis_time = (
                        datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime(
                            "%I %M %p"
                        )
                    ).split(" ")
                else:
                    lis_time = (
                        datetime.strptime(f"{hour}:{minute}", "%H:%M").strftime(
                            "%I %M %p"
                        )
                    ).split(" ")
                print(lis_time)
                hour = lis_time[0]
                minute = lis_time[1]
                zone = lis_time[2]

                lis_time = list(hour) + list(minute)
                print(lis_time)
                for i in range(4):
                    time.sleep(1)
                    self.driver.press_keycode(
                        dict_key_value[int(lis_time[i])]
                    )  # To press key for inputting time
                    print(dict_key_value[int(lis_time[i])])
                self.by = By(locatorValue=zone, locatorType="text")
                self.el = ElementImpl(self.Driver, self.by)
                self.el.click_on_element()
                # self.Element.click()
                # self.click_on_element()  # <----need to give locatortype = text and locatorvalue = variable-->zone from here
                logger.info("set_time method set the time successfully")
                return True
            else:
                logger.info("set_time method only accept 00:00 to 24:59")
        except:
            logger.info("set_time method did not set the time successfully")
            return False
