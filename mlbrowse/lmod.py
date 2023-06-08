#!/bin/env python
"""Module for parsing and querying LMOD json-database"""

import os
import sys
import subprocess
import json

# Generate modules.json with:
# $LMOD_DIR/spider -o jsonSoftwarePage $MODULEPATH > modules.json

import sys

class LmodDB(object):
    """LmodDB class

    Reads a LMOD json database and stores in Python dictionaries.
     """
    def __init__(self, filename="modules.json"):
        self._filename = filename

        if not os.path.exists(self._filename):
            print(f"Could not load {self._filename}")
            sys.exit(1)

        with open(self._filename, "r") as f:
            self.modules = json.load(f)

        self.module_dict = {}
        self.module_version_dict = {}

        for module in self.modules:
            module_name = module["package"]
            self.module_dict[module_name] = module
            for version in module["versions"]:
                if "versionName" in version:
                    module_version = version["versionName"]

                    if not module_name in self.module_version_dict:
                        self.module_version_dict[module_name] = {}
                    if not module_version in self.module_version_dict[module_name]:
                        self.module_version_dict[module_name][module_version] = []

                    self.module_version_dict[module["package"]][module_version].append(version)


    def find_versions(self, module):
        """Find versions of specific module."""
        versions = []
        for version in self.module_version_dict[module].keys():
            versions.append(version)
        return versions

    def find_module_source(self, module, version):
        """Find module source"""
        if module in self.module_version_dict:
            if version in self.module_version_dict[module]:
                return self.module_version_dict[module][version]["path"]
            
        return ""

    def find_parents(self, module, version):
        """Find module parents (dependencies)"""
        module_parents = []
        if module in self.module_version_dict:
            if version in self.module_version_dict[module]:
                for parents in self.module_version_dict[module][version]:
                    if "parent" in parents:
                        for parent in parents["parent"]:
                            module_parents.append(parent)
                return module_parents
        
        return []

    def find_version_info(self, module):
        """Find version information on specific module."""
        versions = []
        for version in self.module_dict[module]["versions"]:
            versions.append(version)
        return versions

    def find_modules(self, name=""):
        """Find modules in tree. Use @name to filter modules."""
        module_names = []

        for module in self.modules:
            if name=="":
                module_names.append(module["package"])
            else:
                if name in module["package"]:
                    module_names.append(module["package"])
                elif name.upper() in module["package"].upper():
                    module_names.append(module["package"])
                elif name.lower() in module["package"].lower():
                    module_names.append(module["package"])

                #if name == module["package"][0:len(name)]:
                #    module_names.append(module["package"])
                #elif name.upper() == module["package"][0:len(name)]:
                #    module_names.append(module["package"])
                #elif name.lower() == module["package"][0:len(name)]:
                #    module_names.append(module["package"])

        return module_names

    def find_description(self, module):
        """Find module descriptions."""
        try:
            return self.module_dict[module]["description"]
        except:
            return ""

    def find_default_version(self, module):
        """Return default version of specific module"""
        try:
            return self.module_dict[module]["defaultVersionName"]
        except:
            return ""


if __name__ == "__main__":

    lmod = LmodDB()
    versions = lmod.find_versions("GROMACS")
    print(versions)

    module_names = lmod.find_modules()
    print(module_names)

    #lmod = LmodDB()
    #versions = lmod.find_versions("Anaconda3")
    #print(versions)

    #dep_mods = lmod.find_deps("Anaconda3", versions[1])
    #print(dep_mods)

    #default_version = lmod.find_default_version("Anaconda3")
    #print(default_version)
    
    #lmod.parse_deps()
