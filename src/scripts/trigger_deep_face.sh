#!/bin/bash
pushd "${0%/*}"
../../venv/Scripts/python.exe ../utility/deep_face_operations.py $1
popd