#!/usr/bin/env python

# tcu_project.py
# project to communicate with the RHINO-TCU using the HARPOON framework
# 04/12/2017
# Brad Kahn

# ----------------------------------------------------------------------------
# EXIT CODES:
# 0     : all good, tcu is armed and waiting
# 64    : headerfile not found
# 65    : expected parameter missing from headerfile
# 66    : failed to connect to rhino
# 67    : read registers don't match expected
# user codes: '0', '64 - 113' http://www.tldp.org/LDP/abs/html/exitcodes.html
# ----------------------------------------------------------------------------

import argparse
import sys
import time
import logging
import prettytable

import harpoon
from harpoon.boardsupport import borph
from parser import TCUParams

# SYMBOLS:
# ---------------------
# num_pulses       0x02
# num_repeats      0x04
# x_amp_delay      0x02
# l_amp_delay      0x02
# pri_pulse_width  0x04
# pulses           0x140
# status           0x02
# instruction      0x02
# pre_pulse        0x02

num_pulses = str()
num_repeats = str()
x_amp_delay = str()
l_amp_delay = str()
rex_delay = str()
pri_pulse_width = str()
pulses = list()
status = str()
instruction = str()
pre_pulse = str()

CLK_PERIOD_NS = 10
CLK_FREQUENCY_HZ = 1 / (CLK_PERIOD_NS * pow(10, -9))


logger = logging.getLogger('tcu_project_logger')


