# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'creator_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(672, 478)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_export = QtWidgets.QPushButton(self.frame)
        self.button_export.setEnabled(False)
        self.button_export.setObjectName("button_export")
        self.horizontalLayout.addWidget(self.button_export)
        self.button_export_close = QtWidgets.QPushButton(self.frame)
        self.button_export_close.setEnabled(False)
        self.button_export_close.setObjectName("button_export_close")
        self.horizontalLayout.addWidget(self.button_export_close)
        self.gridLayout.addWidget(self.frame, 3, 1, 1, 1)
        self.table_pulse_params = QtWidgets.QTableWidget(self.centralwidget)
        self.table_pulse_params.setMinimumSize(QtCore.QSize(391, 61))
        self.table_pulse_params.setAutoScroll(True)
        self.table_pulse_params.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_pulse_params.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_pulse_params.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_pulse_params.setObjectName("table_pulse_params")
        self.table_pulse_params.setColumnCount(4)
        self.table_pulse_params.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(3, item)
        self.table_pulse_params.horizontalHeader().setDefaultSectionSize(97)
        self.gridLayout.addWidget(self.table_pulse_params, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spin_rf_pulse_width = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spin_rf_pulse_width.setSingleStep(0.1)
        self.spin_rf_pulse_width.setProperty("value", 10.0)
        self.spin_rf_pulse_width.setObjectName("spin_rf_pulse_width")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_rf_pulse_width)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spin_pri = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spin_pri.setMaximum(9999999.99)
        self.spin_pri.setSingleStep(0.1)
        self.spin_pri.setProperty("value", 1000.0)
        self.spin_pri.setObjectName("spin_pri")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spin_pri)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.combo_mode = QtWidgets.QComboBox(self.groupBox)
        self.combo_mode.setObjectName("combo_mode")
        self.combo_mode.addItem("")
        self.combo_mode.addItem("")
        self.combo_mode.addItem("")
        self.combo_mode.addItem("")
        self.combo_mode.addItem("")
        self.combo_mode.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.combo_mode)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spin_frequency = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spin_frequency.setDecimals(0)
        self.spin_frequency.setMaximum(10000.0)
        self.spin_frequency.setSingleStep(1.0)
        self.spin_frequency.setProperty("value", 1300.0)
        self.spin_frequency.setObjectName("spin_frequency")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spin_frequency)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_remove_pulse = QtWidgets.QPushButton(self.widget)
        self.button_remove_pulse.setEnabled(False)
        self.button_remove_pulse.setObjectName("button_remove_pulse")
        self.horizontalLayout_2.addWidget(self.button_remove_pulse)
        self.button_add_pulse = QtWidgets.QPushButton(self.widget)
        self.button_add_pulse.setObjectName("button_add_pulse")
        self.horizontalLayout_2.addWidget(self.button_add_pulse)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.widget)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.spin_clk_period = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_clk_period.setMaximum(999999.99)
        self.spin_clk_period.setProperty("value", 10.0)
        self.spin_clk_period.setObjectName("spin_clk_period")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_clk_period)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spin_num_pulses = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_num_pulses.setMinimum(1)
        self.spin_num_pulses.setMaximum(32)
        self.spin_num_pulses.setObjectName("spin_num_pulses")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spin_num_pulses)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.spin_num_repeats = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_num_repeats.setMinimum(1)
        self.spin_num_repeats.setMaximum(999999999)
        self.spin_num_repeats.setDisplayIntegerBase(10)
        self.spin_num_repeats.setObjectName("spin_num_repeats")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spin_num_repeats)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.spin_pri_pulse_width = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_pri_pulse_width.setMaximum(999999999.0)
        self.spin_pri_pulse_width.setProperty("value", 500.0)
        self.spin_pri_pulse_width.setObjectName("spin_pri_pulse_width")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spin_pri_pulse_width)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spin_prepulse = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_prepulse.setMaximum(999.99)
        self.spin_prepulse.setSingleStep(0.1)
        self.spin_prepulse.setProperty("value", 30.0)
        self.spin_prepulse.setObjectName("spin_prepulse")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spin_prepulse)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.spin_x_amp_delay = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_x_amp_delay.setSingleStep(0.1)
        self.spin_x_amp_delay.setProperty("value", 1.6)
        self.spin_x_amp_delay.setObjectName("spin_x_amp_delay")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spin_x_amp_delay)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.spin_l_amp_delay = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_l_amp_delay.setSingleStep(0.1)
        self.spin_l_amp_delay.setProperty("value", 1.0)
        self.spin_l_amp_delay.setObjectName("spin_l_amp_delay")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spin_l_amp_delay)
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.spin_rex_delay = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_rex_delay.setSingleStep(0.1)
        self.spin_rex_delay.setProperty("value", 1.0)
        self.spin_rex_delay.setObjectName("spin_rex_delay")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.spin_rex_delay)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.spin_dac_delay = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_dac_delay.setMaximum(999999999)
        self.spin_dac_delay.setProperty("value", 1)
        self.spin_dac_delay.setObjectName("spin_dac_delay")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spin_dac_delay)
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.spin_adc_delay = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_adc_delay.setMaximum(999999999)
        self.spin_adc_delay.setProperty("value", 372)
        self.spin_adc_delay.setObjectName("spin_adc_delay")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.spin_adc_delay)
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.spin_samples_per_pri = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_samples_per_pri.setMaximum(999999999)
        self.spin_samples_per_pri.setProperty("value", 2048)
        self.spin_samples_per_pri.setObjectName("spin_samples_per_pri")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.spin_samples_per_pri)
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.combo_waveform_index = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_waveform_index.setObjectName("combo_waveform_index")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.combo_waveform_index.addItem("")
        self.formLayout_2.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.combo_waveform_index)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 2, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_17 = QtWidgets.QLabel(self.frame_2)
        self.label_17.setGeometry(QtCore.QRect(10, 10, 102, 17))
        self.label_17.setObjectName("label_17")
        self.lcdNumber_time = QtWidgets.QLCDNumber(self.frame_2)
        self.lcdNumber_time.setGeometry(QtCore.QRect(118, 10, 101, 31))
        self.lcdNumber_time.setDigitCount(8)
        self.lcdNumber_time.setObjectName("lcdNumber_time")
        self.label_18 = QtWidgets.QLabel(self.frame_2)
        self.label_18.setGeometry(QtCore.QRect(230, 10, 55, 17))
        self.label_18.setObjectName("label_18")
        self.lcdNumber_size = QtWidgets.QLCDNumber(self.frame_2)
        self.lcdNumber_size.setGeometry(QtCore.QRect(288, 10, 81, 31))
        self.lcdNumber_size.setObjectName("lcdNumber_size")
        self.gridLayout.addWidget(self.frame_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setEnabled(True)
        self.actionPreferences.setObjectName("actionPreferences")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TCU Parameter Editor"))
        self.button_export.setText(_translate("MainWindow", "Export"))
        self.button_export_close.setText(_translate("MainWindow", "Export + Close"))
        item = self.table_pulse_params.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Pulse width"))
        item = self.table_pulse_params.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "PRI"))
        item = self.table_pulse_params.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mode"))
        item = self.table_pulse_params.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Frequency"))
        self.groupBox.setTitle(_translate("MainWindow", "Pulse Parameters"))
        self.label_2.setText(_translate("MainWindow", "RF Pulse width [μs]"))
        self.label_3.setText(_translate("MainWindow", "PRI [μs]"))
        self.label_5.setText(_translate("MainWindow", "Pol. Mode"))
        self.combo_mode.setItemText(0, _translate("MainWindow", "0: L-VV"))
        self.combo_mode.setItemText(1, _translate("MainWindow", "1: L-VH"))
        self.combo_mode.setItemText(2, _translate("MainWindow", "2: L-HV"))
        self.combo_mode.setItemText(3, _translate("MainWindow", "3: L-HH"))
        self.combo_mode.setItemText(4, _translate("MainWindow", "4: X-HV/H"))
        self.combo_mode.setItemText(5, _translate("MainWindow", "5: X-VV/H"))
        self.label_4.setText(_translate("MainWindow", "Frequency [MHz]"))
        self.button_remove_pulse.setText(_translate("MainWindow", "Remove"))
        self.button_add_pulse.setText(_translate("MainWindow", "Add"))
        self.groupBox_2.setTitle(_translate("MainWindow", "General Parameters"))
        self.label_11.setText(_translate("MainWindow", "Clock Period [ns]"))
        self.label_6.setText(_translate("MainWindow", "Number of pulses"))
        self.label_7.setText(_translate("MainWindow", "Number of repeats"))
        self.label_10.setText(_translate("MainWindow", "Pulse width [μs]"))
        self.label.setText(_translate("MainWindow", "Prepulse  [μs]"))
        self.label_8.setText(_translate("MainWindow", "X amp delay [μs]"))
        self.label_9.setText(_translate("MainWindow", "L amp delay [μs]"))
        self.label_16.setText(_translate("MainWindow", "REX delay [μs]"))
        self.label_12.setText(_translate("MainWindow", "DAC Delay"))
        self.label_13.setText(_translate("MainWindow", "ADC Delay"))
        self.label_14.setText(_translate("MainWindow", "Samples / PRI"))
        self.label_15.setText(_translate("MainWindow", "Waveform Index"))
        self.combo_waveform_index.setItemText(0, _translate("MainWindow", "1:   0.5   [LFM]"))
        self.combo_waveform_index.setItemText(1, _translate("MainWindow", "2:   1.0   [LFM]"))
        self.combo_waveform_index.setItemText(2, _translate("MainWindow", "3:   3.0   [LFM]"))
        self.combo_waveform_index.setItemText(3, _translate("MainWindow", "4:   5.0   [LFM]"))
        self.combo_waveform_index.setItemText(4, _translate("MainWindow", "5:   10.0 [LFM]"))
        self.combo_waveform_index.setItemText(5, _translate("MainWindow", "6:   15.0 [LFM]"))
        self.combo_waveform_index.setItemText(6, _translate("MainWindow", "7:   20.0 [LFM]"))
        self.combo_waveform_index.setItemText(7, _translate("MainWindow", "8:   0.5   [NLFM]"))
        self.combo_waveform_index.setItemText(8, _translate("MainWindow", "9:   1.0   [NLFM]"))
        self.combo_waveform_index.setItemText(9, _translate("MainWindow", "10: 3.0   [NLFM]"))
        self.combo_waveform_index.setItemText(10, _translate("MainWindow", "11: 5.0   [NLFM]"))
        self.combo_waveform_index.setItemText(11, _translate("MainWindow", "12: 10.0 [NLFM]"))
        self.combo_waveform_index.setItemText(12, _translate("MainWindow", "13: 15.0 [NLFM]"))
        self.combo_waveform_index.setItemText(13, _translate("MainWindow", "14: 20.0 [NLFM]"))
        self.label_17.setText(_translate("MainWindow", "Time [HH:MM:SS]:"))
        self.label_18.setText(_translate("MainWindow", "Size [MB]:"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionExport.setText(_translate("MainWindow", "Export..."))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

