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
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox
import datetime

from creator_gui import Ui_MainWindow
from parser import TCUParams

VERSION = '1.2.0'
class Creator(Ui_MainWindow):
    """docstring for TCUPulseParamsGUILogic."""

    def __init__(self, tcu_params, window):
        self.main_window = Ui_MainWindow.__init__(self)
        self.setupUi(window)
        window.setWindowTitle('TCU Parameter Editor v' + VERSION)
        self.tcu_params = tcu_params
        self.actionQuit.triggered.connect(sys.exit)
        self.actionOpen.triggered.connect(self.open)
        self.actionExport.triggered.connect(self.export_to)
        self.actionInstructions.triggered.connect(self.display_help)
        self.actionAbout.triggered.connect(self.display_about)
        self.button_export.clicked.connect(self.export)
        self.button_export_close.clicked.connect(self.export_close)
        self.button_add_pulse.clicked.connect(self.add_pulse)
        self.button_add_pulse.clicked.connect(self.update_metadata)
        self.button_edit_pulse.clicked.connect(self.edit_pulse)
        self.button_edit_pulse.clicked.connect(self.update_metadata)
        self.button_remove_pulse.clicked.connect(self.remove_pulse)
        self.button_more_params.clicked.connect(self.toggle_params)
        self.display_more_pulses = True
        self.toggle_params()

        # self.spin_num_pulses.valueChanged.connect(self.update_table)
        # self.spin_num_pulses.valueChanged.connect(self.update_metadata)
        self.spin_num_repeats.valueChanged.connect(self.update_metadata)
        self.spin_samples_per_pri.valueChanged.connect(self.update_metadata)
        self.combo_mode.activated[str].connect(self.update_frequency_band)
        self.table_pulse_params.itemSelectionChanged.connect(self.update_selection)
        #
        # def select_row(self):
        #     items = self.table_pulse_params.selectedItems()

        # populate fields with existing headerfile data
        self.spin_clk_period.setProperty("value", self.tcu_params.clk_period_ns)
        # self.spin_num_pulses.setProperty("value", self.tcu_params.num_pulses)
        self.spin_num_repeats.setProperty("value", self.tcu_params.num_repeats)
        self.spin_pri_pulse_width.setProperty("value", self.tcu_params.pri_pulse_width)
        self.spin_prepulse.setProperty("value", self.tcu_params.pre_pulse)
        self.spin_x_amp_delay.setProperty("value", self.tcu_params.x_amp_delay)
        self.spin_l_amp_delay.setProperty("value", self.tcu_params.l_amp_delay)
        self.spin_rex_delay.setProperty("value", self.tcu_params.rex_delay)
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
        self.spin_rf_pulse_width.setToolTip('Multiple pulse-widths not yet supported, please use \'Waveform Index\' parameter')
        self.combo_waveform_index.currentTextChanged.connect(self.pulse_width_update)

    def pulse_width_update(self):
        pulse_widths_list = [0.5, 1.0, 3.0, 5.0, 10.0, 15.0, 20.0, 0.5, 1.0, 3.0, 5.0, 10.0, 15.0, 20.0]
        pulse_width = pulse_widths_list[self.combo_waveform_index.currentIndex()]
        self.spin_rf_pulse_width.setProperty("value", pulse_width)
        for pulse in self.tcu_params.pulses:
            pulse['pulse_width'] = pulse_width
        self.update_table()

    def _get_filename_from_dialog(self):
        filename = QFileDialog.getOpenFileName(parent=self.main_window, caption='Open file', directory='./', filter='INI Files (*.ini);;All Files (*)')
        return (filename[0])

    def open(self):
        filename = self._get_filename_from_dialog()

    def export_to(self):
        filename = self._get_filename_from_dialog()

    def display_help(self):
        self.instructions_window = QtWidgets.QMainWindow()
        widget = QtWidgets.QWidget(self.instructions_window)
        gridlayout = QtWidgets.QGridLayout()
        widget.setLayout(gridlayout)
        widget.setWindowTitle('Instructions')
        gridlayout.addWidget(QtWidgets.QLabel(widget, text='https://github.com/nextrad/tcu_software'))
        self.instructions_window.show()


    def display_about(self):
        QMessageBox.about(self.main_window, 'About', 'TCU Parameter Editor\nv1.1.0\nBrad Kahn')

    def export(self):
        # TODO: verify captured datatypes are ints / doubles
        # TODO: input validation and verification
        # retrieve general params
        self.tcu_params.clk_period_ns = self.spin_clk_period.value()
        # self.tcu_params.num_pulses = self.spin_num_pulses.value()
        self.tcu_params.num_repeats = self.spin_num_repeats.value()
        self.tcu_params.pri_pulse_width = self.spin_pri_pulse_width.value()
        self.tcu_params.pre_pulse = self.spin_prepulse.value()
        self.tcu_params.x_amp_delay = self.spin_x_amp_delay.value()
        self.tcu_params.l_amp_delay = self.spin_l_amp_delay.value()
        self.tcu_params.rex_delay = self.spin_rex_delay.value()
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

    def export_close(self):
        self.export()
        window.close()

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

    def _get_selected_rows(self):
        index_list = []
        for model_index in self.table_pulse_params.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        return index_list

    def edit_pulse(self):
        index_list = self._get_selected_rows()

        for index in index_list:
            print('editing pulse #' + str(index.row()+1))

        pulse = {'pulse_width': self.spin_rf_pulse_width.value(),
                 'pri': self.spin_pri.value(),
                 'pol_mode': self.combo_mode.currentIndex(),
                 'frequency': self.spin_frequency.value()}
        self.tcu_params.pulses[index.row()] = pulse
        self.update_table()

    def remove_pulse(self):
        index_list = self._get_selected_rows()

        for index in index_list:
            print('deleting pulse #' + str(index.row()+1))
            del self.tcu_params.pulses[index.row()]
        self.update_table()

    def update_table(self):
        self.table_pulse_params.setRowCount(len(self.tcu_params.pulses))
        for index, pulse_param in enumerate(self.tcu_params.pulses):
            self.table_pulse_params.setItem(index, 0, QTableWidgetItem(str(pulse_param['pulse_width'])))
            self.table_pulse_params.setItem(index, 1, QTableWidgetItem(str(pulse_param['pri'])))
            self.table_pulse_params.setItem(index, 2, QTableWidgetItem(str(pulse_param['pol_mode'])))
            self.table_pulse_params.setItem(index, 3, QTableWidgetItem(str(pulse_param['frequency'])))

        if len(self.tcu_params.pulses) > 0:
            # self.table_pulse_params.selectRow(len(self.tcu_params.pulses) - 1)
            self.button_export.setEnabled(True)
            self.button_export_close.setEnabled(True)
        else:
            self.button_export.setEnabled(False)
            self.button_export_close.setEnabled(False)

        if len(self.tcu_params.pulses) < 32:
            self.button_add_pulse.setEnabled(True)
        else:
            self.button_add_pulse.setEnabled(False)
        index_list = self._get_selected_rows()
        if len(index_list) > 0:
            self.button_edit_pulse.setEnabled(True)
            self.button_remove_pulse.setEnabled(True)
            self.label_pulse_index.setText("Pulse " + str(index_list[0].row()+1) + " of " + str(len(self.tcu_params.pulses)))

        else:
            self.button_edit_pulse.setEnabled(False)
            self.button_remove_pulse.setEnabled(False)
            self.label_pulse_index.setText("No pulse selected")

    def update_selection(self):
        index_list = self._get_selected_rows()
        if len(index_list) > 0:
            self.label_pulse_index.setText("Pulse " + str(index_list[0].row()+1) + " of " + str(len(self.tcu_params.pulses)))
            selected_pulse = self.tcu_params.pulses[index_list[0].row()]
            self.spin_rf_pulse_width.setProperty("value", selected_pulse['pulse_width'])
            self.spin_pri.setProperty("value", selected_pulse['pri'])
            self.combo_mode.setCurrentIndex(selected_pulse['pol_mode'])
            self.update_frequency_band()
            self.spin_frequency.setProperty("value", selected_pulse['frequency'])
            self.button_edit_pulse.setEnabled(True)
            self.button_remove_pulse.setEnabled(True)
            self.label_pulse_index.setText("Pulse " + str(index_list[0].row()+1) + " of " + str(len(self.tcu_params.pulses)))
        else:
            self.button_edit_pulse.setEnabled(False)
            self.button_remove_pulse.setEnabled(False)
            self.label_pulse_index.setText("No pulse selected")

    def update_frequency_band(self):
        # TODO: remove magic numbers
        if self.combo_mode.currentIndex() in range(4):
            self.spin_frequency.setRange(1235, 1365)
        else:
            self.spin_frequency.setRange(8500, 9200)

    def update_metadata(self):
        samples_per_pri = self.spin_samples_per_pri.value()
        num_pulses = len(self.tcu_params.pulses)
        num_repeats = self.spin_num_repeats.value()
        time_block_microseconds = 0
        for pulse in self.tcu_params.pulses:
            time_block_microseconds += pulse['pri']
        time_experiment_microseconds = time_block_microseconds * num_repeats
        time_experiment_seconds = time_experiment_microseconds / 1000000
        num_pris = num_pulses * num_repeats
        num_samples = num_pris * samples_per_pri
        experiment_size_bits = num_samples * 32
        experiment_size_bytes = experiment_size_bits // 8
        experiment_megabytes = experiment_size_bytes // (1024*1024)

        # print('samples_per_pri = ' + str(samples_per_pri))
        # print('num_pulses = ' + str(num_pulses))
        # print('num_repeats = ' + str(num_repeats))
        # print('time_block = ' + str(time_block_microseconds))
        # print('time_experiment_microseconds = ' + str(time_experiment_microseconds))
        # print('time_experiment_seconds = ' + str(time_experiment_seconds))
        # time_experiment_minutes = time_experiment_seconds/60
        # print('time_experiment_minutes = ' + str(time_experiment_minutes))
        # time_experiment_hours = time_experiment_minutes/60
        # print('time_experiment_hours = ' + str(time_experiment_hours))
        # TODO: clip values over 24 hrs
        if time_experiment_seconds < 86400:
            self.lcdNumber_time.display(str(datetime.timedelta(seconds=int(time_experiment_seconds))))
        else:
            self.lcdNumber_time.display('large')
        self.lcdNumber_size.display(str(experiment_megabytes))

    def toggle_params(self):
        if self.display_more_pulses:
            self.display_more_pulses = False
            self.button_more_params.setText('Show More')
            self.label_clk_period.setProperty("visible", False)
            self.spin_clk_period.setProperty("visible", False)
            self.label_pri_pulse_width.setProperty("visible", False)
            self.spin_pri_pulse_width.setProperty("visible", False)
            self.label_prepulse.setProperty("visible", False)
            self.spin_prepulse.setProperty("visible", False)
            self.label_x_amp_delay.setProperty("visible", False)
            self.spin_x_amp_delay.setProperty("visible", False)
            self.label_l_amp_delay.setProperty("visible", False)
            self.spin_l_amp_delay.setProperty("visible", False)
            self.label_rex_delay.setProperty("visible", False)
            self.spin_rex_delay.setProperty("visible", False)
            self.label_dac_delay.setProperty("visible", False)
            self.spin_dac_delay.setProperty("visible", False)
            self.label_adc_delay.setProperty("visible", False)
            self.spin_adc_delay.setProperty("visible", False)
        else:
            self.display_more_pulses = True
            self.button_more_params.setText('Show Less')
            self.label_clk_period.setProperty("visible", True)
            self.spin_clk_period.setProperty("visible", True)
            self.label_pri_pulse_width.setProperty("visible", True)
            self.spin_pri_pulse_width.setProperty("visible", True)
            self.label_prepulse.setProperty("visible", True)
            self.spin_prepulse.setProperty("visible", True)
            self.label_x_amp_delay.setProperty("visible", True)
            self.spin_x_amp_delay.setProperty("visible", True)
            self.label_l_amp_delay.setProperty("visible", True)
            self.spin_l_amp_delay.setProperty("visible", True)
            self.label_rex_delay.setProperty("visible", True)
            self.spin_rex_delay.setProperty("visible", True)
            self.label_dac_delay.setProperty("visible", True)
            self.spin_dac_delay.setProperty("visible", True)
            self.label_adc_delay.setProperty("visible", True)
            self.spin_adc_delay.setProperty("visible", True)

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