def init_logger():
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    time_struct = time.localtime()
    time_str = time.strftime("%H:%M:%S", time_struct)
    date_str = time.strftime("%d-%m-%Y", time_struct)
    fh = logging.FileHandler('tcu_experiment_' + date_str + '_' + time_str + '.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter2 = logging.Formatter('[%(levelname)s] %(message)s')
    ch.setFormatter(formatter2)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logging.getLogger().addHandler(fh)
    logging.getLogger().addHandler(ch)


def parse_header():

    tcu_params = TCUParams(HEADER_FILE)
    logger.debug('Extracted parameters from header:\n' + str(tcu_params))

    global num_pulses
    global num_repeats
    global x_amp_delay
    global l_amp_delay
    global rex_delay
    global pri_pulse_width
    global pulses
    global status
    global instruction
    global pre_pulse

    hex_params = tcu_params.get_hex_params()
    num_pulses = hex_params['num_pulses']
    num_repeats = hex_params['num_repeats']
    # ensuring num_repeats is 32bit hex number
    if len(num_repeats) == 8:
        # NOTE: change this depending on how num_repeats is stored in HDL
        # num_repeats = '\\x00\\x00' + num_repeats
        num_repeats = num_repeats + '\\x00\\x00'
    x_amp_delay = hex_params['x_amp_delay']
    l_amp_delay = hex_params['l_amp_delay']
    rex_delay = hex_params['rex_delay']
    pri_pulse_width = hex_params['pri_pulse_width']
    # ensuring pri_pulse_width is 32bit hex number
    if len(pri_pulse_width) == 8:
        # NOTE: change this depending on how pri_pulse_width is stored in HDL
        # pri_pulse_width = '\\x00\\x00' + pri_pulse_width
        pri_pulse_width = pri_pulse_width + '\\x00\\x00'
    pulses = hex_params['pulses']
    pre_pulse = hex_params['pre_pulse']

    for index, pulse in enumerate(pulses):
        # ensuring PRI is 32bit hex number
        if len(pulse['pri']) == 8:
            # NOTE: change this depending on how PRI is stored in HDL
            # pulse['pri'] = '\\x00\\x00' + pulse['pri']
            pulse['pri'] = pulse['pri'] + '\\x00\\x00'

    logging.info('header parsing complete')


def connect():
    logger.debug('initializing rhino connection, IP address: ' + TCU_ADDRESS)
    global fpga_con
    fpga_con = borph.RHINO(address=TCU_ADDRESS,
                           username='root',
                           password='rhino',
                           login_timeout=30)
    logger.debug('attempting to connect...')
    try:
        fpga_con.connect()
    except Exception as e:
        logger.error('failed to connect to rhino')
        sys.exit(66)

    logger.debug('connection successful!')


def launch_bof():
    # TODO: this assumes that there is no other .bof running on the RHINO
    #       scan for any .bof running on
    if fpga_con._pid == '':
        # check for any prexisting running .bof
        logger.debug('checking for any prexisting running .bof executables')
        existing_bof_proc = fpga_con._action("ps -o pid,args | grep [.]bof | while read c1 c2; do echo $c1; done")
        existing_bof_proc = (existing_bof_proc.decode('utf8').split("\r\n"))[1]

        if existing_bof_proc != '':
            logger.warning('existing .bof was found running on the RHINO...')
            logger.warning('assuming it is a the same TCU project...')
            fpga_con._pid = existing_bof_proc
        else:
            logger.debug('no existing running .bof found, launching TCU.bof')
            fpga_con.program(BOF_EXE)


def kill_bof():
    logger.debug('checking for any prexisting running .bof executables')
    existing_bof_proc = fpga_con._action("ps -o pid,args | grep [.]bof | while read c1 c2; do echo $c1; done")
    existing_bof_proc = (existing_bof_proc.decode('utf8').split("\r\n"))[1]

    if existing_bof_proc != '':
        logger.debug('kill {}'.format(existing_bof_proc))
        fpga_con._action('kill {}'.format(existing_bof_proc))
    else:
        logger.debug('no existing running .bof found, nothing to kill')


def write_registers():
    # TODO: implement framework functionality:
    #       core_tcu.write_reg('pulses', pulses)
    #       core_tcu.write_reg('m', num_repeats)
    #       core_tcu.write_reg('n', num_pulses)

    pulse_param_str = str()
    for pulse in pulses:
        pulse_param_str += pulse['pulse_width'] + pulse['pri'] + pulse['pol_mode'] + pulse['frequency']

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pulse_param_str, fpga_con._pid, 'pulses'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pulse_param_str, fpga_con._pid, 'pulses'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(num_repeats, fpga_con._pid, 'num_repeats'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(num_repeats, fpga_con._pid, 'num_repeats'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(num_pulses, fpga_con._pid, 'num_pulses'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(num_pulses, fpga_con._pid, 'num_pulses'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(x_amp_delay, fpga_con._pid, 'x_amp_delay'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(x_amp_delay, fpga_con._pid, 'x_amp_delay'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(l_amp_delay, fpga_con._pid, 'l_amp_delay'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(l_amp_delay, fpga_con._pid, 'l_amp_delay'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(rex_delay, fpga_con._pid, 'rex_delay'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(rex_delay, fpga_con._pid, 'rex_delay'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pri_pulse_width, fpga_con._pid, 'pri_pulse_width'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pri_pulse_width, fpga_con._pid, 'pri_pulse_width'))

    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pre_pulse, fpga_con._pid, 'pre_pulse'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format(pre_pulse, fpga_con._pid, 'pre_pulse'))


def verify_registers():

    # -------------------------------------------------------------------------
    # verifying global parameters
    # -------------------------------------------------------------------------
    logger.debug('reading num_pulses...')
    reg_num_pulses_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'num_pulses'))
    logger.debug('num_pulses:' + reg_num_pulses_rcv.decode('utf-8'))
    reg_num_pulses_rcv = "'"+reg_num_pulses_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_num_pulses_rcv.replace("'", "").split(" ")
    reg_num_pulses_rcv = ("0x" + arr[1] + arr[0])

    logger.debug('reading num_repeats...')
    reg_num_repeats_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'num_repeats'))
    logger.debug('num_repeats:' + reg_num_repeats_rcv.decode('utf-8'))
    reg_num_repeats_rcv = "'"+reg_num_repeats_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_num_repeats_rcv.replace("'", "").split(" ")
    reg_num_repeats_rcv = ("0x" + arr[2] + arr[1])

    logger.debug('reading x_amp_delay...')
    reg_x_amp_delay_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'x_amp_delay'))
    logger.debug('x_amp_delay:' + reg_x_amp_delay_rcv.decode('utf-8'))
    reg_x_amp_delay_rcv = "'"+reg_x_amp_delay_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_x_amp_delay_rcv.replace("'", "").split(" ")
    reg_x_amp_delay_rcv = ("0x" + arr[1] + arr[0])

    logger.debug('reading l_amp_delay...')
    reg_l_amp_delay_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'l_amp_delay'))
    logger.debug('l_amp_delay:' + reg_l_amp_delay_rcv.decode('utf-8'))
    reg_l_amp_delay_rcv = "'"+reg_l_amp_delay_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_l_amp_delay_rcv.replace("'", "").split(" ")
    reg_l_amp_delay_rcv = ("0x" + arr[1] + arr[0])

    logger.debug('reading rex_delay...')
    reg_rex_delay_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'rex_delay'))
    logger.debug('rex_delay:' + reg_rex_delay_rcv.decode('utf-8'))
    reg_rex_delay_rcv = "'"+reg_rex_delay_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_rex_delay_rcv.replace("'", "").split(" ")
    reg_rex_delay_rcv = ("0x" + arr[1] + arr[0])

    logger.debug('reading pri_pulse_width...')
    reg_pri_pulse_width_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'pri_pulse_width'))
    logger.debug('pri_pulse_width:' + reg_pri_pulse_width_rcv.decode('utf-8'))
    reg_pri_pulse_width_rcv = "'"+reg_pri_pulse_width_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_pri_pulse_width_rcv.replace("'", "").split(" ")
    reg_pri_pulse_width_rcv = ("0x" + arr[2] + arr[1])

    logger.debug('reading pre_pulse...')
    reg_pre_pulse_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'pre_pulse'))
    logger.debug('pre_pulse:' + reg_pre_pulse_rcv.decode('utf-8'))
    reg_pre_pulse_rcv = "'"+reg_pre_pulse_rcv.decode('utf-8').split("\r\n")[1:-1:][0]+"'"
    arr = reg_pre_pulse_rcv.replace("'", "").split(" ")
    reg_pre_pulse_rcv = ("0x" + arr[1] + arr[0])

    ptable_global = prettytable.PrettyTable()
    ptable_global.field_names = ['Parameter', 'Value', 'Hex Cycles [big endian]']
    ptable_global.align['Parameter'] = 'l'
    ptable_global.add_row(['num_pulses', eval(reg_num_pulses_rcv), reg_num_pulses_rcv])

    ptable_global.add_row(['num_repeats', eval(reg_num_repeats_rcv), reg_num_repeats_rcv])

    ptable_global.add_row(
        ['pri_pulse_width', eval(reg_pri_pulse_width_rcv), reg_pri_pulse_width_rcv])
    ptable_global.add_row(['pre_pulse', eval(reg_pre_pulse_rcv), reg_pre_pulse_rcv])
    ptable_global.add_row(
        ['x_amp_delay', eval(reg_x_amp_delay_rcv), reg_x_amp_delay_rcv])
    ptable_global.add_row(
        ['l_amp_delay', eval(reg_l_amp_delay_rcv), reg_l_amp_delay_rcv])
    ptable_global.add_row(
        ['rex_delay', eval(reg_rex_delay_rcv), reg_rex_delay_rcv])
    logger.debug("Global Registers:")
    logger.debug("\n"+str(ptable_global))

    # -------------------------------------------------------------------------
    # verifying pulse parameters
    # -------------------------------------------------------------------------
    logger.debug('reading pulses...')
    reg_pulses_rcv = fpga_con._action('od -x -An /proc/{}/hw/ioreg/{}'.format(fpga_con._pid, 'pulses'))
    logger.debug('pulses:' + reg_pulses_rcv.decode('utf-8'))

    array = reg_pulses_rcv.decode('utf-8').split("\r\n")
    array = array[1:-2:]  # extract only the data
    for i in range(len(array)):
        array[i] = array[i].lstrip()

    # "splitting up pulses info into 16bit chunks...:")
    read_data_array = list()
    for i in range(len(array)):
        line_in_array = array[i].split(" ")
        for word in line_in_array:
            read_data_array.append(word)

    ptable_pulses = prettytable.PrettyTable()
    ptable_pulses.field_names = ['Pulse Number', 'Pulse Width', 'PRIoffset',
                                 'Mode', 'Frequency', "PRF[Hz]"]

    for pulse_number in range(eval(reg_num_pulses_rcv)):

        pulse_width = read_data_array[((pulse_number*5)+0)]
        pulse_width = eval("0x"+pulse_width)*CLK_PERIOD_NS

        pri_lower = read_data_array[((pulse_number*5)+1)]
        pri_upper = read_data_array[((pulse_number*5)+2)]
        pri_offset = eval("0x"+pri_upper+pri_lower)*CLK_PERIOD_NS

        mode = read_data_array[((pulse_number*5)+3)]
        mode = eval("0x"+mode)

        freq = read_data_array[((pulse_number*5)+4)]
        freq = freq[2:4] + freq[0:2]
        freq = eval("0x"+freq)

        pre_pulse = eval(reg_pre_pulse_rcv)*CLK_PERIOD_NS
        pri_calc = (pulse_width + pre_pulse + pri_offset) / 1000000000  # PRI in seconds
        prf_calc = 1 / pri_calc  # PRF in Hertz
        ptable_pulses.add_row([str(pulse_number), str(pulse_width),
                               str(pri_offset), str(mode), str(freq),
                               str(prf_calc)])
    logger.debug("Pulses Register")
    logger.debug("\n"+str(ptable_pulses))
    # TODO: check if registers don't match
    #       sys.exit(67)


