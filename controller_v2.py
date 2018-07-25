import sys
import argparse

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from controller_gui import Ui_MainWindow
import harpoon
from harpoon.boardsupport import borph


class TCUController(harpoon.Project):
    def __init__(self,
                 name='tcu_controller',
                 description='project to communicate with the RHINO-TCU',
                 cores=list(),
                 address='192.168.1.36',
                 headerfile='PulseParameters.ini',
                 bof_exe='tcu_v2-1.bof'):

        harpoon.Project.__init__(self, name, description, cores)
        self.address = address
        self.headerfile = headerfile
        self.bof_exe = bof_exe
        self.fpga_con = borph.RHINO(address=self.address,
                                    username='root',
                                    password='rhino',
                                    login_timeout=30)

    def connect(self):
        print('initializing rhino connection, IP address: ' + self.address)
        print('attempting to connect...')
        try:
            self.fpga_con.connect()
        except Exception as e:
            print('failed to connect to rhino')
            sys.exit(66)
        print('connection successful!')

    def disconnect(self):
        try:
            self.fpga_con.disconnect()
        except Exception as e:
            print('failed to disconnect from rhino')
            sys.exit(66)
        print('disconnect successful!')

    def launch_bof(self):
        # TODO: this assumes that there is no other .bof running on the RHINO
        #       scan for any .bof running on
        if self.fpga_con._pid == '':
            # check for any prexisting running .bof
            print('checking for any prexisting running .bof executables')
            existing_bof_proc = self.fpga_con._action("ps -o pid,args | grep [.]bof | while read c1 c2; do echo $c1; done")
            existing_bof_proc = (existing_bof_proc.decode('utf8').split("\r\n"))[1]

            if existing_bof_proc != '':
                print('existing .bof was found running on the RHINO...')
                print('assuming it is a the same TCU project...')
                self.fpga_con._pid = existing_bof_proc
            else:
                print('no existing running .bof found, launching TCU.bof')
                self.fpga_con.program(self.bof_exe)


# -----------------------------------------------------------------------------
# CORE INSTANTIATION
# -----------------------------------------------------------------------------
core_tcu = harpoon.IPCore('tcu_core', 'Timing control unit')

# -----------------------------------------------------------------------------
# REGISTER INSTANTIATION
# -----------------------------------------------------------------------------
reg_pulses = harpoon.Register('pulses',
                              'Block of pulses in experiment',
                              'uint', 140, 3, core_tcu)
reg_num_repeats = harpoon.Register('num_repeats',
                                   'Number of repeats for each pulse',
                                   'uint', 4, 3, core_tcu)
reg_num_pulses = harpoon.Register('num_pulses',
                                  'Number of pulses',
                                  'uint', 2, 3, core_tcu)
reg_x_amp_delay = harpoon.Register('x_amp_delay',
                                   'Switch-off delay for X band amplifier',
                                   'uint', 2, 3, core_tcu)
reg_l_amp_delay = harpoon.Register('l_amp_delay',
                                   'Switch-off delay for X band amplifier',
                                   'uint', 2, 3, core_tcu)
reg_rex_delay = harpoon.Register('l_amp_delay',
                                 'Delay for REX to output RF after PRI signal',
                                 'uint', 2, 3, core_tcu)
reg_pri_pulse_width = harpoon.Register('pri_pulse_width',
                                       'Pulse width of PRI signal',
                                       'uint', 4, 3, core_tcu)
reg_pre_pulse = harpoon.Register('pre_pulse',
                                 'Pre pulse duration before the main bang',
                                 'uint', 2, 3, core_tcu)
reg_status = harpoon.Register('status',
                              'Current state of the TCU',
                              'uint', 2, 1, core_tcu)
reg_instruction = harpoon.Register('instruction',
                                   'Control register for TCU',
                                   'uint', 2, 3, core_tcu)

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

# -----------------------------------------------------------------------------
# PROJECT INSTANTIATION
# -----------------------------------------------------------------------------
tcu_controller = TCUController(name='tcu_controller',
                               description='project to communicate with the RHINO-TCU',
                               cores=[core_tcu])


class ControllerGUI(Ui_MainWindow):
    """docstring for TCUPulseParamsGUILogic."""

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.txt_pulses.setText("value")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='tcu_controller [address] [file]',
                                     description='Startup script for the '
                                                 'NeXtRAD Timing Control Unit')
    parser.add_argument('address', help='IP address of TCU')
    parser.add_argument('file', help="header file")
    parser.add_argument('-b', '--bof', help='name of .bof file to be executed '
                        'on RHINO [\'tcu_v2.bof\']', default='tcu_v2.bof')
    parser.add_argument('-t', '--timeout', help='login timeout (seconds) to '
                        'establish SSH connection to RHINO [30]',
                        type=int, default=30)
    parser.add_argument('-l', '--logdir', help='directory to store log file '
                        '[\'/tmp\']', default='/tmp')
    parser.add_argument('-g', '--gui', action="store_true", default=False)
    args = parser.parse_args()

    if args.gui is True:
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()

        program = ControllerGUI(window)

        window.show()

        sys.exit(app.exec_())
