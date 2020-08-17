# ml-browse - LMOD Graphical module browser

This tool parses the json module tree and presents the user with an browsable view of available modules in LMOD. This is especially useful when the hiearchical modules option is used with LMOD.

# Installation

## Setup a suitable Python environment

Preferable a Anaconda environment is setup with the required packages. A environment.yml file is located in the conda directory. A conda environment can be created by:

    conda env create -f conda/environment.yml

## Unpack in suitable location. 

The package contains a shell-script, ml-browse, that sets up the environment for running the ml-browse application. The script is shown below:

    #!/bin/sh 

    MBROWSE_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

    export PYTHONPATH=$MBROWSE_DIR/../qtui
    export PATH=$MBROWSE_DIR/../qtui/bin:$PATH
    export FONTCONFIG_FILE=/etc/fonts/fonts.conf
    export FONTCONFIG_PATH=/etc/fonts/
    python $MBROWSE_DIR/ml-browse.py "$@"

The PYTHONPATH and PATH variabels may have to be updated. In this the application is setup in the following module structure:

    .../pkg/mbrowser/bin -- Here is the python package located.
    .../pkg/mbrowser/qtui -- Conda environment for running ml-browse.

# Configuration

ml-browse can read configuration files from 

1. Installation path
2. /etc/mbrowser.conf

The configuration file points to where the JSON file that has been generated from the LMOD module database can be located. Below is an example configuration file:

    [general]
    modules_json_file = /sw/pkg/rviz/share/modules.json

# Generating a modules.json file

The generation of the modules.json file is preferable done as a cron-job. Below is an example of a cron-job script:

    LMOD_DIR=/sw/lmod/lmod/libexec
    MODULEPATH=/sw/Modules/modulefiles/Core:/sw/easybuild/modules/all/Core:/sw/lpkg/Linux:/sw/lpkg/Core:/sw/lmod/lmod/modulefiles/Core
    MODULES_JSON_DIR=/sw/pkg/rviz/share
    $LMOD_DIR/spider -o jsonSoftwarePage $MODULEPATH > $MODULES_JSON_DIR/modules.json

The LMOD_DIR, MODULEPATH and MODULES_JSON_DIR must be updated for your own installation.