def arm_tcu():
    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format('\\x00\\x00', fpga_con._pid, 'instruction'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format('\\x00\\x00', fpga_con._pid, 'instruction'))
    time.sleep(3)
    logger.debug('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format('\\x01\\x00', fpga_con._pid, 'instruction'))
    fpga_con._action('echo -en \'{}\' | cat > /proc/{}/hw/ioreg/{}'.format('\\x01\\x00', fpga_con._pid, 'instruction'))
    logger.debug('TCU armed')


def power_fmc():
    logger.debug('calling power_fmc.sh script...')
    fpga_con._action('./power_fmc.sh')

# TODO: incorporate this:
# -----------------------------------------------------------------------------
# CORE INSTANTIATION
# -----------------------------------------------------------------------------
# core_tcu = harpoon.IPCore('tcu_core', 'Timing control unit')

# -----------------------------------------------------------------------------
# REGISTERS FOR CORE_TCU INSTANTIATION
# -----------------------------------------------------------------------------
# harpoon.Register('version', 'version number of this iteration of tcu gateware',
#                  2, 1, core_tcu)
# harpoon.Register('status',
#                  'status flags:\n'
#                  'bit 0: pulse repeats for experiment completed\n'
#                  'bit 3: digitisation flag\n'
#                  'bit 4: pri flag, bit 5: pulse completed\n'
#                  'bit 6: \'1\'\n'
#                  'bit 7: gpioIN(1) trigger from GPSDO',
#                  2, 1, core_tcu)
# harpoon.Register('control', 'reg-description',
#                  2, 3, core_tcu)
# harpoon.Register('fmc', 'reg-description',
#                  4, 3, core_tcu)
# harpoon.Register('pulses', 'reg-description',
#                  180, 3, core_tcu)
# harpoon.Register('m', 'Number of repeats for each pulse in an experiment',
#                  4, 3, core_tcu)
# harpoon.Register('n', 'Number of pulses',
#                  2, 3, core_tcu)

# -----------------------------------------------------------------------------
# Project instantiation
# -----------------------------------------------------------------------------
# project = harpoon.Project('tcu_project',
#                           'project to communicate with the RHINO-TCU',
#                           [core_tcu])


if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # PARSE COMMAND LINE ARGUMENTS
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(usage='tcu_project [address]',
                                     description='Startup script for the '
                                                 'NeXtRAD Timing Control Unit')
    parser.add_argument('address', help='IP address of TCU')
    parser.add_argument('-f', '--file', help='header file to load parameters '
                        '[./NeXTRAD.ini]', default='./NeXTRAD.ini')
    parser.add_argument('-b', '--bof', help='name of .bof file to be executed '
                        'on RHINO [\'tcu_v2-1.bof\']', default='tcu_v2-1.bof')
    parser.add_argument('-t', '--timeout', help='login timeout (seconds) to '
                        'establish SSH connection to RHINO [30]',
                        type=int, default=30)
    parser.add_argument('-l', '--logdir', help='directory to store log file '
                        '[\'/tmp\']', default='/tmp')
    parser.add_argument('-k', '--kill', help='kill running .bof',
                        action="store_true", default=False)
    args = parser.parse_args()

    init_logger()

    logger.debug(harpoon.LOGO)
    logger.debug("command line args: {}".format(args))

    HEADER_FILE = args.file
    TCU_ADDRESS = args.address
    BOF_EXE = args.bof  # NOTE: assumes .bof must already be in /opt/rhinofs/
    if args.kill:
        # -------------------------------------------------------------------------
        # CONNECT TO RHINO
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('CONNECTING TO TCU...')
        logger.debug('........................')
        connect()

        logger.debug('........................')
        logger.debug('KILLING .BOF ...')
        logger.debug('........................')
        kill_bof()

    else:
        logger.info('initializing TCU at IP [{}] with header file at [{}], '
                    'this should take a moment...'
                    .format(TCU_ADDRESS, HEADER_FILE))

        # -------------------------------------------------------------------------
        # EXTRACT PARAMETERS FROM HEADER FILE
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('PARSING HEADERFILE...')
        logger.debug('........................')
        parse_header()

        # -------------------------------------------------------------------------
        # CONNECT TO RHINO
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('CONNECTING TO TCU...')
        logger.debug('........................')
        connect()

        # -------------------------------------------------------------------------
        # CONNECT TO RHINO
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('POWERING FMC0...')
        logger.debug('........................')
        power_fmc()

        # -------------------------------------------------------------------------
        # CONFIGURE RHINO WITH TCU PROJECT
        # -------------------------------------------------------------------------
        logger.debug('launching TCU .bof...')
        launch_bof()

        # -------------------------------------------------------------------------
        # SEND PARAMETERS TO TCU
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('SENDING PARAMS TO TCU...')
        logger.debug('........................')
        write_registers()

        # -------------------------------------------------------------------------
        # VERIFY REGISTERS HAVE CORRECT VALUES
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('VERYFYING TCU REGISTERS...')
        logger.debug('........................')
        verify_registers()

        # -------------------------------------------------------------------------
        # ARM THE TCU
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('ARMING TCU...')
        logger.debug('........................')
        arm_tcu()

        # -------------------------------------------------------------------------
        # CLOSE SSH CONNECTION
        # -------------------------------------------------------------------------
        logger.debug('........................')
        logger.debug('CLOSING SSH CONNECTION...')
        logger.debug('........................')
        fpga_con.disconnect()

    logger.info('script completed successfully')
    sys.exit(0)
