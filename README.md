# scalar_statistical_paper_experiments
Numerical experiments for the paper [U.S. Fjordholm, K. Lye, S. Mishra, Numerical approximation of statistical solutions of scalar conservation laws arXiv:1710.11173 [math.NA]](https://arxiv.org/abs/1710.11173).


## Installing Alsvinn

You can either use the [docker file for Alsvinn](https://hub.docker.com/r/alsvinn/) to run these experiments (use version 0.5.3 or later), or compile the alsvinn version under the folder ```alsvinn``.

### Compiling Alsvinn

First make sure you have checked out the submodule containing alsvinn:

    git submodule update --init

Do something like:

    mkdir alsvinn_build_folder
    cd alsvinn_build_folder
    cmake ../alsvinn -DCMAKE_BUILD_TYPE=Release -DALSVINN_USE_CUDA=OFF \
        -DALSVINN_BUILD_TESTS=OFF -DALSVINN_BUILD_DOXYGEN=OFF
    make

Then go back to the root of this repository, and make sure the pythonpath is set correctly. The pythonpath must contain the ```python``` folder of this repository, and the ```python``` directory of ```alsvinn_build_folder```. To set these, you can simply run

     source source.sh
     source source_alsvinn.sh


## Running the noteboks

First make sure your ```PYTHONPATH``` is correct, so first do something like

    source source.sh
    source source_alsvinn.sh

then

    cd notebooks
    jupyter notebook