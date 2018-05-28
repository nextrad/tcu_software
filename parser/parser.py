import configparser
import logging


class HeaderFile(object):
    """NeXtRAD.ini File Parser"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = logging.getLogger('header_file_logger')

    def parse(self):
        """parse header file for parameters"""
        raise(NotImplementedError)

    def set_params(self, params):
        raise(NotImplementedError)
