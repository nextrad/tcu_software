import configparser
import logging
import os.path
import sys


class HeaderFileParser(object):
    """NeXtRAD.ini File Parser"""
    def __init__(self, file_name = ''):
        self.logger = logging.getLogger('header_file_parser_logger')
        self.file_parser = configparser.ConfigParser()
        self.file_parser.optionxform = str # retain upper case for keys
        self.file_parser['PulseParameters'] = {'WAVEFORM_INDEX': '0',
                                               'NUM_PRIS': '0',
                                               'PRE_PULSE': '0',
                                               'PRI_PULSE_WIDTH': '0',
                                               'X_AMP_DELAY': '0',
                                               'L_AMP_DELAY': '0',
                                               'DAC_DELAY': '0',
                                               'ADC_DELAY': '0',
                                               'SAMPLES_PER_PRI': '0',
                                               'PULSES': '""'}
        if file_name != '':
            self.read_header(file_name)

    def __str__(self):
        params = ''
        params += 'waveform_index: ' + str(self.file_parser['PulseParameters']['WAVEFORM_INDEX']) + '\n'
        params += 'num_pris: ' + str(self.file_parser['PulseParameters']['NUM_PRIS']) + '\n'
        params += 'pre_pulse: ' + str(self.file_parser['PulseParameters']['PRE_PULSE']) + '\n'
        params += 'pri_pulse_width: ' + str(self.file_parser['PulseParameters']['PRI_PULSE_WIDTH']) + '\n'
        params += 'x_amp_delay: ' + str(self.file_parser['PulseParameters']['X_AMP_DELAY']) + '\n'
        params += 'l_amp_delay: ' + str(self.file_parser['PulseParameters']['L_AMP_DELAY']) + '\n'
        params += 'dac_delay: ' + str(self.file_parser['PulseParameters']['DAC_DELAY']) + '\n'
        params += 'adc_delay: ' + str(self.file_parser['PulseParameters']['ADC_DELAY']) + '\n'
        params += 'samples_per_pri: ' + str(self.file_parser['PulseParameters']['SAMPLES_PER_PRI']) + '\n'
        params += 'pulses: ' + self.file_parser['PulseParameters']['PULSES']
        return params

    def read_header(self, file_name):
        """ Parses a given header file for TCU parameters """

        self.header_file = self.file_parser.read(file_name)
        if len(self.header_file) > 0:
            if not self.file_parser.has_section('PulseParameters'):
                self.logger.error('No "PulseParameters" section found in '
                                  'header file "{}"'.format(file_name))
        else:
            self.logger.error('Could not find header file "{}", no '
                              'parameters extracted'.format(file_name))

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
                'dac_delay'         ->  int
                'adc_delay'         ->  int
                'samples_per_pri'   ->  int
                'waveform_index'    ->  int
        """
        tcu_params = dict()
        if self.file_parser.has_section('PulseParameters'):
            pulses = self._extract_param('PULSES')
            pulses = pulses.replace('"', '')
            pulses_list = pulses.split('|')
            if pulses_list == ['']:
                pulses_list.clear()
            tcu_params['num_pulses'] = len(pulses_list)
            num_pris = eval(self._extract_param('NUM_PRIS'))
            if tcu_params['num_pulses'] != 0:
                tcu_params['num_repeats'] = num_pris//tcu_params['num_pulses']
            else:
                tcu_params['num_repeats'] = 0
            tcu_params['pri_pulse_width'] = eval(self._extract_param('PRI_PULSE_WIDTH'))
            tcu_params['pre_pulse'] = eval(self._extract_param('PRE_PULSE'))
            tcu_params['x_amp_delay'] = eval(self._extract_param('X_AMP_DELAY'))
            tcu_params['l_amp_delay'] = eval(self._extract_param('L_AMP_DELAY'))
            tcu_params['dac_delay'] = eval(self._extract_param('DAC_DELAY'))
            tcu_params['adc_delay'] = eval(self._extract_param('ADC_DELAY'))
            tcu_params['samples_per_pri'] = eval(self._extract_param('SAMPLES_PER_PRI'))
            tcu_params['waveform_index'] = eval(self._extract_param('WAVEFORM_INDEX'))
            tcu_params['pulses'] = []
            for pulse in pulses_list:
                pulse_params = pulse.split(',')
                pulse_param_dict = {'pulse_width':eval(pulse_params[0]),
                                    'pri':eval(pulse_params[1]),
                                    'pol_mode':eval(pulse_params[2]),
                                    'frequency':eval(pulse_params[3])}
                tcu_params['pulses'].append(pulse_param_dict)
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


    # NOTE: Simply using 'self.file_parser.write(headerfile)' will change the
    #       existing header's format and remove its comments. This could be
    #       fixed using configobj module. For now, a temporary ini file is
    #       generated for the cnc cpp software to parse.
    def write_header(self, file_name):
        """ writes tcu params to header file """
        with open(file_name, 'w') as configfile:
            configfile.write('# Intermediary ini file for TCU\n')
            configfile.write('[PulseParameters]\n')
            for key in self.file_parser['PulseParameters']:
                configfile.write(key + ' = ' + self.file_parser['PulseParameters'][key]+'\n')

    def set_tcu_params(self, params):
        """ sets parser with given parameters

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
                'dac_delay'         ->  int
                'adc_delay'         ->  int
                'samples_per_pri'   ->  int
                'waveform_index'    ->  int
        """
        # TODO: check that all the required items exist in the params argument
        self.file_parser['PulseParameters']['PULSES'] = '"'
        for index, pulse in enumerate(params['pulses']):
            self.file_parser['PulseParameters']['PULSES'] += str(pulse['pulse_width'])+','+str(pulse['pri'])+','+str(pulse['pol_mode'])+','+str(pulse['frequency'])
            if index < (len(params['pulses']) - 1):
                self.file_parser['PulseParameters']['PULSES'] += '|'
        self.file_parser['PulseParameters']['PULSES'] += '"'
        self.file_parser['PulseParameters']['NUM_PRIS'] = str(params['num_pulses'] * params['num_repeats'])
        self.file_parser['PulseParameters']['PRI_PULSE_WIDTH'] = str(params['pri_pulse_width'])
        self.file_parser['PulseParameters']['PRE_PULSE'] = str(params['pre_pulse'])
        self.file_parser['PulseParameters']['X_AMP_DELAY'] = str(params['x_amp_delay'])
        self.file_parser['PulseParameters']['L_AMP_DELAY'] = str(params['l_amp_delay'])
        self.file_parser['PulseParameters']['DAC_DELAY'] = str(params['dac_delay'])
        self.file_parser['PulseParameters']['ADC_DELAY'] = str(params['adc_delay'])
        self.file_parser['PulseParameters']['SAMPLES_PER_PRI'] = str(params['samples_per_pri'])
        self.file_parser['PulseParameters']['WAVEFORM_INDEX'] = str(params['waveform_index'])


if __name__ == '__main__':
    hfparser = HeaderFileParser()
    hfdir = '../nextrad_header/NeXtRAD.ini'
    test_params = {'pre_pulse': 30,
                   'x_amp_delay': 3.5,
                   'l_amp_delay': 1.0,
                   'dac_delay': 1,
                   'adc_delay': 372,
                   'samples_per_pri': 2048,
                   'waveform_index': 5,
                   'num_pulses': 2,
                   'num_repeats': 75000,
                   'pri_pulse_width': 100,
                   'pulses': [{'pol_mode': 4, 'frequency': 8500.0, 'pri': 500.0, 'pulse_width': 10.0},
                              {'pol_mode': 5, 'frequency': 8500.0, 'pri': 500.0, 'pulse_width': 10.0}]}
