#!/bin/env python

import os, configparser

from . singleton import *
from . import settings

def print_error(msg):
    """Print error message"""
    print("Error: %s" % msg)


@Singleton
class MlBrowseConfig(object):
    """LMOD Browser configuration"""
    def __init__(self, config_filename = ""):

        self._default_props()

        tool_path = settings.LaunchSettings.create().tool_path        

        self.config_file_alt1 = "/etc/mlbrowse.conf"
        self.config_file_alt2 = "/sw/pkg/mbrowser/etc/mlbrowse.conf"
        self.config_file_alt3 = os.path.join(tool_path, "../etc/mlbrowse.conf")

        self.config_filename = config_filename

        if config_filename == "":
            if os.path.isfile(self.config_file_alt1):
                self.config_filename = self.config_file_alt1
            elif os.path.isfile(self.config_file_alt2):
                self.config_filename = self.config_file_alt2
            elif os.path.isfile(self.config_file_alt3):
                self.config_filename = self.config_file_alt3
        else:
            self.config_filename = config_filename            

        if not self.parse_config_file():
            print_error("Couldn't parse configuration")
            self.is_ok = False
        else:
            self.is_ok = True



    def _default_props(self):
        """Assign default properties"""
        self.module_json_file = "/sw/pkg/rviz/share/modules.json"

    def print_config(self):
        """Print configuration"""

        print("")
        print("-------------------------------")
        print("Graphics Launcher configuration")
        print("-------------------------------")

        print("")
        print("General settings")
        print("")
        print("modules_json_file = %" % (self.module_json_file))

        
    def _config_get(self, config, section, option):
        """Safe config retrieval"""
        
        if config.has_option(section, option):
            return config.get(section, option)
        else:
            return ""

    def _config_getboolean(self, config, section, option):
        """Safe config retrieval"""

        if config.has_option(section, option):
            return config.getboolean(section, option)
        else:
            return ""

    def parse_config_file(self):
        """Parse configuration file"""

        if not os.path.isfile(self.config_filename):
            print_error("Configuration file %s not found" % self.config_filename)
            return False

        print("Using configuration file : %s" % self.config_filename)

        config = configparser.RawConfigParser()
        config.read(self.config_filename)

        # Check for correct sections

        try:
            self.modules_json_file = self._config_get(config, "general", "modules_json_file")
        except configparser.Error as e:
            print_error(e)
            return False

        return True
