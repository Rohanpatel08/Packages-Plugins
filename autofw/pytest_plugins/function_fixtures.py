import os
import pytest
from autofw.utilities.logger import logger
from autofw.selenium_base.selenium_driver_handler import SeleniumDriverHandler, Browser
from appium.webdriver.appium_service import AppiumService
from autofw.appium_base.appium_driver_handler import AppiumDriverHandler, AppType
from autofw.appium_base.mobile import Mobile
from autofw.utilities.config_utils import ConfigParser, ConfigKeys


@pytest.fixture
def driver_setup():
    global D
    appium_service = AppiumService()
    appium_service.start(args=['--address', '127.0.0.1', '-p', str(4728), '--base-path', '/wd/hub'])
    mobile_configs = ConfigParser.extract_config(ConfigKeys.MOBILE_CONFIGS)
    mobile = Mobile(mobile_configs[0])
    driver = AppiumDriverHandler(mobile, AppType.KWAD).get_driver()
    D = driver
    yield driver
    try:
        driver.quit()
    finally:
        appium_service.stop()


@pytest.fixture
def browser_driver():
    global D
    driver = SeleniumDriverHandler(browser=Browser.CHROME).get_driver()
    D = driver
    yield driver

    driver.quit()


@pytest.fixture(autouse=True)
def take_screenshot(request, test_context):
    test_context.screenshots = []
    yield
    if request.session.testsfailed:
        test_name = request.node.name
        for mobile in test_context.mobiles:
            mobile_driver = mobile.driver
            udid = mobile.udid
            if mobile_driver:
                screenshot_name = test_name + '_' + udid + '.png'
                screenshot_name = os.path.join(logger.run_path, screenshot_name)
                mobile_driver.save_screenshot(screenshot_name)
                test_context.screenshots.append(screenshot_name)
        for browser_driver in test_context.browser_drivers:
            screenshot_name = test_name + '_' + 'chrome.png'
            screenshot_name = (logger.run_path / screenshot_name).absolute()
            browser_driver.save_screenshot(screenshot_name)
            test_context.screenshots.append(screenshot_name)
