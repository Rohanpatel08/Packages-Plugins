from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from autofw.selenium_base.selenium_driver_handler import SeleniumDriverHandler


class TestSeleniumDriverHandler:
    def test_read_data_from_excel(self, mocker):
        mock_driver = mocker.patch.object(webdriver, "Chrome")
        mock_driver_manager = mocker.patch.object(ChromeDriverManager, "install")
        handler = SeleniumDriverHandler()
        handler.get_driver()
        mock_driver_manager.assert_called_once()
        mock_driver.assert_called_once()
