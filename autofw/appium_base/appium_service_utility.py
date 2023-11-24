import random
import subprocess as sp
import re
from appium.webdriver.appium_service import AppiumService

from autofw.utilities.logger import logger


class AppiumServiceUtility(AppiumService):
    GET_PROCESS_ID_WIN32 = "netstat -aon"
    KILL_PROCESS_WIN32 = "taskkill /F /PID {}"

    def __init__(self, address='127.0.0.1', base_path='/wd/hub'):
        self.address = address
        self.base_path = base_path
        self.ports = []
        super().__init__()

    def start(self, port, **kwargs):
        return super().start(args=['--address', self.address, '-p', str(port), '--base-path', self.base_path], **kwargs)

    def select_port(self):
        netstat_out = sp.check_output(self.GET_PROCESS_ID_WIN32).decode()
        re_string = f"TCP\s+{self.address}:(\d+)\s+.*LISTENING\s+"
        search_results = re.findall(re_string, netstat_out)
        logger.info(f"ports currently listening on the address {self.address}: {search_results}")
        port = 0
        for i in range(2 * len(search_results)):
            rand_port = random.randint(4723, 7999)
            if str(rand_port) not in search_results:
                port = rand_port
                self.ports.append(port)
                break
        return port

    def stop(self):
        try:
            super().stop()
        except:
            self.KILL_PROCESS_WIN32.format(self._process.pid)


if __name__ == "__main__":
    app_ser = AppiumServiceUtility()
    print(app_ser.select_port())
