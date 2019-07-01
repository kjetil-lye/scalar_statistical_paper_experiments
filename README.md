# scalar_statistical_paper_experiments
Numerical experiments for the paper [U.S. Fjordholm, K. Lye, S. Mishra, Numerical approximation of statistical solutions of scalar conservation laws arXiv:1710.11173 [math.NA]](https://arxiv.org/abs/1710.11173).


## Latex
Note that these plots needs LaTeX installed. On some clusters, LaTeX is installed, but with a non functioning version. You can [download LaTeX from the TeXLive homepage](https://www.tug.org/texlive/acquire-netinstall.html) To install LaTeX to a local directory on such a cluster (eg. CSCS Daint), do 

    export TEXLIVE_INSTALL_PREFIX=$SCRATCH/texlive
    export TEXLIVE_INSTALL_TEXDIR=$SCRATCH/texlive/2019
    
    wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    tar xvf install-tl-unx.tar.gz
    cd install-tl-<version here>
    ./install-tl -gui text
    # Check that everything is OK, then
    # Press i <ENTER>