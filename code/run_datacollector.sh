#!/usr/bin/env bash

#Script to run every 15 minutes using crontab

cd /home/nextpi/portomobility/

set -e
source .venv/bin/activate && \
echo "Initiating the script to collect the data" && \
python code/data_collector.py .env && \
echo "Done"
deactivate
