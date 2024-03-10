#!/bin/bash
pushd "${0%/*}"
echo 'in file trigger script'
../../venv/Scripts/python.exe ../utility/trigger_file_counter.py
echo 'done'
popd