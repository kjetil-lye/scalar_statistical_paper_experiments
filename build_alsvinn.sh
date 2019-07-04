#!/bin/bash
set -e
mkdir -p alsvinn_build_folder
cd alsvinn_build_folder
cmake ../alsvinn -DALSVINN_USE_CUDA=OFF -DCMAKE_BUILD_TYPE=Release -DALSVINN_PYTHON_VERSION=3.6 -DALSVINN_BUILD_TESTS=OFF -DALSVINN_BUILD_DOXYGEN=OFF
make -j
