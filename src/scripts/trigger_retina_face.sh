#!/bin/bash
pushd "${0%/*}"
../../venv/Scripts/python.exe ../utility/trigger_retina_face.py $1
popd