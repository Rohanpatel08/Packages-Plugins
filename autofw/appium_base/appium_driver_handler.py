from appium import webdriver
from autofw.utilities.config_utils import MetaEnvPropReader


class AppTypeIndices:
    APK_PATH = 0
    ANDROID_APP_PACKAGE = 1
    ANDROID_APP_ACTIVITY = 2
    IOS_BUNDLE_ID = 3
    IOS_APP_PACKAGE = 4

    @classmethod
    def start_activity_args(cls, app, mobile) -> list:
        if mobile.platform_name == MobilePlatforms.ANDROID:
            return [app[AppTypeIndices.ANDROID_APP_PACKAGE], app[AppTypeIndices.ANDROID_APP_ACTIVITY]]
        elif mobile.platform_name == MobilePlatforms.IOS:
            return [app[AppTypeIndices.IOS_BUNDLE_ID], app[AppTypeIndices.IOS_APP_PACKAGE]]

    @classmethod
    def terminate_app_args(cls, app, mobile) -> list:
        if mobile.platform_name == MobilePlatforms.ANDROID:
            return [app[AppTypeIndices.ANDROID_APP_PACKAGE]]
        elif mobile.platform_name == MobilePlatforms.IOS:
            return [app[AppTypeIndices.IOS_BUNDLE_ID]]


class AppType(MetaEnvPropReader):
    """
    Run the phone in the emulator or connect to the computer
    run the app and run this command to get the app_package and app_activity
    adb shell dumpsys window windows
    """


class MobilePlatforms:
    ANDROID = 'Android'
    IOS = 'IOS'


class AppiumDriverHandler:
    def __init__(self, mobile, app=None, url_protocol='http', url_path='/wd/hub'):
        self.mobile = mobile
        self.starting_app = app
        self.address = mobile.address
        self.port = mobile.port
        self.capabilities = dict()
        self.url_protocol = url_protocol
        self.url_path = url_path
        self.construct_capabilities()

    def add_app(self, app):
        desired_caps = dict()
        if app[AppTypeIndices.APK_PATH]:
            desired_caps['app'] = app[AppTypeIndices.APK_PATH]
        elif self.mobile.platform_name == MobilePlatforms.ANDROID:
            desired_caps['appPackage'] = app[AppTypeIndices.ANDROID_APP_PACKAGE]
            desired_caps['appActivity'] = app[AppTypeIndices.ANDROID_APP_ACTIVITY]
        elif self.mobile.platform_name == MobilePlatforms.IOS:
            desired_caps['bundleId'] = app[AppTypeIndices.IOS_BUNDLE_ID]
            desired_caps['appPackage'] = app[AppTypeIndices.IOS_APP_PACKAGE]
        self.capabilities.update(desired_caps)

    def construct_android_capabilities(self):
        mobile = self.mobile
        desired_caps = dict()
        desired_caps['platformName'] = mobile.platform_name
        desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['platformVersion'] = mobile.platform_version
        desired_caps['deviceName'] = mobile.device_name
        if mobile.udid:
            desired_caps['udid'] = mobile.udid
        desired_caps['adbExecTimeout'] = 60000
        desired_caps['uiautomator2ServerInstallTimeout'] = 60000
        desired_caps['uiautomator2ServerLaunchTimeout'] = 60000
        if self.starting_app:
            self.add_app(self.starting_app)
        self.capabilities.update(desired_caps)

    def construct_ios_capabilities(self):
        mobile = self.mobile
        desired_caps = dict()
        if self.starting_app:
            self.add_app(self.starting_app)
        desired_caps['autoWebview'] = 'false'
        desired_caps['newCommandTimeout'] = 36000
        desired_caps['wdaLocalPort'] = int(mobile.wda_local_port)
        desired_caps['automationName'] = 'XCUITest'
        desired_caps['noReset'] = True
        desired_caps['fullReset'] = False
        desired_caps['wdaStartupRetries'] = 3

        self.capabilities.update(desired_caps)

    def construct_capabilities(self):
        mobile = self.mobile
        desired_caps = dict()
        desired_caps['platformName'] = mobile.platform_name
        desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['platformVersion'] = mobile.platform_version
        desired_caps['deviceName'] = mobile.device_name
        if mobile.udid:
            desired_caps['udid'] = mobile.udid
        self.capabilities.update(desired_caps)

        if self.mobile.platform_name == MobilePlatforms.ANDROID:
            self.construct_android_capabilities()
        elif self.mobile.platform_name == MobilePlatforms.IOS:
            self.construct_ios_capabilities()

    def update_capabilities(self, **kwargs):
        self.capabilities.update(kwargs)

    @property
    def url(self):
        _url = f"{self.url_protocol}://{self.address}:{self.port}{self.url_path}" #self.port OR
        return _url

    def get_driver(self, app=None, no_reset=False):
        desired_caps = dict()
        if no_reset:
            desired_caps['noReset'] = no_reset
        if app:
            self.add_app(app)
        self.update_capabilities(**desired_caps)
        driver = webdriver.Remote(self.url, self.capabilities)

        return driver
