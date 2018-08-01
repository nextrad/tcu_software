import npyscreen


class TCUMonitorForm(npyscreen.Form):

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.keypress_timeout = 10  # refresh period in 100ms (10 = 1s)
        self.text_address = self.add(npyscreen.TitleText, name='IP Address', editable=False, value='192.168.1.36')
        self.text_connection = self.add(npyscreen.TitleText, name='Connection', editable=False, value='Disconnected')
        self.text_state = self.add(npyscreen.TitleText, name='State', editable=False, value='?')
        self.text_num_pulses = self.add(npyscreen.TitleText, name='Pulses', editable=False, value='?')
        self.text_num_repeats = self.add(npyscreen.TitleText, name='Repeats', editable=False, value='?')
        self.text_pre_pulse = self.add(npyscreen.TitleText, name='Pre Pulse', editable=False, value='?')
        self.text_x_amp_delay = self.add(npyscreen.TitleText, name='X Amp Delay', editable=False, value='?')
        self.text_l_amp_delay = self.add(npyscreen.TitleText, name='L Amp Delay', editable=False, value='?')
        self.text_rex_delay = self.add(npyscreen.TitleText, name='Rex Delay', editable=False, value='?')
        self.grid_pulses = self.add(npyscreen.GridColTitles, name='Pulses', editable=False, height=7, max_height=10)
        self.grid_pulses.col_titles =[ 'Pulse', 'Pulse Width', 'PRI', 'Mode', 'Frequency']
        self.grid_pulses.values = [
                                    ['0', '10.0', '1000', '0', '1300'],
                                    ['1', '10.0', '1000', '1', '1300'],
                                    ['2', '10.0', '1000', '2', '1300'],
                                    ['3', '10.0', '1000', '3', '1300'],
                                    ['4', '10.0', '1000', '4', '8500'],
                                    ['5', '10.0', '1000', '5', '8500'],
                                  ]
        self.button_arm = self.add(npyscreen.ButtonPress, name='Arm')
        self.button_arm.whenPressed = self.when_pressed_arm

    def when_pressed_arm(self):
        self.button_arm.name = 'disarm'

    def while_waiting(self):
        # called every keypress_timeout period when user not interacting
        pass


class TCUMonitorApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TCUMonitorForm, name='TCU MONITOR')


if __name__ == '__main__':
    app = TCUMonitorApplication()
    app.run()
