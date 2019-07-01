#!/bin/bash
set -e
mkdir -p alsvinn_build_folder
cd alsvinn_build_folder
cmake ../alsvinn -DALSVINN_USE_CUDA=OFF -DCMAKE_BUILD_TYPE=Release
make -j
echo "### RUNNING UNIT TESTS"
./test/library_tests/alstest
