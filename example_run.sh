#!/bin/bash

PROJECT_NAME=myproject
PROJECT_DIR=example

set -e

#git co example

./licenseadder.py --project $PROJECT_NAME --dir $PROJECT_DIR \
        --license lgpl3  --author "Johan Henriksson johan[a]dexar.se"  \
        --name "example"

