import configparser
import logging
import os.path
import sys


class HeaderFileParser(object):
    """NeXtRAD.ini File Parser"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logging.getLogger('header_file_parser_logger')
        self.file_parser = configparser.ConfigParser()

        self.file_parser['PulseParameters'] = {'WAVEFORM_INDEX': '',
                                               'NUM_PRIS': '',
                                               'PRE_PULSE': '',
                                               'PRI_PULSE_WIDTH': '',
                                               'X_AMP_DELAY': '',
                                               'L_AMP_DELAY': '',
                                               'PULSES': ''}

    def __str__(self):
        params = ''
        params += 'waveform_index: ' + str(self.file_parser['PulseParameters']['WAVEFORM_INDEX']) + '\n'
        params += 'num_pris: ' + str(self.file_parser['PulseParameters']['NUM_PRIS']) + '\n'
        params += 'pre_pulse: ' + str(self.file_parser['PulseParameters']['PRE_PULSE']) + '\n'
        params += 'pri_pulse_width: ' + str(self.file_parser['PulseParameters']['PRI_PULSE_WIDTH']) + '\n'
        params += 'x_amp_delay: ' + str(self.file_parser['PulseParameters']['X_AMP_DELAY']) + '\n'
        params += 'l_amp_delay: ' + str(self.file_parser['PulseParameters']['L_AMP_DELAY']) + '\n'
        params += 'pulses: ' + self.file_parser['PulseParameters']['PULSES']
        return params

    def read_header(self):
        """ Parses a given header file for TCU parameters """

        self.header_file = self.file_parser.read(self.file_name)
        if len(self.header_file) > 0:
            if not self.file_parser.has_section('PulseParameters'):
                self.logger.error('No "PulseParameters" section found in '
                                  'header file "{}"'.format(self.file_name))
        else:
            self.logger.error('Could not find header file "{}", no '
                              'parameters extracted'.format(self.file_name))

    def get_tcu_params(self):
        """ Returns a dictionary containing TCU parameters

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
        tcu_params = dict()
        if len(self.header_file) > 0:
            if self.file_parser.has_section('PulseParameters'):
                pulses = self._extract_param('PULSES')
                pulses = pulses.replace('"', '')
                pulses_list = pulses.split('|')
                tcu_params['num_pulses'] = len(pulses_list)
                num_pris = eval(self._extract_param('NUM_PRIS'))
                tcu_params['num_repeats'] = num_pris//tcu_params['num_pulses']
                tcu_params['pri_pulse_width'] = eval(self._extract_param('PRI_PULSE_WIDTH'))
                tcu_params['pre_pulse'] = eval(self._extract_param('PRE_PULSE'))
                tcu_params['x_amp_delay'] = eval(self._extract_param('X_AMP_DELAY'))
                tcu_params['l_amp_delay'] = eval(self._extract_param('L_AMP_DELAY'))
                tcu_params['pulses'] = []
                for pulse in pulses_list:
                    pulse_params = pulse.split(',')
                    pulse_param_dict = {'pulse_width':eval(pulse_params[0]),
                                        'pri':eval(pulse_params[1]),
                                        'pol_mode':eval(pulse_params[2]),
                                        'frequency':eval(pulse_params[3])}
                    tcu_params['pulses'].append(pulse_param_dict)
            else:
                self.logger.error('No "PulseParameters" section found in '
                                  'header file "{}"'.format(self.file_name))
        else:
            self.logger.error('Could not find header file "{}", no '
                              'parameters extracted'.format(self.file_name))

        return tcu_params

    def _extract_param(self, param):
        """ returns the value of given param name

            program exists if parameter is not found
        """
        result = ""
        try:
            result = self.file_parser['PulseParameters'][param]
        except Exception as e:
            self.logger.error('Could not find required parameter "{}"'
                              .format(param, self.file_name))
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
        # TODO: check that all the required items exist in the params argument
        self.file_parser['PulseParameters']['PULSES'] = '""'
        test = '"'
        for index, pulse in enumerate(params['pulses']):
            self.file_parser['PulseParameters']['PULSES'] += str(pulse['pulse_width'])+','+str(pulse['pri'])+','+str(pulse['pol_mode'])+','+str(pulse['frequency'])
            test += str(pulse['pulse_width'])+','+str(pulse['pri'])+','+str(pulse['pol_mode'])+','+str(pulse['frequency'])
            if index < (len(params['pulses']) - 1):
                self.file_parser['PulseParameters']['PULSES'] += '|'
                test += '|'
        test += '"'
        print(test)
        self.file_parser['PulseParameters']['NUM_PRIS'] = ''
        self.file_parser['PulseParameters']['PRI_PULSE_WIDTH'] = str(params['pri_pulse_width'])
        self.file_parser['PulseParameters']['PRE_PULSE'] = str(params['pre_pulse'])
        self.file_parser['PulseParameters']['X_AMP_DELAY'] = str(params['x_amp_delay'])
        self.file_parser['PulseParameters']['L_AMP_DELAY'] = str(params['l_amp_delay'])


if __name__ == '__main__':
    # hfparser = HeaderFileParser('../../nextrad_header/NeXtRAD.ini')
    hfparser = HeaderFileParser('../../nextrad_header/NeXtRAD')

    test_params = {'pre_pulse': 30,
                   'x_amp_delay': 3.5,
                   'l_amp_delay': 1.0,
                   'num_pulses': 2,
                   'num_repeats': 75000,
                   'pri_pulse_width': 500,
                   'pulses': [{'pol_mode': 4, 'frequency': 8500.0, 'pri': 500.0, 'pulse_width': 10.0},
                              {'pol_mode': 5, 'frequency': 8500.0, 'pri': 500.0, 'pulse_width': 10.0}]}
