import re
from selenium import webdriver
from selenium.common import SessionNotCreatedException, WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from autofw.utilities.logger import logger
from autofw.utilities.config_utils import MetaEnvPropReader
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager


class URLS(MetaEnvPropReader):
    """

    """


class Browser:
    CHROME = 'chrome'
    FIREFOX = 'firefox'
    EDGE = 'edge'
    SAFARI = 'safari'


class PageLoadStrategy:
    NORMAL = 'normal'
    EAGER = 'eager'
    NONE = 'none'


class SeleniumDriverHandler:
    def __init__(self, browser=Browser.CHROME, page_load_strategy=PageLoadStrategy.EAGER, headless=False):
        self.driver = None
        self.browser = browser
        self.page_load_strategy = page_load_strategy
        self.headless = headless

    def get_executable_path(self):
        """
        to be downloaded from https://chromedriver.chromium.org/downloads
        :return: path to executable
        """
        path = logger.parent_dir / './venv/Lib/site-packages/autofw/selenium_base/web_drivers'
        if self.browser == Browser.CHROME:
            path = path / 'chromedriver.exe'
        elif self.browser == Browser.FIREFOX:
            path = path / 'geckodriver.exe'
        elif self.browser == Browser.EDGE:
            path = path / 'msedgedriver.exe'
        elif self.browser == Browser.SAFARI:
            path = path / '.exe'
        return path

    def get_firefox_driver(self):
        path = self.get_executable_path()
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities["pageLoadStrategy"] = self.page_load_strategy
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.tabs.remote.autostart", False)
        profile.set_preference("browser.tabs.remote.autostart.1", False)
        profile.set_preference("browser.tabs.remote.autostart.2", False)
        profile.set_preference("dom.webnotifications.enabled", False)
        options = FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')
        driver = webdriver.Firefox(executable_path=path, capabilities=capabilities,
                                   firefox_profile=profile, options=options)
        return driver

    def get_chrome_driver(self):
        path = self.get_executable_path()
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities["pageLoadStrategy"] = self.page_load_strategy
        options = ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(
                'ChromeDriverManager().install()',
                desired_capabilities=capabilities, options=options)
        return driver

    def get_edge_driver(self):
        path = self.get_executable_path()
        capabilities = webdriver.DesiredCapabilities.EDGE
        capabilities["pageLoadStrategy"] = self.page_load_strategy
        options = EdgeOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        try:
            driver = webdriver.Edge(executable_path=path, capabilities=capabilities, options=options)
            return driver
        except SessionNotCreatedException as exc:
            """
            When there is a browser and driver version mismatch, the exception raised is
            selenium.common.exceptions import SessionNotCreatedException with exc.msg as:
            'session not created: This version of ChromeDriver only supports Chrome version 97\nCurrent ' \
            'browser version is 104.0.5112.81 with binary path ' \
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            """
            version_expr = '[0-9]+.[0-9]+.[0-9]+.[0-9]+'
            result = re.search(version_expr, exc.msg)
            version = result.group()
            driver = webdriver.Edge(EdgeChromiumDriverManager().install(), capabilities=capabilities,
                                    options=options)
            return driver

    def get_safari_driver(self):
        path = self.get_executable_path()
        capabilities = webdriver.DesiredCapabilities.SAFARI
        capabilities["pageLoadStrategy"] = self.page_load_strategy
        options = SafariOptions()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        # driver = webdriver.Safari(executable_path=path, desired_capabilities=capabilities,
        #                           options=options)
        try:
            driver = webdriver.Safari(EdgeChromiumDriverManager().install(), desired_capabilities=capabilities,
                                      options=options)
            return driver
        except SessionNotCreatedException as exc:
            """
            When there is a browser and driver version mismatch, the exception raised is
            selenium.common.exceptions import SessionNotCreatedException with exc.msg as:
            'session not created: This version of ChromeDriver only supports Chrome version 97\nCurrent ' \
            'browser version is 104.0.5112.81 with binary path ' \
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            """
            version_expr = '[0-9]+.[0-9]+.[0-9]+.[0-9]+'
            result = re.search(version_expr, exc.msg)
            version = result.group()
            # driver = webdriver.Safari(EdgeChromiumDriverManager(version=version).install(), desired_capabilities=capabilities, options=options)
            return driver

    def get_driver(self):
        driver = None
        if self.browser == Browser.FIREFOX:
            driver = self.get_firefox_driver()

        if self.browser == Browser.CHROME:
            driver = self.get_chrome_driver()

        if self.browser == Browser.EDGE:
            driver = self.get_edge_driver()

        if self.browser == Browser.SAFARI:
            driver = self.get_safari_driver()

        driver.maximize_window()
        return driver
