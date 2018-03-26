#!/usr/bin/env python

# creator.py

# TODO: initialize default values from tcu_params object
# TODO: change range of frequency spin box depending on mode setting
# TODO: add content to the info section, perhaps have help files with html
# TODO: delete/ignore empty rows of table when export()
# TODO: check rounding of floats when extracting from spinbox

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from prettytable import PrettyTable

from creator_gui import Ui_MainWindow


class Creator(Ui_MainWindow):
    """docstring for TCUPulseParamsGUILogic."""

    def __init__(self, tcu_params, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.tcu_params = tcu_params
        self.button_export.clicked.connect(self.export)
        self.button_add_pulse.clicked.connect(self.add_pulse)
        self.button_remove_pulse.clicked.connect(self.remove_pulse)
        self.spin_num_pulses.valueChanged.connect(self.update_table)
    #     self.table_pulse_params.itemSelectionChanged.connect(self.select_row)
    #
    # def select_row(self):
    #     items = self.table_pulse_params.selectedItems()

    def export(self):
        # TODO: verify captured datatypes are ints / doubles
        # TODO: input validation and verification
        # retrieve general params
        self.tcu_params.clk_period_ns = self.spin_clk_period.value()
        self.tcu_params.num_pulses = self.spin_num_pulses.value()
        self.tcu_params.num_pulses = self.spin_num_pulses.value()
        self.tcu_params.num_repeats = self.spin_num_repeats.value()
        self.tcu_params.pri_pulse_width = self.spin_pri_pulse_width.value()
        self.tcu_params.prepulse = self.spin_prepulse.value()
        self.tcu_params.x_amp_delay = self.spin_x_amp_delay.value()
        self.tcu_params.l_amp_delay = self.spin_l_amp_delay.value()
        # retrieve pulse params from table
        for row in range(self.table_pulse_params.rowCount()):
            pulse_width = eval(self.table_pulse_params.item(row, 0).text())
            pri = eval(self.table_pulse_params.item(row, 1).text())
            pol_mode = eval(self.table_pulse_params.item(row, 2).text())
            frequency = eval(self.table_pulse_params.item(row, 3).text())
        self.tcu_params.export()

    # TODO: this needs to be fixed, what gets updated first? table or object?
    def add_pulse(self):
        pulse = PulseParameters(pulse_width=self.spin_rf_pulse_width.value(),
                                pri=self.spin_pri.value(),
                                pol_mode=self.combo_mode.currentIndex(),
                                frequency=self.spin_frequency.value())
        self.tcu_params.params.append(pulse)
        self.update_table()
        # if num added pulses == num_pulses, disabled add button

    def remove_pulse(self):
        index_list = []
        for model_index in self.table_pulse_params.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)

        for index in index_list:
            print(index.row())
            del self.tcu_params.params[index.row()]
            self.table_pulse_params.removeRow(index.row())
        self.update_table()

    def update_table(self):
        self.table_pulse_params.setRowCount(self.spin_num_pulses.value())
        for index, pulse_param in enumerate(self.tcu_params.params):
            self.table_pulse_params.setItem(index, 0, QTableWidgetItem(str(pulse_param.pulse_width)))
            self.table_pulse_params.setItem(index, 1, QTableWidgetItem(str(pulse_param.pri)))
            self.table_pulse_params.setItem(index, 2, QTableWidgetItem(str(pulse_param.pol_mode)))
            self.table_pulse_params.setItem(index, 3, QTableWidgetItem(str(pulse_param.frequency)))

        if len(self.tcu_params.params) > 0:
            self.table_pulse_params.selectRow(len(self.tcu_params.params) - 1)
            self.button_export.setEnabled(True)
        else:
            self.button_export.setEnabled(False)

        if len(self.tcu_params.params) < self.spin_num_pulses.value():
            self.button_add_pulse.setEnabled(True)
        else:
            self.button_add_pulse.setEnabled(False)

        if len(self.tcu_params.params) > 0:
            self.button_remove_pulse.setEnabled(True)
        else:
            self.button_remove_pulse.setEnabled(False)

        self.spin_num_pulses.setMinimum(len(self.tcu_params.params))


