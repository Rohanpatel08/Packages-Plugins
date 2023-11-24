import subprocess
import time

from autofw.adb_utilities.adb_command_helper import AdbCommandHelper
from autofw.utilities.logger import logger

IFCONFIG = "ifconfig"
INTERFACE_UP = "up"
INTERFACE_DOWN = 'down'
WAIT_TIME_FOR_INTERFACE_UP_DOWN = 10
SYSTEM_USER ='su'


class NetworkInterfaceADB(AdbCommandHelper):
    """
    SoundTouch Interface via ADB
    """

    # todo - implement the StTapSerialSupport methods or inheritance from
    # StTapSerialSup

    def __init__(self, driver):
        """
        starts the ADB server
        """
        super().__init__(driver)
        self.comm_interface = None
        self.logger = logger
        self.driver = driver

    def get_ip_addr(self, interface_name='wlan0', polling_interval=0):
        """
        returns the IP address for a desired network interface
        :param interface_name: string eg:'eth0', 'wlan0, 'lo'
        :param polling_interval: Time to poll in second
        :return: ip_addr(string)
        if there is no error : ip_addr= ip address of the interface
        if there is error: ip_addr = None

        """
        ip_addr = None
        start_time = time.time()
        while ((time.time() - start_time) < polling_interval) or (polling_interval == 0):
            # get the ip addr if adb server started successfully
            if self.adb_server_started:
                status, ip_addr, err = self._is_network_interface_up(interface_name)  # verify interface is up
                if not status:
                    self.logger.info("network interface is down with err {}.".format(err))
                    if polling_interval == 0:
                        break
                elif ip_addr is not None:
                    self.logger.info("{} IP is : {}".format(interface_name, ip_addr))
                    break
            else:
                self.logger.info("ADB server did not start.")

        return ip_addr

    def _is_network_interface_up(self, interface_name='wlan0'):
        try:
            command_to_get_interface_state = 'ip a show {} up'.format(interface_name)
            output = subprocess.Popen(command_to_get_interface_state.split(), stdout=subprocess.PIPE)
            stdout, stderr = output.communicate()
            resp = stdout.decode()
            self.logger.info("From command: {} response: \n{}".format(command_to_get_interface_state, resp))
            if resp is not None:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Unable to get the interface state for interface {}".format(interface_name))
            raise e

    def up_network_interface(self, interface_name='wlan0'):
        """

            this is a method to bring the network interface up with
            command "ifconfig interface_name up"
            :param interface_name: string
            :return:Status(Boolean), resp(String)
            Status = True, resp = ip_address if there is no exception
            Status = False and resp = Reason for failure, If there is any exception
            or error
            """
        command_to_wait_for_devices = '{} {} {} {}'.format(SYSTEM_USER, IFCONFIG, interface_name, INTERFACE_UP)
        status, resp = self.send_adb_command(command_to_wait_for_devices)
        time.sleep(WAIT_TIME_FOR_INTERFACE_UP_DOWN)
        if status:
            return status, resp
        else:
            return False

    def down_network_interface(self, interface_name='eth0'):
        """

        this is a method to bring the network interface up with
        command "ifconfig interface_name down"
        :param interface_name: string
        :return:Status(Boolean), resp(String)
        Status = True, resp = ip_address if there is no exception
        Status = False and resp = Reason for failure, If there is any exception
        or error
        """

        status, resp = self.comm_interface.send_shell_command('{} {}'.format(
            INTERFACE_DOWN, interface_name))
        time.sleep(WAIT_TIME_FOR_INTERFACE_UP_DOWN)
        if status:
            status, ip_address, err_msg = \
                self._is_network_interface_up(interface_name)
            if status:
                status = False
                resp = "Interface is still up: {}".format(resp)
            else:
                resp = "Successfully brought the interface down: {}".format(resp)
                status = True
        return status, resp
