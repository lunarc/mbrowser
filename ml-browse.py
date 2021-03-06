#!/bin/env python

import os, sys, argparse

from PyQt5 import QtCore, QtGui, QtWidgets

# --- Version information

mlbrowse_copyright = """LUNARC LMOD Browser - Version %s
Copyright (C) 2017-2020 LUNARC, Lund University
This program comes with ABSOLUTELY NO WARRANTY; for details see LICENSE.
This is free software, and you are welcome to redistribute it
under certain conditions; see LICENSE for details.
"""
mlbrowse_copyright_short = """LUNARC LMOD Browser - %s"""
mlbrowse_version = "0.2"

# --- Fix search path for tool

tool_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(tool_path)

from mlbrowse import *

def create_dark_palette():
    """Create a dark palette"""
    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    darkPalette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,QtGui.QColor(127,127,127));
    darkPalette.setColor(QtGui.QPalette.Base,QtGui.QColor(42,42,42));
    darkPalette.setColor(QtGui.QPalette.AlternateBase,QtGui.QColor(66,66,66));
    darkPalette.setColor(QtGui.QPalette.ToolTipBase,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.ToolTipText,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.Text,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Text,QtGui.QColor(127,127,127));
    darkPalette.setColor(QtGui.QPalette.Dark,QtGui.QColor(35,35,35));
    darkPalette.setColor(QtGui.QPalette.Shadow,QtGui.QColor(20,20,20));
    darkPalette.setColor(QtGui.QPalette.Button,QtGui.QColor(53,53,53));
    darkPalette.setColor(QtGui.QPalette.ButtonText,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ButtonText,QtGui.QColor(127,127,127));
    darkPalette.setColor(QtGui.QPalette.BrightText,QtCore.Qt.red);
    darkPalette.setColor(QtGui.QPalette.Link,QtGui.QColor(42,130,218));
    darkPalette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(42,130,218));
    darkPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,QtGui.QColor(80,80,80));
    darkPalette.setColor(QtGui.QPalette.HighlightedText,QtCore.Qt.white);
    darkPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.HighlightedText,QtGui.QColor(127,127,127));

    return darkPalette

def create_light_palette():
    """Create light palette"""
    
    lightPalette = QtGui.QPalette()

    lightPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(212,212,212))
    lightPalette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.black);
    lightPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,QtGui.QColor(172,172,172));
    lightPalette.setColor(QtGui.QPalette.Base,QtGui.QColor(255,255,230));
    lightPalette.setColor(QtGui.QPalette.AlternateBase,QtGui.QColor(0,255,0));
    lightPalette.setColor(QtGui.QPalette.ToolTipBase,QtCore.Qt.black);
    lightPalette.setColor(QtGui.QPalette.ToolTipText,QtCore.Qt.black);
    lightPalette.setColor(QtGui.QPalette.Text,QtCore.Qt.black);
    lightPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Text,QtGui.QColor(128,128,128));
    lightPalette.setColor(QtGui.QPalette.Dark,QtGui.QColor(160,160,160));
    lightPalette.setColor(QtGui.QPalette.Shadow,QtGui.QColor(100,100,100));
    lightPalette.setColor(QtGui.QPalette.Button,QtGui.QColor(212,212,212));
    lightPalette.setColor(QtGui.QPalette.ButtonText,QtCore.Qt.black);
    lightPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ButtonText,QtGui.QColor(172,172,172));
    lightPalette.setColor(QtGui.QPalette.BrightText,QtCore.Qt.red);
    lightPalette.setColor(QtGui.QPalette.Link,QtGui.QColor(42,130,218));
    lightPalette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(42,130,218));
    lightPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,QtGui.QColor(80,80,80));
    lightPalette.setColor(QtGui.QPalette.HighlightedText,QtCore.Qt.white);
    lightPalette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.HighlightedText,QtGui.QColor(127,127,127));

    return lightPalette

if __name__ == '__main__':

    # Show version information


    print((mlbrowse_copyright % mlbrowse_version))
    print("")

    parser = argparse.ArgumentParser(description="LMOD Browser")

    parser.add_argument("--select", dest="select", action="store_true", default=False,
                        help="Selection mode")

    args = parser.parse_args()

    launchSettings = settings.LaunchSettings.create()
    launchSettings.args = args
    launchSettings.tool_path = tool_path
    launchSettings.copyright_info = mlbrowse_copyright
    launchSettings.copyright_short_info = mlbrowse_copyright_short
    launchSettings.version_info = mlbrowse_version

    # User interface 

    dark_mode = False

    # Redirect standard output

    redirect = False

    app = QtWidgets.QApplication(sys.argv)

    if dark_mode:
        palette = create_dark_palette()
    else:
        palette = create_light_palette()
    
    app.setPalette(palette)

    #app.setStyle("gtk2")

    # Show user interface
    
    form = lmod_ui.LmodQueryWindow()
    form.show()

    # Start main application loop

    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    app.exec_()
