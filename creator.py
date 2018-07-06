#!/usr/bin/env python

# creator.py

# TODO: initialize default values from tcu_params object
# TODO: change range of frequency spin box depending on mode setting
# TODO: add content to the info section, perhaps have help files with html
# TODO: delete/ignore empty rows of table when export()
# TODO: check rounding of floats when extracting from spinbox
# TODO: verify pulse_params_reg format (is pri 1x32 or 2x16)

import argparse
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from creator_gui import Ui_MainWindow
from parser import TCUParams


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

        # populate fields with existing headerfile data
        self.spin_clk_period.setProperty("value", self.tcu_params.clk_period_ns)
        self.spin_num_pulses.setProperty("value", self.tcu_params.num_pulses)
        self.spin_num_repeats.setProperty("value", self.tcu_params.num_repeats)
        self.spin_pri_pulse_width.setProperty("value", self.tcu_params.pri_pulse_width)
        self.spin_prepulse.setProperty("value", self.tcu_params.pre_pulse)
        self.spin_x_amp_delay.setProperty("value", self.tcu_params.x_amp_delay)
        self.spin_l_amp_delay.setProperty("value", self.tcu_params.l_amp_delay)
        self.spin_dac_delay.setProperty("value", self.tcu_params.dac_delay)
        self.spin_adc_delay.setProperty("value", self.tcu_params.adc_delay)
        self.spin_samples_per_pri.setProperty("value", self.tcu_params.samples_per_pri)
        self.combo_waveform_index.setProperty("currentIndex", self.tcu_params.waveform_index -1)
        self.update_table()
        # disabling the RF pulse width field in the pulses editor selection
        # this will be used for future NeXtRAD experiments capable of waveforms
        # with varying pulse widths. for now, this value is the same as the
        # WAVEFORM_INDEX value
        self.spin_rf_pulse_width.setProperty("enabled", False)
        self.combo_waveform_index.currentTextChanged.connect(self.pulse_width_update)

    def pulse_width_update(self):
        pulse_widths_list = [0.5, 1.0, 3.0, 5.0, 10.0, 15.0, 20.0, 0.5, 1.0, 3.0, 5.0, 10.0, 15.0, 20.0]
        pulse_width = pulse_widths_list[self.combo_waveform_index.currentIndex()]
        self.spin_rf_pulse_width.setProperty("value", pulse_width)
        for pulse in self.tcu_params.pulses:
            pulse['pulse_width'] = pulse_width
        self.update_table()

    def export(self):
        # TODO: verify captured datatypes are ints / doubles
        # TODO: input validation and verification
        # retrieve general params
        self.tcu_params.clk_period_ns = self.spin_clk_period.value()
        self.tcu_params.num_pulses = self.spin_num_pulses.value()
        self.tcu_params.num_pulses = self.spin_num_pulses.value()
        self.tcu_params.num_repeats = self.spin_num_repeats.value()
        self.tcu_params.pri_pulse_width = self.spin_pri_pulse_width.value()
        self.tcu_params.pre_pulse = self.spin_prepulse.value()
        self.tcu_params.x_amp_delay = self.spin_x_amp_delay.value()
        self.tcu_params.l_amp_delay = self.spin_l_amp_delay.value()
        self.tcu_params.dac_delay = self.spin_dac_delay.value()
        self.tcu_params.adc_delay = self.spin_adc_delay.value()
        self.tcu_params.samples_per_pri = self.spin_samples_per_pri.value()
        self.tcu_params.waveform_index = self.combo_waveform_index.currentIndex() + 1
        # retrieve pulse params from table
        # TODO ...
        for row in range(self.table_pulse_params.rowCount()):
            pulse_width = eval(self.table_pulse_params.item(row, 0).text())
            pri = eval(self.table_pulse_params.item(row, 1).text())
            pol_mode = eval(self.table_pulse_params.item(row, 2).text())
            frequency = eval(self.table_pulse_params.item(row, 3).text())
        self.tcu_params.export()
        print("exported")

    # TODO: this needs to be fixed, what gets updated first? table or object?
    def add_pulse(self):
        # pulse = PulseParameters(pulse_width=self.spin_rf_pulse_width.value(),
        #                         pri=self.spin_pri.value(),
        #                         pol_mode=self.combo_mode.currentIndex(),
        #                         frequency=self.spin_frequency.value())
        pulse = {'pulse_width': self.spin_rf_pulse_width.value(),
                 'pri': self.spin_pri.value(),
                 'pol_mode': self.combo_mode.currentIndex(),
                 'frequency': self.spin_frequency.value()}
        self.tcu_params.pulses.append(pulse)
        self.update_table()
        # if num added pulses == num_pulses, disabled add button

    def remove_pulse(self):
        index_list = []
        for model_index in self.table_pulse_params.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)

        for index in index_list:
            print(index.row())
            del self.tcu_params.pulses[index.row()]
            self.table_pulse_params.removeRow(index.row())
        self.update_table()

    def update_table(self):
        self.table_pulse_params.setRowCount(self.spin_num_pulses.value())
        for index, pulse_param in enumerate(self.tcu_params.pulses):
            self.table_pulse_params.setItem(index, 0, QTableWidgetItem(str(pulse_param['pulse_width'])))
            self.table_pulse_params.setItem(index, 1, QTableWidgetItem(str(pulse_param['pri'])))
            self.table_pulse_params.setItem(index, 2, QTableWidgetItem(str(pulse_param['pol_mode'])))
            self.table_pulse_params.setItem(index, 3, QTableWidgetItem(str(pulse_param['frequency'])))

        if len(self.tcu_params.pulses) > 0:
            self.table_pulse_params.selectRow(len(self.tcu_params.pulses) - 1)
            self.button_export.setEnabled(True)
        else:
            self.button_export.setEnabled(False)

        if len(self.tcu_params.pulses) < self.spin_num_pulses.value():
            self.button_add_pulse.setEnabled(True)
        else:
            self.button_add_pulse.setEnabled(False)

        if len(self.tcu_params.pulses) > 0:
            self.button_remove_pulse.setEnabled(True)
        else:
            self.button_remove_pulse.setEnabled(False)

        self.spin_num_pulses.setMinimum(len(self.tcu_params.pulses))


if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # PARSE COMMAND LINE ARGUMENTS
    # -------------------------------------------------------------------------
    clargparser = argparse.ArgumentParser(usage='creator.py [-f FILE]',
                                          description='Experiment creator for the '
                                                      'NeXtRAD Timing Control Unit')
    clargparser.add_argument('-f', '--file',
                             help='header file default [./NeXtRAD.ini]',
                             default='./NeXtRAD.ini')
    clargparser.add_argument('-o', '--outputfile',
                             help='output file for exported params [./PulseParameters.ini]',
                             default='./PulseParameters.ini')
    args = clargparser.parse_args()
    HEADER_FILE = args.file
    OUTPUT_FILE = args.outputfile

    tcu_params = TCUParams(HEADER_FILE, OUTPUT_FILE)

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    program = Creator(tcu_params, window)

    window.show()

    sys.exit(app.exec_())
