#!/bin/env python

import os, sys, argparse

from PyQt5 import QtCore, QtGui, QtWidgets

# --- Version information

mlbrowse_copyright = """LUNARC LMOD Browser - Version %s
Copyright (C) 2017-2024 LUNARC, Lund University
This program comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.
This is free software, and you are welcome to redistribute it
under certain conditions; see LICENSE for details.
"""
mlbrowse_copyright_short = """LUNARC LMOD Browser - %s"""
mlbrowse_version = "0.3.1"

# --- Fix search path for tool

tool_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(tool_path)

from mlbrowse import *

if __name__ == '__main__':

    # Show version information


    print((mlbrowse_copyright % mlbrowse_version))
    print("")

    parser = argparse.ArgumentParser(description="LMOD Browser")

    parser.add_argument("--select", dest="select", action="store_true", default=False, help="Selection mode")
    parser.add_argument("--name-only", dest="name_only", action="store_true", default=False, help="Only return names in selection.")
    parser.add_argument("--filter", dest="filter", action="store", default="", help="default filter applied.")

    args = parser.parse_args()

    launchSettings = settings.LaunchSettings.create()
    launchSettings.args = args
    launchSettings.tool_path = tool_path
    launchSettings.copyright_info = mlbrowse_copyright
    launchSettings.copyright_short_info = mlbrowse_copyright_short
    launchSettings.version_info = mlbrowse_version

    # Redirect standard output

    redirect = False

    app = QtWidgets.QApplication(sys.argv)

    # Show user interface
    
    form = lmod_ui.LmodQueryWindow()
    form.show()

    # Start main application loop

    app.exec_()
