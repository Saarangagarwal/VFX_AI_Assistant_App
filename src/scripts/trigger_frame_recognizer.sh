#!/bin/bash
pushd "${0%/*}"
../../venv/Scripts/python.exe ../utility/trigger_frame_recognizer.py
popd