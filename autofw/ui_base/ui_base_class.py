from appium.webdriver.common.touch_action import TouchAction
from autofw.utilities.logger import logger


class UIBaseClass:
    def __init__(self, driver):
        self.driver = driver

    def swipe_vertical(self, x_rel=0.5, y_start_rel=0.8, y_end_rel=0.5):
        window_size = self.driver.get_window_size()
        max_width = window_size['width'] - 1
        max_height = window_size['height'] - 1
        start_y = int(max_height * y_start_rel)
        end_y = int(max_height * y_end_rel)
        x_coord = int(max_width * x_rel)
        self.driver.swipe(x_coord, start_y, x_coord, end_y)

    def swipe_left(self, ):  # Ui base
        """It will Swipe left on the screen.

        Returns
        -------
        bool value
        """
        try:
            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize["width"]
            screenHeight = deviceSize["height"]

            startx = screenWidth * 8 / 9
            endx = screenWidth / 9
            starty = screenHeight / 2
            endy = screenHeight / 2

            actions = TouchAction(self.driver)
            actions.long_press(None, startx, starty, ).move_to(None, endx, endy, ).release().perform()

            logger.info("swipe left has been performed successful")
            return True

        except:
            logger.error("swipe left has faced some error")
            return False

    def swipe_right(self, ):  # ui base
        """It will Swipe right on the screen.

        Returns
        -------
        bool value
        """
        try:
            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize["width"]
            screenHeight = deviceSize["height"]

            startx = screenWidth / 9
            endx = screenWidth * 8 / 9
            starty = screenHeight / 2
            endy = screenHeight / 2

            actions = TouchAction(self.driver)
            actions.long_press(None, startx, starty, ).move_to(
                None,
                endx,
                endy,
            ).release().perform()

            logger.info("swipe right has been performed successful")
            return True
        except:
            logger.error("swipe right has faced some error")
            return False

    def swipe_up(self, ):  # ui base
        """It will Swipe up on the screen.

        Returns
        -------
        bool value
        """
        try:
            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize["width"]
            screenHeight = deviceSize["height"]

            startx = screenWidth / 2
            endx = screenWidth / 2
            starty = screenHeight * 8 / 9
            endy = screenHeight / 9

            actions = TouchAction(self.driver)
            actions.long_press(None, startx, starty, ).move_to(
                None,
                endx,
                endy,
            ).release().perform()
            logger.info("swipe up has been performed successful")
            return True

        except:
            logger.error("swipe up has faced some error")
            return False

    def swipe_down(self, ):  # ui base
        """It will Swipe down on the screen.

        Returns
        -------
        bool value
        """
        try:
            deviceSize = self.driver.get_window_size()
            screenWidth = deviceSize["width"]
            screenHeight = deviceSize["height"]

            startx = screenWidth / 2
            endx = screenWidth / 2
            starty = screenHeight * 2 / 9
            endy = screenHeight * 8 / 9

            actions = TouchAction(self.driver)
            actions.long_press(None, startx, starty).move_to(None, endx, endy, ).release().perform()
            logger.info("swipe down has been performed successful")
            return True

        except:
            logger.error("swipe down has faced some error")
            return False

    def back(self):
        """
        Takes the current tab back one page
        :return: None
        """
        self.driver.back()

    def send_key(self, value):
        self.driver.press_keycode(value)



