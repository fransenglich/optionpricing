#!/bin/sh

flake8 *.py

python3 Testblackscholes.py
python3 TestBinomialNode.py
python3 Test_mc.py
