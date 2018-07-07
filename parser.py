import configparser
import logging
import os.path
import sys
import prettytable

class HeaderFileParser(object):
    """NeXtRAD.ini File Parser"""
    def __init__(self, file_name=''):
        self.logger = logging.getLogger('header_file_parser_logger')
        self.file_parser = configparser.ConfigParser()
        self.file_parser.optionxform = str  # retain upper case for keys
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


class TCUParams(object):
    """docstring for TCUPulseParams."""

    def __init__(self, headerfile, outputfile='PulseParameters.ini'):
        # clk_period_ns=10, num_pulses=1, num_repeats=1, pri_pulse_width=50, pre_pulse=30, x_amp_delay=3.5, l_amp_delay=1.0, params=list()
        self.hfparser = HeaderFileParser(headerfile)
        self.outputfilename = outputfile
        params = self.hfparser.get_tcu_params()
        self.clk_period_ns = 10
        self.num_pulses = params['num_pulses']
        self.num_repeats = params['num_repeats']
        self.pri_pulse_width = params['pri_pulse_width']
        self.pre_pulse = params['pre_pulse']
        self.x_amp_delay = params['x_amp_delay']
        self.l_amp_delay = params['l_amp_delay']
        self.pulses = params['pulses']
        self.dac_delay = params['dac_delay']
        self.adc_delay = params['adc_delay']
        self.samples_per_pri = params['samples_per_pri']
        self.waveform_index = params['waveform_index']

    def __str__(self):
        ptable_global = prettytable.PrettyTable()
        ptable_global.field_names = ['Parameter', 'Value', 'Hex Cycles [little endian]']
        ptable_global.align['Parameter'] = 'l'
        hex_params = self.get_hex_params()
        ptable_global.add_row(['num_pulses', self.num_pulses, hex_params['num_pulses']])
        ptable_global.add_row(['num_repeats', self.num_repeats, hex_params['num_repeats']])
        ptable_global.add_row(
            ['pri_pulse_width', self.pri_pulse_width, hex_params['pri_pulse_width']])
        ptable_global.add_row(['pre_pulse', self.pre_pulse, hex_params['pre_pulse']])
        ptable_global.add_row(
            ['x_amp_delay', self.x_amp_delay, hex_params['x_amp_delay']])
        ptable_global.add_row(
            ['l_amp_delay', self.l_amp_delay, hex_params['l_amp_delay']])

        ptable_pulses = prettytable.PrettyTable()
        ptable_pulses.field_names = ['Pulse Number', 'Pulse Width', 'PRI', 'Mode', 'Frequency']
        for index, pulse in enumerate(self.pulses):
            ptable_pulses.add_row([index,
                                  str(pulse['pulse_width']) + ' : ' + hex_params['pulses'][index]['pulse_width'],
                                   '(' + str(pulse['pri']) + ') : [' + hex_params['pulses'][index]['pri'] + ']',
                                  str(pulse['pol_mode']) + ' : ' + hex_params['pulses'][index]['pol_mode'],
                                  str(pulse['frequency']) + ' : ' + hex_params['pulses'][index]['frequency']])

        return 'Global Params:\n' + str(ptable_global) + '\nPulse Params\n' + str(ptable_pulses) + '\n[PRIoffset] = (PRI) - pre_pulse - pulse_width'

    def export(self):
        """exports pulse parameters in NeXtRAD.ini format"""
        # TODO: use config parser for this
        #print('NUM_PULSES = {}'.format(self.num_pulses))
        #print('NUM_REPEATS = {}'.format(self.num_repeats))
        #print('PRI_PULSE_WIDTH = {}'.format(self.pri_pulse_width))
        #print('pre_pulse_DELAY = {}'.format(self.pre_pulse))
        #print('X_AMP_DELAY = {}'.format(self.x_amp_delay))
        #print('L_AMP_DELAY = {}'.format(self.l_amp_delay))
        #print('; PULSES = [<PULSE|PULSE|PULSE...>]')
        #print('; PULSE = [<p. width>, <pri>, <mode>, <freq>]')
        #print(self.to_pulses_string())
        #print()
        #self.to_vhdl_snippet()
        params = {'num_pulses':self.num_pulses,
                  'num_repeats':self.num_repeats,
                  'pri_pulse_width':self.pri_pulse_width,
                  'pre_pulse':self.pre_pulse,
                  'x_amp_delay':self.x_amp_delay,
                  'l_amp_delay':self.l_amp_delay,
                  'dac_delay':self.dac_delay,
                  'adc_delay':self.adc_delay,
                  'samples_per_pri':self.samples_per_pri,
                  'waveform_index':self.waveform_index,
                  'pulses':self.pulses}
        self.hfparser.set_tcu_params(params)
        self.hfparser.write_header(self.outputfilename)

    def to_pulses_string(self):
        pulses = 'PULSES = \"'
        for index, pulse in enumerate(self.pulses):
            # pulses += 'PULSE_' + str(index) + ' = \''
            pulses += str(pulse['pulse_width']) + ','
            pulses += str(pulse['pri']) + ','
            pulses += str(pulse['pol_mode']) + ','
            pulses += str(pulse['frequency'])
            if index < len(self.pulses) - 1:
                pulses += '|'
        pulses += '\"'
        return pulses

    def to_vhdl_snippet(self):
        print('copy this into HDL:')
        print()
        print('-'*100)
        clock_frequency = (1/(self.clk_period_ns * pow(10, -9))/1000000)
        print('-- system clock period : {}ns ({}MHz)'.format(self.clk_period_ns, clock_frequency))
        print('-'*100)
        print('num_pulses_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(self.num_pulses, big_endian=True, hdl=True), self.num_pulses))
        print('num_repeats_reg <= {};\t\t-- {}'.format(self._int_to_hex_str(self.num_repeats, big_endian=True, hdl=True), self.num_repeats))
        pri_pulse_width = (self._to_clock_ticks(self.pri_pulse_width))
        pri_pulse_width_hex_str = self._int_to_hex_str(pri_pulse_width, big_endian=True, hdl=True)
        print('pri_pulse_width_reg <= {};\t\t-- {}'.format(pri_pulse_width_hex_str, self.pri_pulse_width))
        pre_pulse = (self._to_clock_ticks(self.pre_pulse))
        pre_pulse_hex_str = self._int_to_hex_str(pre_pulse, big_endian=True, hdl=True)
        print('pre_pulse_reg <= {};\t\t-- {}'.format(pre_pulse_hex_str, self.pre_pulse))
        x_amp_delay = (self._to_clock_ticks(self.x_amp_delay))
        x_amp_delay_hex_str = self._int_to_hex_str(x_amp_delay, big_endian=True, hdl=True)
        print('x_amp_delay_reg <= {};\t\t-- {}'.format(x_amp_delay_hex_str, self.x_amp_delay))
        l_amp_delay = (self._to_clock_ticks(self.l_amp_delay))
        l_amp_delay_hex_str = self._int_to_hex_str(l_amp_delay, big_endian=True, hdl=True)
        print('l_amp_delay_reg <= {};\t\t-- {}'.format(l_amp_delay_hex_str, self.l_amp_delay))

        print('-'*100)
        print()
        print()
        print('-- <p. width>, <pri>, <mode>, <freq>')
        print()
        for index, pulse in enumerate(self.pulses):
            print('-- pulse ' + str(index))
            pulse_width = self._to_clock_ticks(pulse['pulse_width'])
            pri = self._to_clock_ticks(pulse['pri'])
            pri_offset = pri - pre_pulse - pulse_width
            print(self._int_to_hex_str(pulse_width, big_endian=True, hdl=True) + ', ' +
                  # TODO: 1x32bit or 2x16bit?
                  self._int_to_hex_str(pri_offset, big_endian=True, hdl=True) + ', ' +
                  self._int_to_hex_str(int(pulse['pol_mode']), big_endian=True, hdl=True) + ', ' +
                  self._int_to_hex_str(int(pulse['frequency']), big_endian=False, hdl=True) + ', ')
        print('\nothers => x\"ffff\"')
        print('-' * 100)

    def get_hex_params(self, hdl_format=False):
        """returns a dictionary of parameters in hex string format"""
        hex_params = dict()
        hex_params['num_pulses'] = self._int_to_hex_str(self.num_pulses, hdl=hdl_format, big_endian=hdl_format, bytes=4)
        hex_params['num_repeats'] = self._int_to_hex_str(self.num_repeats, hdl=hdl_format, big_endian=hdl_format)
        pri_pulse_width = (self._to_clock_ticks(self.pri_pulse_width))
        hex_params['pri_pulse_width'] = self._int_to_hex_str(pri_pulse_width, hdl=hdl_format, big_endian=hdl_format, bytes=4)
        pre_pulse = (self._to_clock_ticks(self.pre_pulse))
        hex_params['pre_pulse'] = self._int_to_hex_str(pre_pulse, hdl=hdl_format, big_endian=hdl_format)
        x_amp_delay = (self._to_clock_ticks(self.x_amp_delay))
        hex_params['x_amp_delay'] = self._int_to_hex_str(x_amp_delay, hdl=hdl_format, big_endian=hdl_format)
        l_amp_delay = (self._to_clock_ticks(self.l_amp_delay))
        hex_params['l_amp_delay'] = self._int_to_hex_str(l_amp_delay, hdl=hdl_format, big_endian=hdl_format)
        hex_params['pulses'] = list()
        for index, pulse in enumerate(self.pulses):
            pulse_width = self._to_clock_ticks(pulse['pulse_width'])
            pri = self._to_clock_ticks(pulse['pri'])
            pri_offset = pri - pre_pulse - pulse_width
            hex_params['pulses'].append({'pulse_width': self._int_to_hex_str(pulse_width, hdl=hdl_format, big_endian=hdl_format),
                                         'pri': self._int_to_hex_str(pri_offset, hdl=hdl_format, big_endian=hdl_format, bytes=4),
                                         'pol_mode': self._int_to_hex_str(int(pulse['pol_mode']), hdl=hdl_format, big_endian=hdl_format),
                                         'frequency': self._int_to_hex_str(int(pulse['frequency']), hdl=hdl_format, big_endian=(not hdl_format))})

        return hex_params

    def _to_clock_ticks(self, x):
        """ converts a time duration into a number of clock ticks """
        # NOTE: assumes inputs are in microseconds
        return(int(x * 1000 // self.clk_period_ns))

    def _int_to_hex_str(self, num, bytes=2, big_endian=False, hdl=False):
        """ returns a hexidecimal string in format given an integer
            endianess:
                default is LITTLE endian
                for big endian, pass 'big_endian = True' as an argument
        """
        if bytes % 2 != 0:
            raise ValueError('i can only do even byte sizes')
        hex_num = hex(num)
        hex_num = hex_num.replace('0x', '')
        num_zeros_to_pad = 0
        if len(hex_num) % (bytes*2) != 0:
            num_zeros_to_pad = (bytes*2) - len(hex_num) % (bytes*2)
        hex_num = '0' * num_zeros_to_pad + hex_num
        num_bytes = len(hex_num) // 2
        byte_list = list()
        index = 0
        for count in range(num_bytes):
            byte_list.append(hex_num[index: index + 2])
            index += 2

        if not big_endian:
            byte_list.reverse()

        hex_str = str()
        if not hdl:
            for byte in byte_list:
                hex_str += '\\x' + byte
        else:
            hex_str += 'x\"'
            for byte in byte_list:
                hex_str += byte
            hex_str += '\"'

        return hex_str


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