class TCUParams(object):
    """docstring for TCUPulseParams."""

    def __init__(self, clk_period_ns=10, num_pulses=1, num_repeats=1, pri_duty_cycle=50, prepulse=30, x_amp_delay=3.5, l_amp_delay=1.0):
        self.clk_period_ns = clk_period_ns
        self.num_pulses = num_pulses
        self.num_repeats = num_repeats
        self.pri_pulse_width = pri_duty_cycle
        self.prepulse = prepulse
        self.x_amp_delay = x_amp_delay
        self.l_amp_delay = l_amp_delay
        self.params = list()

    def __str__(self):
        ptable_global = PrettyTable()
        ptable_global.field_names = ['Parameter', 'Value', 'Hex Cycles [big endian]']
        ptable_global.align['Parameter'] = 'l'
        ptable_global.add_row(['num_pulses', self.num_pulses, self._int_to_hex_str(self.num_pulses)])
        ptable_global.add_row(['num_repeats', self.num_repeats, self._int_to_hex_str(self.num_repeats)])
        ptable_global.add_row(
            ['pri_duty_cycle', self.pri_pulse_width, self._int_to_hex_str(int(self.pri_pulse_width * 1000) // self.clk_period_ns)])
        ptable_global.add_row(['prepulse', self.prepulse, self._int_to_hex_str(int(self.prepulse * 1000) // self.clk_period_ns)])
        ptable_global.add_row(
            ['x_amp_delay', self.x_amp_delay, self._int_to_hex_str(int(self.x_amp_delay * 1000) // self.clk_period_ns)])
        ptable_global.add_row(
            ['l_amp_delay', self.l_amp_delay, self._int_to_hex_str(int(self.l_amp_delay * 1000) // self.clk_period_ns)])

        ptable_pulses = PrettyTable()
        ptable_pulses.field_names = ['Pulse Number', 'Pulse Width', 'PRI', 'Mode', 'Frequency']
        for index, pulse in enumerate(self.params):
            ptable_pulses.add_row([index,
                                   pulse.pulse_width,
                                   pulse.pri,
                                   pulse.pol_mode,
                                   pulse.frequency])

        return 'Global Params:\n' + str(ptable_global) + '\nPulse Params\n' + str(ptable_pulses)

    def export(self):
        """exports pulse parameters in NeXtRAD.ini format"""
        # TODO: use config parser for this
        print('NUM_PULSES = {}'.format(self.num_pulses))
        print('NUM_REPEATS = {}'.format(self.num_repeats))
        print('PRI_PULSE_WIDTH = {}'.format(self.pri_pulse_width))
        print('PREPULSE_DELAY = {}'.format(self.prepulse))
        print('X_AMP_DELAY = {}'.format(self.x_amp_delay))
        print('L_AMP_DELAY = {}'.format(self.l_amp_delay))
        print('; PULSES = [<PULSE|PULSE|PULSE...>]')
        print('; PULSE = [<p. width>, <pri>, <mode>, <freq>]')
        print(self.to_pulses_string())
        print()
        self.to_vhdl_snippet()

    def to_pulses_string(self):
        pulses = 'PULSES = \"'
        for index, pulse in enumerate(self.params):
            # pulses += 'PULSE_' + str(index) + ' = \''
            pulses += str(pulse.pulse_width) + ','
            pulses += str(pulse.pri) + ','
            pulses += str(pulse.pol_mode) + ','
            pulses += str(pulse.frequency)
            if index < len(self.params) -1:
                pulses += '|'
        pulses += '\"'
        return pulses

    def to_vhdl_snippet(self):
        print('copy this into HDL:')
        print()
        print('-'*100)
        print('-- system clock period : {}ns ({}MHz)'.format(self.clk_period_ns, (1/(self.clk_period_ns * pow(10, -9))/1000000)))
        print('-'*100)
        print('num_pulses_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(self.num_pulses), self.num_pulses))
        print('num_repeats_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(self.num_repeats), self.num_repeats))
        print('pri_pulse_width_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(int(self.pri_pulse_width * 1000 // self.clk_period_ns)), self.pri_pulse_width))
        print('prepulse_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(int(self.prepulse * 1000 // self.clk_period_ns)), self.prepulse))
        print('x_amp_delay_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(int(self.x_amp_delay * 1000 // self.clk_period_ns)), self.x_amp_delay))
        print('l_amp_delay_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(int(self.l_amp_delay * 1000 // self.clk_period_ns)), self.l_amp_delay))

        print('-'*100)
        print()
        print()
        print('-- <p. width>, <pri>, <mode>, <freq>')
        print()
        for index, pulse in enumerate(self.params):
            print('-- pulse ' + str(index))
            print(self._int_to_hex_str(int(pulse.pulse_width * 1000 // self.clk_period_ns)) + ', ' +
                  self._int_to_hex_str(int(pulse.pri * 1000 // self.clk_period_ns)) + ', ' +
                  self._int_to_hex_str(int(pulse.pol_mode)) + ', ' +
                  self._int_to_hex_str(int(pulse.frequency), endian='l') + ', ')
        print('\nothers => \"ffff\";')
        print('-' * 100)

    def _int_to_hex_str(self, num, endian='b'):
        """ returns a hexidecimal string in format given an integer
            endianess:
                default is LITTLE endian
                for big endian, pass char 'b' as an argument
        """
        hex_num = hex(num)
        hex_num = hex_num.replace('0x', '')
        num_zeros_to_pad = 0
        if len(hex_num) % 4 != 0:
            num_zeros_to_pad = 4 - len(hex_num) % 4
        hex_num = '0' * num_zeros_to_pad + hex_num
        num_bytes = len(hex_num) // 2
        num_words = num_bytes // 2
        byte_list = list()
        index = 0
        for count in range(num_words):
            byte_upper = hex_num[index: index + 2]
            byte_lower = hex_num[index + 2: index + 4]
            if endian == 'b':
                byte_list.append([byte_upper, byte_lower])
            else:
                byte_list.append([byte_lower, byte_upper])
            index += 4
        hex_str = 'x\"'
        for word in byte_list:
            hex_str += word[0] + word[1]
        return hex_str + '\"'


class PulseParameters(object):
    """docstring for PulseParameters."""

    def __init__(self, pulse_width, pri, pol_mode, frequency):
        self.pulse_width = pulse_width
        self.pri = pri
        self.pol_mode = pol_mode
        self.frequency = frequency

    def __str__(self):
        return ("pulse_width : " + str(self.pulse_width) + ", " +
                "pri : " + str(self.pri) + ", " +
                "pol_mode : " + str(self.pol_mode) + ", " +
                "frequency : " + str(self.frequency))


if __name__ == '__main__':
    tcu_params = TCUParams()

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    program = Creator(tcu_params, window)

    window.show()

    sys.exit(app.exec_())
