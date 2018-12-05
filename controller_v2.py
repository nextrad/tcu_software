import sys
import argparse
import time
import logging
import npyscreen

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from controller_gui import Ui_MainWindow
import harpoon
from harpoon.boardsupport import borph
from parser import TCUParams


class TCUController(harpoon.Project):
    def __init__(self,
                 fpga_con,
                 name='tcu_controller',
                 description='project to communicate with the RHINO-TCU',
                 cores=list(),
                 address='192.168.1.36',
                 headerfile='PulseParameters.ini',
                 bof_exe='tcu_v2-1-3.bof',
                 debug=False,
                 log_dir=''
                 ):

        harpoon.Project.__init__(self, name, description, cores)
        self.address = address
        self.headerfile = headerfile
        self.bof_exe = bof_exe
        self.fpga_con = fpga_con
        self._init_logger(log_dir, debug)

    def _init_logger(self, log_dir='', debug=False):
        self.logger = logging.getLogger('tcu_project_logger')
        self.logger.setLevel(logging.DEBUG)
        self.log_dir = log_dir
        # create file handler which logs even debug messages
        time_struct = time.localtime()
        time_str = time.strftime("%H:%M:%S", time_struct)
        date_str = time.strftime("%d-%m-%Y", time_struct)
        fh = logging.FileHandler(self.log_dir+'tcu_'+self.fpga_con.address+'.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        if debug is True:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter2 = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter2)
        fh.setFormatter(formatter)
        # add the handlers to logger
        logging.getLogger().addHandler(fh)
        logging.getLogger().addHandler(ch)

    def connect(self):
        self.logger.info('initializing rhino connection, IP address: ' + self.address)
        try:
            self.fpga_con.connect()
            # time.sleep(3)
            self.power_fmc()
        except Exception as e:
            self.logger.exception('failed to connect to tcu')
            sys.exit(66)
        self.logger.info('connection successful!')

    def disconnect(self):
        self.logger.info('disconnecting from tcu...')
        try:
            self.fpga_con.disconnect()
        except Exception as e:
            self.logger.exception('failed to disconnect from tcu')
            sys.exit(66)
        self.logger.info('disconnect successful!')

    def power_fmc(self):
        self.logger.debug('calling power_fmc.sh script...')
        fpga_con._action('./power_fmc.sh')
        # time.sleep(3)
        # self.fpga_con._action('echo 102 > /sys/class/gpio/export')
        # self.fpga_con._action('echo out > /sys/class/gpio/gpio102/direction')
        # self.fpga_con._action('echo 1 > /sys/class/gpio/gpio102/value')
        # self.fpga_con._action('echo out > /sys/class/gpio/gpio100/direction')
        # self.fpga_con._action('echo 1 > /sys/class/gpio/gpio100/value')

    def start(self):
        self.logger.info('starting.bof...')
        self.fpga_con.launch_bof(self.bof_exe, link=True)

    def stop(self):
        self.logger.info('stopping .bof...')
        self.fpga_con.kill_bof()

    def parse_header(self):
        self.logger.info('parsing header file...')
        self.tcu_params = TCUParams(self.headerfile)
        self.logger.debug('Extracted parameters from header:\n' + str(self.tcu_params))

    def write_registers(self):
        self.logger.info('writing registers...')
        params = self.tcu_params.get_int_params()
        reg_num_repeats.write(params['num_repeats'])
        reg_num_pulses.write(params['num_pulses'])
        reg_x_amp_delay.write(params['x_amp_delay'])
        reg_l_amp_delay.write(params['l_amp_delay'])
        reg_rex_delay.write(params['rex_delay'])
        reg_pri_pulse_width.write(params['pri_pulse_width'])
        reg_pre_pulse.write(params['pre_pulse'])

        # need to do a bit more work for reg_pulses,
        # as it is a more complex data structure
        hex_params = self.tcu_params.get_hex_params()
        pulses = hex_params['pulses']
        pulse_param_str = str()
        for pulse in pulses:
            pulse_param_str += pulse['pulse_width'].replace('\\x', '') + pulse['pri'].replace('\\x', '') + pulse['pol_mode'].replace('\\x', '') + pulse['frequency'].replace('\\x', '')
        pulse_param_bytearray = bytearray.fromhex(pulse_param_str)
        reg_pulses.write_bytes(pulse_param_bytearray, raw=True)

    def verify_registers(self):
        self.logger.info('verifying registers...')
        params = self.tcu_params.get_int_params()
        register_value_correct = True
        if self._verify_register(reg_num_repeats, params['num_repeats']) == False:
            register_value_correct = False
        if self._verify_register(reg_num_pulses, params['num_pulses']) == False:
            register_value_correct = False
        if self._verify_register(reg_x_amp_delay, params['x_amp_delay']) == False:
            register_value_correct = False
        if self._verify_register(reg_l_amp_delay, params['l_amp_delay']) == False:
            register_value_correct = False
        if self._verify_register(reg_rex_delay, params['rex_delay']) == False:
            register_value_correct = False
        if self._verify_register(reg_pri_pulse_width, params['pri_pulse_width']) == False:
            register_value_correct = False
        if self._verify_register(reg_pre_pulse, params['pre_pulse']) == False:
            register_value_correct = False

        # need to do a bit more work for reg_pulses,
        # as it is a more complex data structure
        hex_params = self.tcu_params.get_hex_params(hdl_format=True)
        pulses = hex_params['pulses']
        pulse_param_str = str()
        for pulse in pulses:
            pulse_param_str += pulse['pulse_width'].replace('\"', '') + pulse['pri'].replace('\"', '') + pulse['pol_mode'].replace('\"', '') + pulse['frequency'].replace('\"', '')
        pulse_param_str = pulse_param_str.replace('x', '')

        num_pulses = reg_num_pulses.read()
        read_value = reg_pulses.read_bytes()[0:(10*num_pulses)]
        read_value_str= str()
        self.logger.warning('Due to python version mismatches, verifying pulses register has been disabled')
        # for pulse_index in range(num_pulses):
        #     # print('pulse[{}]'.format(pulse_index))
        #     pulse_width = read_value[pulse_index*10 + 0:pulse_index*10+ 2]
        #     # print('pw {}'.format(pulse_width.hex()))
        #     pri = read_value[pulse_index*10 + 4:pulse_index*10+ 6] + read_value[pulse_index*10 + 2:pulse_index*10+ 4]
        #     # print('pri {}'.format(pri.hex()))
        #     mode = read_value[pulse_index*10 + 6:pulse_index*10+ 8]
        #     # print('mode {}'.format(mode.hex()))
        #     freq = read_value[pulse_index*10 + 8:pulse_index*10+ 10]
        #     # print('freq {}'.format(freq.hex()))
        #     read_value_str += pulse_width.hex() + pri.hex() + mode.hex() + freq.hex()
        # if read_value_str == pulse_param_str:
        #     self.logger.debug('Register \'{}\' verified'.format('pulses'))
        # else:
        #     self.logger.error('Value mismatch for register \'{}\' retrieved {}, expected {}'.format('pulses', read_value_str, pulse_param_str))
        #     register_value_correct = False

        if register_value_correct:
            self.logger.info('All registers have been verified')
        else:
            self.logger.error('One or more registers contain incorrect value(s) - see {} for details'.format(self.log_dir+'tcu_'+self.fpga_con.address+'.log'))

    def _verify_register(self, register, expected_value):
        read_value = register.read()
        if read_value == expected_value:
            self.logger.debug('Register \'{}\' verified'.format(register.name))
            return True
        else:
            self.logger.error('Value mismatch for register \'{}\' retrieved {}, expected {}'.format(register.name, read_value, expected_value))
            return False

    def arm(self):
        self.logger.info('arming tcu...')
        reg_instruction.write(0)
        # time.sleep(3)
        reg_instruction.write(1)

fpga_con = borph.RHINO()
# -----------------------------------------------------------------------------
# CORE INSTANTIATION
# -----------------------------------------------------------------------------
core_tcu = harpoon.IPCore('tcu_core', 'Timing control unit', fpga_con)

# -----------------------------------------------------------------------------
# REGISTER INSTANTIATION
# -----------------------------------------------------------------------------
reg_pulses = harpoon.Register('pulses',
                              'Block of pulses in experiment',
                              int, 140, 3, core_tcu)
reg_num_repeats = harpoon.Register('num_repeats',
                                   'Number of repeats for each pulse',
                                   int, 4, 3, core_tcu)
reg_num_pulses = harpoon.Register('num_pulses',
                                  'Number of pulses',
                                  int, 2, 3, core_tcu)
reg_x_amp_delay = harpoon.Register('x_amp_delay',
                                   'Switch-off delay for X band amplifier',
                                   int, 2, 3, core_tcu)
reg_l_amp_delay = harpoon.Register('l_amp_delay',
                                   'Switch-off delay for X band amplifier',
                                   int, 2, 3, core_tcu)
reg_rex_delay = harpoon.Register('rex_delay',
                                 'Delay for REX to output RF after PRI signal',
                                 int, 2, 3, core_tcu)
reg_pri_pulse_width = harpoon.Register('pri_pulse_width',
                                       'Pulse width of PRI signal',
                                       int, 4, 3, core_tcu)
reg_pre_pulse = harpoon.Register('pre_pulse',
                                 'Pre pulse duration before the main bang',
                                 int, 2, 3, core_tcu)
reg_status = harpoon.Register('status',
                              'Current state of the TCU',
                              int, 2, 1, core_tcu)
reg_instruction = harpoon.Register('instruction',
                                   'Control register for TCU',
                                   int, 2, 3, core_tcu)

# add list of registers to the core
# TODO: fix this reverse dependency between core and registers
registers = [
            reg_pulses,
            reg_num_repeats,
            reg_num_pulses,
            reg_x_amp_delay,
            reg_l_amp_delay,
            reg_rex_delay,
            reg_pri_pulse_width,
            reg_pre_pulse,
            reg_status,
            reg_instruction
            ]
core_tcu.registers = registers


class ControllerGUI(Ui_MainWindow):
    """docstring for TCUPulseParamsGUILogic."""

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.txt_pulses.setText("value")

class TCUMonitorForm(npyscreen.Form):

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.count = 0
        self.keypress_timeout = 10  # refresh period in 100ms (10 = 1s)
        self.text_address = self.add(npyscreen.TitleText, name='IP Address', editable=False, value='xxx.xxx.xxx.xxx')
        self.text_connection = self.add(npyscreen.TitleText, name='Connection', editable=False, value='?')
        self.text_state = self.add(npyscreen.TitleText, name='State', editable=False, value='?')
        self.text_num_pulses = self.add(npyscreen.TitleText, name='Pulses', editable=False, value='?')
        self.text_num_repeats = self.add(npyscreen.TitleText, name='Repeats', editable=False, value='?')
        self.text_pre_pulse = self.add(npyscreen.TitleText, name='Pre Pulse', editable=False, value='?')
        self.text_x_amp_delay = self.add(npyscreen.TitleText, name='X Amp Delay', editable=False, value='?')
        self.text_l_amp_delay = self.add(npyscreen.TitleText, name='L Amp Delay', editable=False, value='?')
        self.text_rex_delay = self.add(npyscreen.TitleText, name='Rex Delay', editable=False, value='?')
        self.grid_pulses = self.add(npyscreen.GridColTitles, name='Pulses', editable=False, column_width=10, height=7, max_height=10)
        self.grid_pulses.col_titles =[ 'Pulse', 'Pulse Width', 'PRI', 'Mode', 'Frequency']
        self.grid_pulses.values = [
                                    ['0', '10.0', '1000', '0', '1300'],
                                    ['1', '10.0', '1000', '1', '1300'],
                                    ['2', '10.0', '1000', '2', '1300'],
                                    ['3', '10.0', '1000', '3', '1300'],
                                    ['4', '10.0', '1000', '4', '8500'],
                                    ['5', '10.0', '1000', '5', '8500'],
                                  ]
        # self.button_arm = self.add(npyscreen.ButtonPress, name='Arm')
        # self.button_arm.whenPressed = self.when_pressed_arm

    def when_pressed_arm(self):
        self.button_arm.name = 'disarm'

    def while_waiting(self):
        # called every keypress_timeout period when user not interacting
        self.text_address.value = str(tcu.address)
        self.text_state.value = str(reg_status.read())
        self.text_num_pulses.value = str(reg_num_pulses.read())
        self.text_num_repeats.value = str(reg_num_repeats.read())
        self.text_pre_pulse.value = str(reg_pre_pulse.read())
        self.text_x_amp_delay.value = str(reg_x_amp_delay.read())
        self.text_l_amp_delay.value = str(reg_l_amp_delay.read())
        self.text_rex_delay.value = str(reg_rex_delay.read())
        self.display()


class TCUMonitorApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TCUMonitorForm, name='TCU MONITOR')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='tcu_controller [address]',
                                     description='Controller script for '
                                                 'NeXtRAD\'s Timing Control Unit')
    parser.add_argument('address', help='IP address of TCU')
    parser.add_argument('-f', '--file', help="header file")
    parser.add_argument('-b', '--bof', help='name of .bof file to be executed '
                        'on RHINO [\'tcu_v2.bof\']', default='tcu_v2.bof')
    parser.add_argument('-t', '--timeout', help='login timeout (seconds) to '
                        'establish SSH connection to RHINO [30]',
                        type=int, default=30)
    parser.add_argument('-d', '--debug', help='display debug messages to STDOUT',
                        action='store_true', default=False)
    parser.add_argument('-c', '--check_regs', help='verify registers after writing',
                        action='store_true', default=False)
    parser.add_argument('-l', '--logdir', help='directory to store log file '
                        '[\'/tmp/\']', default='/tmp/')
    parser.add_argument('-g', '--gui', action="store_true", default=False)
    parser.add_argument('-m', '--monitor', action="store_true", default=False)
    parser.add_argument('-k', '--kill', help='kill running .bof',
                        action="store_true", default=False)
    parser.add_argument('-i', '--init', help='automatically connect and initialize TCU',
                        action="store_true", default=False)
    args = parser.parse_args()

    fpga_con.address = args.address
    fpga_con.login_timeout = args.timeout

    tcu = TCUController(name='tcu_controller',
                        description='project to communicate with the RHINO-TCU',
                        cores=[core_tcu],
                        fpga_con=fpga_con,
                        bof_exe=args.bof,
                        headerfile=args.file,
                        debug=args.debug,
                        log_dir=args.logdir)

    if args.init is True:
        tcu.parse_header()
        tcu.connect()
        tcu.start()
        tcu.write_registers()
        if args.check_regs is True:
            tcu.verify_registers()
        tcu.arm()
        tcu.disconnect()

    if args.monitor is True:
        tcu.connect()
        tcu.start()
        app = TCUMonitorApplication()
        app.run()

    if args.gui is True:
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()

        program = ControllerGUI(window)

        window.show()

        sys.exit(app.exec_())
