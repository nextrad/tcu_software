import configparser
import logging
import os.path
import sys

class HeaderFileParser(object):
    """NeXtRAD.ini File Parser"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logging.getLogger('header_file_parser_logger')
        self.tcu_params = {'num_pulses':'', 'num_repeats':'', 'pri_pulse_width':'', 'pre_pulse':'', 'x_amp_delay':'', 'l_amp_delay':'', 'pulses':''}
        # if not os.path.isfile(self.file_name):
        #     self.logger.error('could not find header file "{}"'
        #                       .format(file_name))
        self.file_parser = configparser.ConfigParser()
        self.header_file = self.file_parser.read(self.file_name)
        if len(self.header_file) == 0:
            self.logger.info('No existing header file found...')
        else:
            self.pulse_parameters_section = self.file_parser['PulseParameters']

    def __str__(self):
        params = ''
        params += 'num_pulses: ' + str(self.tcu_params['num_pulses']) + '\n'
        params += 'num_repeats: ' + str(self.tcu_params['num_repeats']) + '\n'
        params += 'pre_pulse: ' + str(self.tcu_params['pre_pulse']) + '\n'
        params += 'pri_pulse_width: ' + str(self.tcu_params['pri_pulse_width']) + '\n'
        params += 'x_amp_delay: ' + str(self.tcu_params['x_amp_delay']) + '\n'
        params += 'l_amp_delay: ' + str(self.tcu_params['l_amp_delay']) + '\n'
        params += 'pulses: ' + '\n'
        for index, pulse in enumerate(self.tcu_params['pulses']):
            params += '\tpulse[' + str(index) + ']' + '\n'
        return params

    def get_tcu_params(self):
        """ Returns a dictionary containing TCU parameters found in the header file

            The dictionary contains the following items:

                'num_pulses'        ->  int
                'num_repeats'       ->  int
                'pri_pulse_width'   ->  float
                'pre_pulse'         ->  float
                'x_amp_delay'       ->  float
                'l_amp_delay'       ->  float
                'pulses'            ->  list of dictionary types containing:
                                            'pri'           ->  float
                                            'pol_mode'      ->  int
                                            'pulse_width'   ->  float
                                            'frequency'     ->  float
        """
        if len(self.header_file) > 0:
            if self.file_parser.has_section('PulseParameters'):
                self.pulse_parameters_section = self.file_parser['PulseParameters']
                pulses = self._extract_param('PULSES')
                pulses = pulses.replace('"', '')
                pulses_list = pulses.split('|')
                self.tcu_params['num_pulses'] = len(pulses_list)
                num_pris = eval(self._extract_param('NUM_PRIS'))
                self.tcu_params['num_repeats'] = num_pris//self.tcu_params['num_pulses']
                self.tcu_params['pri_pulse_width'] = eval(self._extract_param('PRI_PULSE_WIDTH'))
                self.tcu_params['pre_pulse'] = eval(self._extract_param('PRE_PULSE'))
                self.tcu_params['x_amp_delay'] = eval(self._extract_param('X_AMP_DELAY'))
                self.tcu_params['l_amp_delay'] = eval(self._extract_param('L_AMP_DELAY'))
                self.tcu_params['pulses'] = []
                for pulse in pulses_list:
                    pulse_params = pulse.split(',')
                    pulse_param_dict = {'pulse_width':eval(pulse_params[0]),
                                        'pri':eval(pulse_params[1]),
                                        'pol_mode':eval(pulse_params[2]),
                                        'frequency':eval(pulse_params[3])}
                    self.tcu_params['pulses'].append(pulse_param_dict)
            else:
                self.logger.error('Could not find "PulseParameters" section in header file')
        else:
            self.logger.warning('No existing header file was found, no parameters to extract')

        return self.tcu_params

    def _extract_param(self, param):
        """ returns the value of given param name

            program exists if parameter is not found
        """
        result = ""
        try:
            result = self.pulse_parameters_section[param]
        except Exception as e:
            self.logger.error("Could not find required parameter '{}' from header file".format(param))
            exit(65)
        return result

    def set_tcu_params(self, params):
        """ writes tcu params to header file

            'params' expects a dictionary containing the following items:

                'num_pulses'        ->  int
                'num_repeats'       ->  int
                'pri_pulse_width'   ->  float
                'pre_pulse'         ->  float
                'x_amp_delay'       ->  float
                'l_amp_delay'       ->  float
                'pulses'            ->  list of dictionary types containing:
                                            'pri'           ->  float
                                            'pol_mode'      ->  int
                                            'pulse_width'   ->  float
                                            'frequency'     ->  float
        """
        # TODO: check that all the required items exist in the params argument
        self.pulse_parameters_section['PULSES'] = '""'
        test = '""'
        for index, pulse in enumerate(params['pulses']):
            self.pulse_parameters_section['PULSES'] += str(pulse['pulse_width'])+','+str(pulse['pri'])+','+str(pulse['pol_mode'])+','+str(pulse['frequency'])
            test += str(pulse['pulse_width'])+','+str(pulse['pri'])+','+str(pulse['pol_mode'])+','+str(pulse['frequency'])+','
            if index < (len(params['pulses']) - 1):
                self.pulse_parameters_section['PULSES'] += '|'
                test += '|'

        print (test)
        # self.pulse_parameters_section['NUM_PRIS']) = params['']
        # self.pulse_parameters_section['PRI_PULSE_WIDTH']) = params['pri_pulse_width']
        # self.pulse_parameters_section['PRE_PULSE']) = params['pre_pulse']
        # self.pulse_parameters_section['X_AMP_DELAY']) = params['x_amp_delay']
        # self.pulse_parameters_section['L_AMP_DELAY']) = params['l_amp_delay']
