import sys
import argparse
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from controller_gui import Ui_MainWindow
import harpoon
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

registers = [reg_pulses, reg_num_repeats, reg_num_pulses,
             reg_x_amp_delay, reg_l_amp_delay,
             reg_pri_pulse_width, reg_pre_pulse,
             reg_status, reg_instruction]

# -----------------------------------------------------------------------------
# PROJECT INSTANTIATION
# -----------------------------------------------------------------------------
project = harpoon.Project('tcu_project',
                          'project to communicate with the RHINO-TCU',
                          [core_tcu])


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
