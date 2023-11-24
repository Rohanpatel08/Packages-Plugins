import abc
import logging
import json

LOG_LEVEL = logging.DEBUG


class MetaEnvPropReader:
    ENV_PROP = None

    @classmethod
    def init_class(cls, group, env_json):
        if cls.ENV_PROP is None:
            cls.ENV_PROP = cls.get_env_properties(env_json)

        group_properties = cls.ENV_PROP.get(group)
        if group_properties:
            for name, value in group_properties.items():
                setattr(cls, name, value)

    @staticmethod
    def get_env_properties(env_json):
        with open(env_json) as env_file:
            properties = json.load(env_file)
        return properties


class ConfigConstants:
    """ for the mobile section """
    MOBILES = "mobiles"
    PLATFORM_NAME = "platform_name"
    PLATFORM_VERSION = "platform_version"
    DEVICE_NAME = "device_name"
    UDID = "udid"
    ADDRESS = "address"
    PORT = "port"

    """ for the web section """
    WEB = "web"
    BROWSER = "browser"
    PAGE_LOAD_STRATEGY = "page_load_strategy"
    HEADLESS = "headless"

    """ General configurations """
    LOG_LEVEL = "log_level"


class ConfigKeys:
    MOBILE_CONFIGS = "mobile_configs"
    WEB_CONFIGS = "web_configs"


class ConfigParser:
    CONFIG = dict()

    @classmethod
    def parse_args(cls, config_file, env):
        with open(config_file) as config_file:
            config_dict = json.load(config_file)

        cls.CONFIG = config_dict.get(env)

    @classmethod
    def extract_config(cls, key):
        if key == ConfigKeys.MOBILE_CONFIGS:
            mobile_dict = cls.CONFIG.get(ConfigConstants.MOBILES)
            if mobile_dict:
                mobile_configs = []
                from autofw.appium_base.mobile import MobileConfig
                for config in mobile_dict:
                    mobile = MobileConfig(**config)
                    mobile_configs.append(mobile)
                return mobile_configs
        elif key == ConfigKeys.WEB_CONFIGS:
            web_list = cls.CONFIG.get(ConfigConstants.WEB)
            if web_list:
                from autofw.selenium_base.selenium_driver_handler import SeleniumDriverHandler
                web_driver_handlers = dict()
                for web_dict in web_list:
                    a_web_driver_handler = SeleniumDriverHandler(**web_dict)
                    web_driver_handlers[web_dict[ConfigConstants.BROWSER]] = a_web_driver_handler
                return web_driver_handlers
