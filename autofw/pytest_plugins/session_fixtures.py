import pytest
from autofw.utilities.test_context import TestContext
from autofw.utilities.config_utils import ConfigParser, ConfigKeys


@pytest.fixture(scope="session")
def test_context():
    _test_context = TestContext()

    mobile_configs = ConfigParser.extract_config(ConfigKeys.MOBILE_CONFIGS)
    _test_context.set_mobiles(mobile_configs)
    web_driver_handler = ConfigParser.extract_config(ConfigKeys.WEB_CONFIGS)
    _test_context.set_browser_handlers(web_driver_handler)

    yield _test_context

    _test_context.terminate_mobile_apps()
    _test_context.quit_browser_drivers()
