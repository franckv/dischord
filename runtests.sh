#! /bin/bash

export PYTHONPATH=src

find tests -name *_test.py -exec python {} \;
