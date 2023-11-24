from autofw.appium_base.mobile import Mobile
from autofw.selenium_base.selenium_driver_handler import Browser


class EIDriver:
    def __init__(self):
        self.appium_driver = None
        self.selenium_driver = None


class TestContext:
    def __init__(self):
        self.browser_drivers = []
        self.mobiles = []
        self.browser_handlers = None
        self.ei_driver = EIDriver()
        self.screenshots = None

    def set_mobiles(self, mobile_configs):
        if mobile_configs:
            for config in mobile_configs:
                mobile = Mobile(config)
                self.mobiles.append(mobile)

    @property
    def mobile(self):
        if self.mobiles:
            return self.mobiles[0]

    def launch_app(self, app=None, force_open=False, no_reset=False):
        appium_driver = self.mobile.launch_app(app, force_open, no_reset)
        self.ei_driver.appium_driver = appium_driver
        return self.ei_driver

    def terminate_mobile_apps(self):
        for mobile in self.mobiles:
            mobile.terminate_apps()

    def set_browser_handlers(self, browser_handlers):
        if browser_handlers:
            self.browser_handlers = browser_handlers

    def launch_website(self, url, browser=Browser.CHROME):
        a_browser_handler = self.browser_handlers.get(browser)
        if not a_browser_handler:
            raise RuntimeError("The given browser is not available")
        selenium_driver = a_browser_handler.get_driver()
        self.browser_drivers.append(selenium_driver)
        self.ei_driver.selenium_driver = selenium_driver
        selenium_driver.get(url)
        return self.ei_driver

    def quit_browser_drivers(self):
        for browser_driver in self.browser_drivers:
            browser_driver.quit()
