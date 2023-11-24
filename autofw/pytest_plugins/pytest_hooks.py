import os
import pathlib
import pytest

from autofw.utilities.config_utils import ConfigParser
from autofw.utilities.logger import logger
from autofw.appium_base.appium_driver_handler import AppType
from autofw.selenium_base.selenium_driver_handler import URLS


def pytest_addoption(parser):
    """ Adding additional pytest command line argument definitions"""
    parser.addoption("--log_dir", action="store", default=".", help="directory location for log files")
    parser.addoption("--config", action="store", default="config.json", help="location of the config file")
    parser.addoption("--config_env", action="store", default="web_android_12",
                     help="Environment to be chosen from the config file")
    parser.addoption("--env_json", action="store", default="env_properties.json",
                     help="Json file with the App and Url information")


def pytest_cmdline_main(config):
    log_dir = config.getoption("--log_dir")
    assert pathlib.Path(log_dir).exists(), "The log directory given on the command line does not exist"
    logger.setup_logger(log_dir)

    config_file = config.getoption("--config")
    assert pathlib.Path(log_dir).exists(), "The config given on the command line does not exist"
    env = config.getoption("--config_env")
    ConfigParser.parse_args(config_file, env)

    env_json = config.getoption("--env_json")
    AppType.init_class(group="APPS", env_json=env_json)
    URLS.init_class(group="URLS", env_json=env_json)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not config.option.htmlpath:
        config.option.htmlpath = logger.run_path / 'report.html'


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    :param call:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if call.excinfo:
        logger.error(f'{item.name} FAILED WITH THE FOLLOWING TRACEBACK')
        logger.error(item.repr_failure(call.excinfo))

    if report.when == 'teardown':
        test_context = item.funcargs['test_context']
        for file_name in test_context.screenshots:
            html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % os.path.split(file_name)[-1]
            extra.append(pytest_html.extras.html(html))
        report.extra = extra
