import os
from datetime import datetime

import pytest
from appium.webdriver.appium_service import AppiumService
from selenium import webdriver

from autofw.appium_base.appium_driver_handler import AppiumDriverHandler, AppType
from autofw.selenium_base.selenium_driver_handler import SeleniumDriverHandler, Browser
from autofw.utilities.test_context import TestContext
from autofw.utilities.config_utils import ConfigParser, ConfigKeys
from autofw.appium_base.mobile import Mobile
from autofw.utilities.logger import logger


@pytest.fixture(scope="class")
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


@pytest.fixture(scope="class")
def browser_driver():
    global D
    driver = SeleniumDriverHandler(browser=Browser.CHROME).get_driver()
    D = driver
    yield driver

    driver.quit()


@pytest.fixture(scope="class")
def test_context():
    _test_context = TestContext()

    mobile_configs = ConfigParser.extract_config(ConfigKeys.MOBILE_CONFIGS)
    _test_context.set_mobiles(mobile_configs)
    web_driver_handler = ConfigParser.extract_config(ConfigKeys.WEB_CONFIGS)
    _test_context.set_browser_handler(web_driver_handler)

    yield _test_context

    _test_context.terminate_mobile_apps()
    _test_context.quit_browser_drivers()


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
            screenshot_name = os.path.join(logger.run_path, screenshot_name)
            browser_driver.save_screenshot(screenshot_name)
            test_context.screenshots.append(screenshot_name)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'teardown':
        test_context = item.funcargs['test_context']
        for file_name in test_context.screenshots:
            html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra
