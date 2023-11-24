from autofw.utilities.logger import logger
import time
import sys
import subprocess
import psutil
import re

ADB_SERVER_NOT_RUNNING = 'server not running'
ADB_STARTED_STRING = 'daemon started successfully'
ADB_SHELL_PROMPT = '#'
ADB_CMD_SHELL = 'shell'
ADB_CMD_HELP = 'help'
ADB_KILL_SERVER_CMD = 'kill-server'
ADB_START_SERVER_CMD = 'start-server'
ADB_DEVICES_CMD = 'devices'
ADB_CMD = 'adb'
ADB_PULL_CMD = "pull"
ADB_PUSH_CMD = "push"
ADB_TOUCH_CMD = "touch"
ADB_CMD_REMOVE_TEMP_FILES = "rm /tmp/tmp.*"
ADB_CMD_ROOT = 'root'
SERVICE_STR = "service"
RUNNING_STR = "running"
ADB_GET_MODEL = 'getprop ro.product.model'
ADB_REBOOT = 'reboot'
ADB_WAIT_FOR_DEVICE = 'wait-for-device'


class AdbCommandHelper:
    def __init__(self, driver):
        """
        Initialize all required objects
        :param phone_info: Phone info object
        :return: None
        """
        self.logger = logger
        self.driver = driver.appium_driver
        self.adb_cmd = ADB_CMD
        self.adb_help = ADB_CMD_HELP
        self.adb_kill_server = ADB_KILL_SERVER_CMD
        self.adb_shell = ADB_CMD_SHELL
        self.start_server = ADB_START_SERVER_CMD
        self.adb_devices = ADB_DEVICES_CMD
        self.adb_shell_prompt = ADB_SHELL_PROMPT
        self._functional = False
        self.__adb_device = self.driver.capabilities['deviceUDID']
        status = self.is_adb_installed()
        if status:
            self.adb_server_started, resp = self.start_adb_server()

    def is_adb_installed(self):
        """
        This function confirms if adb is installed on the test station.
        It also sets self._functional = True if adb is installed and False
        otherwise.
        :return: self._functional(boolean) True if ADB is installed and False
        if it is not installed on the station

        """
        status, resp = self.send_adb_command(self.adb_help)
        if status:
            self._functional = True

            self.logger.info('ADB is installed on system: {}'.format(resp))
        else:
            self._functional = False
            self.logger.info('ADB is not installed on system: {}'.format(resp))
        return self._functional

    def send_shell_command(self, shell_command=None, cd_command=[]):
        """
        Used to send commands to the Android device that's connected via ADB.
        ****
        If shell_command and cd_command are passed, shell_command will be ignored.
        ****
        :param:
            shell_command - a string of the command to be sent
            cd_command - a list of commands that will be executed one after another
        :return:
            Boolean, String
                Boolean is True if command was sent successfully
                    String will then be the response to that command (may be empty string)
                Boolean is False if any errors occur
                    String will then be an error message description
        """
        # Set root permission to adb device in case of VT ADB or Coronado platform
        status = True
        if not self._functional:
            response = 'ADB is not installed  Cannot send shell_command {}'.format(shell_command)
            status = False
        else:
            if cd_command == [] and shell_command is not None:
                cd_command = [shell_command]
            try:
                for shell_cmd in cd_command:

                    if self.__adb_device:
                        command = '{} -s {} {} {}'.format(self.adb_cmd, self.__adb_device,
                                                          self.adb_shell, shell_cmd)
                    else:
                        command = '{} {} {}'.format(self.adb_cmd, self.adb_shell,
                                                    shell_cmd)

                    proc = subprocess.Popen(command.split(),
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                    stdout, stderr = proc.communicate()
                    response = stdout.decode()
                    self.logger.info("From command: {} response: {}".format(command, response))
            except Exception as ex:
                status = False
                response = ex

        return status, response

    def send_adb_command(self, command):
        """
        method which sends the adb command on the terminal and returns the
        response
        :param command: adb command
        :return: status(boolean), response(String)
        Status = false if there is an exception, else status = True
        resp = The response from the command line for the adb command issued.
        """

        if command == self.adb_shell:
            status = False
            resp = 'adb command "{}" cannot to executed as it would take the control ' \
                   'to ADB Shell and the control does not come back to the ' \
                   'terminal.'.format(command)
        else:
            if self.__adb_device:
                cmd = '{} -s {} {}'.format(self.adb_cmd, self.__adb_device, command)
            else:
                cmd = '{} {}'.format(self.adb_cmd, command)
                if self.start_server in command and 'linux' in sys.platform:
                    cmd = '{} {}'.format('sudo', cmd)

            status = True
            try:
                proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                resp = stdout.decode()
                self.logger.info("From command: {} response: \n{}".format(cmd, resp))
            except Exception as ex:
                status = False
                resp = ex
        return status, resp

    def set_root_permission(self, adb_device_id=None):
        """
        Method to set root permission to adb device.
        :param adb_device_id: Adb device id.
        :return: status: True on success, else False.
                 rtn_msg: Command response on success and error message on failure.
        """
        status = False

        if not adb_device_id:
            adb_device_id = self.__adb_device

        self.logger.info("Execute adb root command for adb device : {}".format(adb_device_id))
        cmd = '{} -s {} {}'.format(self.adb_cmd, adb_device_id, ADB_CMD_ROOT)
        try:
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            self.logger.info("From command: {} response: \n{}".format(cmd, stdout.decode()))
            time.sleep(2)
            status = True
            rtn_msg = stdout.decode()
        except Exception as ex:
            rtn_msg = "Received exception while root to adb device. Exception : {}".format(ex)

        return status, rtn_msg

    def get_android_phone_model(self):
        """
            Get the android phone model
            :return: Android phone model
            """
        try:
            command_to_get_model_number = '{} {}'.format(ADB_CMD_SHELL, ADB_GET_MODEL)
            status, resp = self.send_adb_command(command_to_get_model_number)
            if status:
                self._functional = True
                self.logger.info('Device Model Info: {}'.format(resp))
                return resp
            else:
                self._functional = False
                self.logger.info('Unable to get Model info: {}'.format(resp))
            return self._functional
        except Exception as error:
            # log error and return blank mode number
            raise error

    def get_status_of_app(self, app_package):
        try:
            command_to_get_status = 'pidof {}'.format(app_package)
            status, resp = self.send_shell_command(command_to_get_status)
            if status:
                self._functional = True
                if resp is '':
                    self.logger.info('App {} is inactive'.format(app_package))
                    return True
                else:
                    self.logger.info('App {} is active'.format(app_package))
                    return False
            else:
                self._functional = False
                self.logger.info('Unable to get app status info: {}'.format(resp))
            return self._functional
        except:
            logger.error("Something went wrong while getting the app status of:".format(app_package))

    def uninstall_app(self, app_package):
        try:
            command_to_get_status = 'uninstall {}'.format(app_package)
            status, resp = self.send_adb_command(command_to_get_status)
            if status:
                self._functional = True
                self.logger.info('Uninstalled App: {}'.format(app_package))
            else:
                self._functional = False
                self.logger.info('Unable to uninstall app: {}'.format(resp))
            return self._functional
        except:
            logger.error("Something went wrong while uninstalling the app :".format(app_package))

    def install_app(self, app_path):
        try:
            command_to_get_status = 'install {}'.format(app_path)
            status, resp = self.send_adb_command(command_to_get_status)
            if status:
                self._functional = True
                self.logger.info('installed App: {}'.format(app_path))
            else:
                self._functional = False
                self.logger.info('Unable to install app: {}'.format(resp))
            return self._functional
        except:
            logger.error("Something went wrong while uninstalling the app :".format(app_path))

    def get_app_package_app_activity(self):
        try:
            command_to_get_activity_package = 'dumpsys window windows | grep -E mObscuringWindow'
            status, resp = self.send_shell_command(command_to_get_activity_package)
            if status:
                self._functional = True
                self.logger.info('App package and App activity:{}'.format(resp))
            else:
                self._functional = False
                self.logger.info('App package and App activity'.format(resp))
            return resp
        except:
            logger.error("Something went wrong")

    def reboot_android_device(self):
        try:
            command_to_get_status = '{}'.format(ADB_REBOOT)
            command_to_wait_for_devices = '{}'.format(ADB_WAIT_FOR_DEVICE)
            status, resp = self.send_adb_command(command_to_get_status)
            if status:
                self._functional = True
                self.logger.info('Device reboot command successful')
                try:
                    logger.info("Waiting for the device")
                    self.send_adb_command(command_to_wait_for_devices)
                    logger.info("Device restarted")
                except:
                    logger.error("Device unable to restart")
            else:
                self._functional = False
                self.logger.info('Device reboot command unsuccessful')

            return self._functional
        except:
            logger.error("Something went wrong while rebooting the device")

    def kill_adb_server(self):
        """
                This sends a command to kill any ADB instance that may be running on the workstation
                :param:None
                :return:
                    Boolean, String
                        Boolean is True if command was sent successfully
                            String will be a happy message
                        Boolean is False if any errors occur
                            String will then be an error message description
                """
        # Kill any previous server to ensure one device at a time
        if self._functional:
            status, resp = self.send_adb_command(self.adb_kill_server)
            if status:
                if resp and ADB_SERVER_NOT_RUNNING in resp:
                    self.logger.info('ADB server already killed with response = {}'.format(resp))
                elif resp:
                    self.logger.info('Error: ADB server could not be killed with err = {}'.format(resp))
                    status = False
                else:
                    self.logger.info('ADB server successfully killed')
        else:
            status = False
            resp = 'ADB not installed'
        return status, resp

    def start_adb_server(self):
        cmd = self.start_server
        status, resp = self.send_adb_command('{}'.format(cmd))
        self.logger.info("Start Adb server with response  {}, ".format(resp))
        if status:
            if resp and ADB_STARTED_STRING not in resp:
                resp = 'Error: There is problem starting the adb server with' \
                       ' err_msg : {}'.format(resp)
                status = False
            else:
                status = True
                resp = "Successfully started adb server"
        return status, resp

    def get_device_state(self):
        try:
            command_to_get_app_state = 'get-state'
            status, resp = self.send_adb_command(command_to_get_app_state)
            if status:
                self._functional = True
                self.logger.info('Device state:{}'.format(resp))
            else:
                self._functional = False
                self.logger.info('Unable to get device state'.format(resp))
            return self._functional
        except:
            logger.error("Something went wrong")

    def get_android_logs(self):
        try:
            if sys.platform == 'win32':
                command_to_get_logs = 'logcat -d > {}'.format('android_logs.txt')
                status, resp = self.send_adb_command(command_to_get_logs)
                if status:
                    self._functional = True
                    logger.info("Logs stored in file {}".format("android_logs.txt"))
                else:
                    self._functional = False
                    self.logger.info('Unable to get device state'.format(resp))
                return self._functional

        except Exception as e:
            logger.error("Unable to store the logs")
            raise e

    def push_file_from_pc_to_device(self, source, destination):
        try:
            if sys.platform == 'win32':
                command_to_get_activity_package = 'cmd', '/c', 'adb -s emulator-5554 push {} {}'.format(source, destination)
                subprocess.check_output(command_to_get_activity_package, shell=True)
                logger.info("file pushed from {} to {}".format(source, destination))
        except Exception as e:
            logger.error("Unable push the file")
            raise e

    def pull_file_from_device_to_pc(self, source, destination):
        try:
            if sys.platform == 'win32':
                command_to_get_activity_package = 'cmd', '/c', 'adb -s emulator-5554 pull {} {}'.format(source, destination)
                subprocess.check_output(command_to_get_activity_package, shell=True)
                logger.info("file pulled from {} to {}".format(source, destination))
        except Exception as e:
            logger.error("Unable pull the file")
            raise e

    def ensure_no_orphan_adb(self):
        """
               sometimes things go wrong and orphan adb process is left running and holding resources, this is one final
               cleanup to kill those orphans are dead!

               :return: no return
               """
        # todo return the status

        for process in psutil.process_iter():
            try:
                process_cmd_list = process.cmdline()
                if 'adb' in process_cmd_list and 'fork-server' in process_cmd_list:  # in the rare chance more orphans are left hanging around, we keep going
                    logger.info(
                        "\n!!Found a stray adb process. Will now terminate process {} ".format(process.cmdline()))
                    process.terminate()  # todo handle failure here
            except Exception:
                # on windows we may not have permission to check this process details - that's ok, keep going adb
                continue

    def get_volume_using_adb_command(self, stream):
        """
        Get the current volume of a stream from the Android device settings using adb command.
        stream : int
        stream = 1 for STREAM_SYSTEM
        stream = 2 for STREAM_RING
        stream = 3 for STREAM_MUSIC
        stream = 4 for STREAM_ALARM
        stream = 5 for STREAM_NOTIFICATION
        stream = 6 for STREAM_BLUETOOTH_SCO
        stream = 7 for STREAM_SYSTEM_ENFORCED
        stream = 8 for STREAM_DTM
        :return: Volume of the specified stream
        """
        command_to_get_volume = 'adb shell cmd media_session volume --stream {} --get'.format(stream)
        output = subprocess.Popen(command_to_get_volume.split(), stdout=subprocess.PIPE)
        output, _ = output.communicate()
        current_volume = int(re.findall("volume is \\d+", output.decode())[0].replace("volume is ", ""))
        logger.debug("Current volume is %s on android device %s", str(current_volume),
                     self.driver.capabilities['deviceUDID'])
        return current_volume

    def set_volume_using_adb_command(self, stream, volume):
        """
            Get the current volume of a stream from the Android device settings using adb command.
            stream : int
            volume : int
            stream = 1 for STREAM_SYSTEM
            stream = 2 for STREAM_RING
            stream = 3 for STREAM_MUSIC
            stream = 4 for STREAM_ALARM
            stream = 5 for STREAM_NOTIFICATION
            stream = 6 for STREAM_BLUETOOTH_SCO
            stream = 7 for STREAM_SYSTEM_ENFORCED
            stream = 8 for STREAM_DTM
            :return: Volume of the specified stream
            """
        try:
            command_to_set_volume = 'adb shell cmd media_session volume --stream {} --set {}'.format(stream, volume)
            output = subprocess.Popen(command_to_set_volume.split(), stdout=subprocess.PIPE)
            output, _ = output.communicate()
            logger.debug("Set volume to %s on android device %s", str(volume),
                         self.driver.capabilities['deviceUDID'])
            return volume
        except Exception as e:
            logger.error("Unable to set the volume to {}".format(volume))
            raise e
