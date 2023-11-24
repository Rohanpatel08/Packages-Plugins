import time
from datetime import datetime

from autofw.appium_base.appium_element_handler import AppiumElementHandler
from autofw.appium_base.appium_feature import AppiumTextBox

from autofw.utilities.logger import logger


class AppiumDatePicker(AppiumElementHandler):
    def __init__(self, locator_by, locator, driver):
        super().__init__(locator_by, locator, driver)
        self.TextBoxImpl = AppiumTextBox(locator_by, locator, driver)

    def send_input_value(self, input_value):
        self.TextBoxImpl.send_text(input_value)

    def clear_the_text_field(
            self,
    ):
        AppiumTextBox.clear_the_text_field(self.TextBoxImpl)

    def set_date(self, date, month, year):
        self.by = By(locatorValue="android:id/date_picker_header_date", locatorType="id")
        self.el = ElementImpl(self.driver, self.by)
        dateTextView = self.el.get_element()
        # -->locator Type = ID,locator value = "android:id/date_picker_header_date"
        # #wait.until(lambda x: x.find_element(AppiumBy.ID, "android:id/date_picker_header_date"))

        self.by = By(locatorValue="android:id/date_picker_header_year", locatorType="id")
        self.el = ElementImpl(self.driver, self.by)
        yearTextView = self.el.get_element()
        # -->locator Type = ID,locator value = "android:id/date_picker_header_year"
        # wait.until(lambda x: x.find_element(AppiumBy.ID, "android:id/date_picker_header_year"))

        currentDate = (
            datetime.strptime(f"{[dateTextView.text] + [yearTextView.text]}", "['%a, %b %d', '%Y']").strftime(
                "%d %m %Y")
        ).split(" ")

        yearTextView.click()

        if (0 < date <= 31) and (0 < month <= 12) and (1900 <= year <= 2100):

            # select year
            yearString = int(currentDate[2])
            select_year = year - yearString

            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize["width"]
            screenHeight = deviceSize["height"]

            startx = screenWidth / 2
            endx = screenWidth / 2
            starty = screenHeight * 4 / 10
            endy = screenHeight * 6 / 10

            year_flag = False
            if select_year >= 0:
                while not year_flag:
                    self.by = By(locatorValue=str(year), locatorType="text")
                    self.el = ElementImpl(self.driver, self.by)
                    year_flag_1 = self.el.is_element_visible()
                    if year_flag_1:
                        self.by = By(locatorValue=str(year), locatorType="text")
                        self.el = ElementImpl(self.driver, self.by)
                        self.el.click_on_element()
                        year_flag = True
                    else:
                        self.driver.swipe(startx, endy, endx, starty)
            else:
                while not year_flag:
                    self.by = By(locatorValue=str(year), locatorType="text")
                    self.el = ElementImpl(self.driver, self.by)
                    year_flag_1 = self.el.is_element_visible()
                    if year_flag_1:
                        self.by = By(locatorValue=str(year), locatorType="text")
                        self.el = ElementImpl(self.driver, self.by)
                        self.el.click_on_element()
                        break
                    else:
                        self.driver.swipe(startx, starty, endx, endy)

            # select month
            month_string = int(currentDate[1])
            select_month = month - month_string
            if select_month >= 0:
                for i in range(select_month):
                    self.by = By(locatorValue="android:id/next", locatorType="id")
                    self.el = ElementImpl(self.driver, self.by)
                    self.el.click_on_element()  # -->ID,android:id/next
                    # wait.until(lambda x: x.find_element(AppiumBy.ID, "android:id/next")).click()
            else:
                select_month = abs(select_month)
                for i in range(select_month):
                    self.by = By(locatorValue="android:id/prev", locatorType="id")
                    self.el = ElementImpl(self.driver, self.by)
                    self.el.click_on_element()  # ID,android:id/prev
                    # wait.until(lambda x: x.find_element(AppiumBy.ID, "android:id/prev")).click()

            # select date
            select_date = int(date)
            self.by = By(locatorValue=select_date, locatorType="text")
            self.el = ElementImpl(self.driver, self.by)
            self.el.click_on_element()  # text,variable=select_date
            # wait.until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'text("{select_date}")')).click()
            time.sleep(2)

            # click ok
            self.by = By(locatorValue="OK", locatorType="text")
            self.el = ElementImpl(self.driver, self.by)
            self.el.click_on_element()  # text,OK
            # wait.until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("OK")')).click()

        else:
            print("log error")
