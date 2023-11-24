from autofw.appium_base.appium_driver_handler import AppTypeIndices, AppiumDriverHandler
from autofw.appium_base.appium_service_utility import AppiumServiceUtility


class MobileConfig:
    """
    Made temporarily for the config to be in place
    """
    def __init__(self, platform_name, platform_version, device_name, udid, address='127.0.0.1', emulated=True):
        self.platform_name = platform_name
        self.platform_version = platform_version
        self.device_name = device_name
        self.udid = udid
        self.address = address
        self.emulated = emulated


class Mobile:
    def __init__(self, mobile_config):
        self.platform_name = mobile_config.platform_name
        self.platform_version = mobile_config.platform_version
        self.device_name = mobile_config.device_name
        self.udid = mobile_config.udid
        self.port = 0
        self.emulated = mobile_config.emulated
        self.address = mobile_config.address
        self._current_app = None
        self.driver = None
        self._open_apps = list()  # list of open apps, useful for when the all the apps need to be terminated
        self.appium_service = None

    def start_appium_server(self):
        if self.appium_service is None:
            self.appium_service = AppiumServiceUtility(self.address)
            self.port = self.appium_service.select_port()
            self.appium_service.start(port=self.port)

    def stop_appium_server(self):
        if self.appium_service:
            self.appium_service.stop()

    def launch_app(self, app=None, force_open=False, no_reset=False):
        driver = None
        self.start_appium_server()
        if self.driver is None:
            driver = AppiumDriverHandler(self, app=app).get_driver(no_reset=no_reset)
            self._current_app = app
            self.driver = driver
            self._open_apps.append(app)
        elif self._current_app != app or app == self._current_app and force_open:
            driver = self.driver
            try:
                driver.start_activity(*AppTypeIndices.start_activity_args(app, self))
            except Exception as exc:
                self.stop_appium_server()
            self._current_app = app
            if app not in self._open_apps:
                self._open_apps.append(app)
        elif app == self._current_app:
            driver = self.driver
        return driver

    def terminate_apps(self):
        exception = None
        try:
            for app in self._open_apps:
                self.driver.terminate_app(*AppTypeIndices.terminate_app_args(app, self))
            if self.driver:
                self.driver.quit()
        except Exception as exc:
            exception = exc
        finally:
            self.stop_appium_server()
            if exception:
                raise exception
        self._current_app = None
        self._open_apps = []

    def terminate_app(self, app):
        self.driver.terminate_app(*AppTypeIndices.terminate_app_args(app, self))
        if app == self._current_app:
            self._current_app = None
        if app in self._open_apps:
            self._open_apps.remove(app)
