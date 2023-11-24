import base64
import os
import time

from autofw.ui_base.ui_base_class import UIBaseClass
from autofw.utilities.logger import logger
from autofw.utilities.test_context import EIDriver
from autofw.appium_base.appium_driver_handler import MobilePlatforms


class AppiumBasePage(UIBaseClass):
    def __init__(self, driver):
        super().__init__(driver)
        if isinstance(driver, EIDriver):
            self.driver = driver.appium_driver
        else:
            self.driver = driver

        if self.platform_name == MobilePlatforms.ANDROID:
            self.platform_android = True
        else:
            self.platform_android = False

    @property
    def platform_name(self):
        return self.driver.capabilities.get("desired").get("platformName")

    def take_screenshot(self, name):
        file_name = name + "_" + (time.strftime("%d_%m_%y_%H_%M_%S")) + ".png"
        directory = "..\\screenshots\\ "
        path = directory + file_name
        try:
            self.driver.save_screenshot(path)
            logger.info("Screenshot save to path : " + path)
        except Exception as exc:
            logger.warning(f"Unable to save Screenshot {path} due to exception {exc.__class__.__name__}:{exc}")

    def key_code(self, value):
        self.driver.press_keycode(value)

    def start_video(self, ):
        self.driver.start_recording_screen()
        self.video_name = self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")

    def stop_video(self):
        video_rawdata = self.driver.stop_recording_screen()
        filepath = os.path.join(logger.run_path, self.video_name + ".mp4")
        with open(filepath, "wb") as vd:
            vd.write(base64.b64decode((video_rawdata)))
