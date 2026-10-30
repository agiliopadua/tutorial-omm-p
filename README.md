# Simulation of an ionic liquid using a polarizable force field

## Objectives

The following example uses molecular dynamics (MD) simulations to study an ionic liquid, ethylmethylimidazolium bis(trifluoromethanesulfonyl)imide, denoted [EMIM][TFSI] or [C<sub>2</sub>C<sub>1</sub>im][Ntf<sub>2</sub>].

The objective is to compare traditional molecular interaction force fields, which have fixed electrostatic charges, with more advanced force fields that include explicit polarization effects.

The MD code for the present examples is [OpenMM](https://openmm.org), a modern code that runs very efficiently on GPUs and is accessed through its Python API.


## Context

Ionic liquids are entirely composed of large organic ions. Their asymmetric shspe, molecular flexilibity and charge delocalization render crystallization difficult, therefore these compounds have melting points below room temperature. They are molten salts, with negligible volatility, high thermal and electrochemical stability. They are studied as alternative solvents for reactions or separations, or as electrolytes for energy-storage devices.

Ionic liquids are more viscous than water or common organic solvents, therefore MD trajectories need to be longer and it is also interesting to run then above room  temperature (353 K for example).


## Working environment and codes

The study cases below make use of Python libraries and simulation codes installed on the machines of the Centre Blaise Pascal, CBP.

### Python environment

A **conda** installation with the simulation codes and tools is installed in `/projects/DepartementChimie/miniforge3`. To activate source the contents of the `conda.rc` file (or append it to you `.bashrc` and relaunch a shell):

        source /projects/DepartementChimie/conda.rc

Activate the conda environment containing OpenMM:

        conda activate openmm

### Paths to codes and tools on the CBP

* **OpenMM, mdtraj**: available in the `openmm` conda environment

* **fftool**: `/projects/DepartementChimie/fftool`
* **pol_openmm**: `/projects/DepartementChimie/pol_openmm`

You can add these lines to your `.bashrc`:

    DEPT=/projects/DepartementChimie
    export PATH=$DEPT/fftool:$DEPT/pol_openmm:$PATH

* packmol: /usr/bin/packmol (in the default PATH)
* VMD: /usr/local/bin/vmd (in the default PATH)

Check the accessibility of executables and the path with:

        which packmol
        which fftool
        echo $PATH

### Checking GPU hardware

To check your machine's GPU configuration and monitor its usage:

        nvidia-smi

If your machine is not equiped with a NVIDIA GPU (RTX 2080, 4090, etc.) then you'll need to `ssh` to one that has. It is best if the GPU is not being used by someone else.

You can select and see the state of the CBP machines on the [Cloud@CBP](https://www.cbp.ens-lyon.fr/python/forms/CloudCBP) web page.


## Contents

* `emim_tfsi`: folder with molecule input files and force field parameters for the ionic liquid [EMIM][TFSI]
* `fixq`: simulations with fixed-charge force field
* `pol`: simulations with polarizable force field
* `utils`: utilities
* `refs`: literature references

