#!/bin/sh
echo "python3 ./src/main_ski.py ./test/test.ski"
python3 ./src/main_ski.py ./test/test.ski
echo "python3 ./src/main_ski.py ./problem.ski"
python3 ./src/main_ski.py ./problem.ski
echo "python3 test/test_numpy.py"
python3 test/test_numpy.py
