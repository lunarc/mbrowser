#!/bin/env python
"""LMOD Browser main user interface"""

import os, sys

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic

from . import lmod
from . import settings
from . import config

from subprocess import Popen, PIPE, STDOUT

def execute_with_output(command):
    """Execute a command and return output"""
    process = Popen(command, shell=True, stdout=PIPE)
    output, error = process.communicate()
    return output

class LmodQueryWindow(QtWidgets.QWidget):
    """Resource specification window"""

    def __init__(self, parent=None):
        """Resource window constructor"""

        super(LmodQueryWindow, self).__init__(parent, QtCore.Qt.Window)

        self.tool_path = settings.LaunchSettings.create().tool_path
        ui_path = os.path.join(self.tool_path, "ui")
        etc_path = os.path.join(self.tool_path, "etc")

        uic.loadUi(os.path.join(ui_path, "lmod_query.ui"), self)
        #uic.loadUi(os.path.join("../ui", "lmod_query.ui"), self)
        
        self.config = config.MlBrowseConfig.create()

        self.parent = parent

        self.lmod = lmod.LmodDB(self.config.modules_json_file)

        self.current_module = ""
        self.current_version = ""

        self.prefer_gcc = False
        self.prefer_ifort = False
        self.prefer_icc = False
        self.prefer_cuda = False

        if settings.LaunchSettings.create().args.select:
            self.start_term_button.setVisible(False)
            self.copy_cmds_button.setVisible(False)

        self.module_stats_label.setText("%d total modules and %d versions." % (self.lmod.module_count, self.lmod.module_version_count))

        self.on_search_edit_textChanged("")
        

    @QtCore.pyqtSlot(str)
    def on_search_edit_textChanged(self, search_string):
        """Updates module list based on search criteria"""
        
        self.module_list.clear()
        self.version_list.clear()
        self.alt_list.clear()
        self.parent_list.clear()

        self.current_module = ""
        self.current_version = ""

        sorted_modules = self.lmod.find_modules(search_string)
        sorted_modules.sort()

        for module in sorted_modules:
            if module[0] != ".":
                self.module_list.addItem(module)

    @QtCore.pyqtSlot()
    def on_prefer_none_check_clicked(self):
        """None radio button checked."""
        self.prefer_gcc = False
        self.prefer_icc = False
        self.prefer_ifort = False

    @QtCore.pyqtSlot()
    def on_prefer_gcc_check_clicked(self):
        """GCC radio button checked."""
        self.prefer_gcc = True
        self.prefer_icc = False
        self.prefer_ifort = False

    @QtCore.pyqtSlot()
    def on_prefer_ifort_check_clicked(self):
        """Intel Fortran radio button checked."""
        self.prefer_gcc = False
        self.prefer_icc = False
        self.prefer_ifort = True

    @QtCore.pyqtSlot()
    def on_prefer_icc_check_clicked(self):
        """Intel C radio button checked."""
        self.prefer_gcc = False
        self.prefer_icc = True
        self.prefer_ifort = False

    @QtCore.pyqtSlot(int)
    def on_prefer_cuda_check_stateChanged(self, state):
        """CUDA Check box checked."""
        self.prefer_cuda = self.prefer_cuda_check.isChecked()

    @QtCore.pyqtSlot(int)
    def on_module_list_currentRowChanged(self, idx):
        """Module selected in module list"""

        default_version_idx = -1

        if idx>=0:

            self.alt_list.clear()
            self.parent_list.clear()

            self.current_module = self.module_list.item(idx).text()
            self.version_list.clear()

            self.versions = self.lmod.find_versions(self.current_module)
            self.version_info = self.lmod.find_version_info(self.current_module)
            self.description = self.lmod.find_description(self.current_module)
            self.default_version = self.lmod.find_default_version(self.current_module)

            self.module_help_text.clear()
            self.module_help_text.insertPlainText(self.description.replace("\n", ""))

            #default_version = self.lmod.module_tree[self.current_module]["default_version"]

            self.version_list.clear()

            curr_row = 0

            for version in self.versions:
                if version == self.default_version:
                    self.version_list.addItem(version)
                    self.version_list.item(self.version_list.count()-1).setForeground(QtCore.Qt.red)
                    default_version_idx = curr_row
                else:
                    self.version_list.addItem(version)

                curr_row += 1

            if default_version_idx != -1:
                self.version_list.setCurrentRow(default_version_idx)


    @QtCore.pyqtSlot(int)
    def on_version_list_currentRowChanged(self, idx):
        """Version selected in version list"""

        self.alt_list.clear()
        self.parent_list.clear()
        self.module_cmds_text.clear()
        
        if idx>=0:

            self.current_version = self.version_list.item(idx).text()

            self.current_alternatives = self.lmod.find_parents(self.current_module, self.current_version)

            self.alt_list.clear()
            if len(self.current_alternatives)>0:
                for i in range(len(self.current_alternatives)):
                    short_form = ""
                    for parent in self.current_alternatives[i]:
                        short_form += parent.split("/")[0] + "/"

                    short_form = short_form[:-1]
                    self.alt_list.addItem("%s" % (short_form))

                if len(self.current_alternatives)==1:
                    self.alt_list.setCurrentRow(0)
                else:
                    if self.alt_list.count()<4:
                        for i in range(self.alt_list.count()):
                            if self.prefer_cuda:
                                if self.alt_list.item(i).text().lower().find("cuda")!=-1:
                                    self.alt_list.setCurrentRow(i)
                                    break
                            if self.prefer_gcc:
                                if self.alt_list.item(i).text().lower().find("gcc")!=-1:
                                    self.alt_list.setCurrentRow(i)
                                    break
                            if self.prefer_ifort:
                                if self.alt_list.item(i).text().lower().find("ifort")!=-1:
                                    self.alt_list.setCurrentRow(i)
                                    break
                            if self.prefer_icc:
                                if self.alt_list.item(i).text().lower().find("icc")!=-1:
                                    self.alt_list.setCurrentRow(i)
                                    break
            else:
                self.module_cmds_text.insertPlainText("module load %s/%s" % (self.current_module, self.current_version))



    @QtCore.pyqtSlot(int)
    def on_alt_list_currentRowChanged(self, idx):
        """Variant selected in variants list."""

        if idx>=0:

            self.current_alternative = self.current_alternatives[idx]

            self.parent_list.clear()
            self.module_cmds_text.clear()

            for parent in self.current_alternatives[idx]:
                self.parent_list.addItem(parent)
                self.module_cmds_text.insertPlainText("module load %s\n" % parent)

            self.module_cmds_text.insertPlainText("module load %s/%s\n" % (self.current_module, self.current_version))

    @QtCore.pyqtSlot()
    def on_start_term_button_clicked(self):
        """Start a terminal with selected modules"""

        cmds = str(self.module_cmds_text.toPlainText())
        cmd_list = cmds.split("\n")

        if len(cmd_list)>1:
            cmd_list.insert(0, "ml purge")
            cmd_row = ";".join(cmd_list)
            print("%smate-terminal" % (cmd_row))
            execute_with_output("%smate-terminal" % (cmd_row))
        else:
            execute_with_output("ml purge;%s;mate-terminal" % (cmds.strip()))

    @QtCore.pyqtSlot()
    def on_copy_cmds_button_clicked(self):
        """Copy selected modules to clipboard"""
        self.module_cmds_text.selectAll()
        self.module_cmds_text.copy()

    @QtCore.pyqtSlot()
    def on_select_modules_button_clicked(self):
        """Copy selected modules to clipboard"""

        print('#MODSTART#')
        print(self.module_cmds_text.toPlainText())
        
        self.close()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # Show user interface
    
    form = LmodQueryWindow()
    form.show()

    # Start main application loop

    app.exec_()
