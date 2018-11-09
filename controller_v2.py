import sys
import argparse
import time
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from controller_gui import Ui_MainWindow
import harpoon
from harpoon.boardsupport import borph


class TCUController(harpoon.Project):
    def __init__(self,
                 fpga_con,
                 name='tcu_controller',
                 description='project to communicate with the RHINO-TCU',
                 cores=list(),
                 address='192.168.1.36',
                 headerfile='PulseParameters.ini',
                 bof_exe='tcu_v2-1_internal_clk.bof',
                 ):

        harpoon.Project.__init__(self, name, description, cores)
        self.address = address
        self.headerfile = headerfile
        self.bof_exe = bof_exe
        self.fpga_con = fpga_con
        self._init_logger()

    def _init_logger(self):
        self.logger = logging.getLogger('tcu_project_logger')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        time_struct = time.localtime()
        time_str = time.strftime("%H:%M:%S", time_struct)
        date_str = time.strftime("%d-%m-%Y", time_struct)
        fh = logging.FileHandler('tcu_' + self.fpga_con.address + '.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
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
        except Exception as e:
            self.logger.error('failed to connect to tcu')
            sys.exit(66)
        self.logger.info('connection successful!')

    def disconnect(self):
        self.logger.info('disconnecting from tcu...')
        try:
            self.fpga_con.disconnect()
        except Exception as e:
            self.logger.error('failed to disconnect from tcu')
            sys.exit(66)
        self.logger.info('disconnect successful!')

    def start(self):
        self.logger.info('starting.bof...')
        self.fpga_con.launch_bof(self.bof_exe, link=True)

    def stop(self):
        self.logger.info('stopping .bof...')
        self.fpga_con.kill_bof()

    def parse_header(self):
        self.logger.info('parsing header file...')

    def write_registers(self):
        self.logger.info('writing registers...')

    def verify_registers(self):
        self.logger.info('verifying registers...')

    def arm(self):
        self.logger.info('arming tcu...')
        reg_instruction.write(0)
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
    parser.add_argument('-l', '--logdir', help='directory to store log file '
                        '[\'/tmp\']', default='/tmp')
    parser.add_argument('-g', '--gui', action="store_true", default=False)
    args = parser.parse_args()
    print(args.address)
    fpga_con.address = args.address
    fpga_con.login_timeout= args.timeout
    tcu = TCUController(name='tcu_controller',
                        description='project to communicate with the RHINO-TCU',
                        cores=[core_tcu],
                        fpga_con=fpga_con,
                        bof_exe=args.bof)

    if args.gui is True:
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()

        program = ControllerGUI(window)

        window.show()

        sys.exit(app.exec_())
