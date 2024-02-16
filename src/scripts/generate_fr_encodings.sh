#!/bin/bash
pushd "${0%/*}"
echo 'in bnash script'
../../venv/Scripts/python.exe ../utility/generate_fr_encodings.py
echo 'done'
popd