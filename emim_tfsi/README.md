# Simulation of EMIM TFSI

## Objectives

Build a simulation boxes with 300 ion pairs of EMIM TFSI, one with a fixed-charge force field and one with a polarizable force field.

Then run molecular dynamics trajectories and compare structural and transport properties obtained with the two models. 


## Contents

* `c2c1im.zmat`: `fftool` input file for the EMIM cation (z-matrix file)
* `ntf2.zmat`: `fftool` input file for the TFSI cation (z-matrix file)
* `il.ff`: force field parameters for ionic liquids (the CL&P model)
* `alpha.ff`: polarizability parameters for Drude induce dipoles (the CL&Pol model)
* `fragment.ff`: molecular fragments for LJ scaling of the CL&Pol polarizable force field


## Tools and codes

The **fftool** and **packmol** utilities build initial configuration and force field files for used with OpenMM.  **VMD** allows visualization of configurations and trajectories.


## System setup: fixed-charge force field

Build a system with 300 ion pairs of EMIM TFSI, with an initial density of 4 mol L<sup>-1</sup>:

        fftool 300 c2c1im.zmat 300 ntf2.zmat --rho 4.0

Verify that the number of covalent bonds is correct and the total charge is zero.

This step produces an input file `pack.inp` for the Packmol utility. Use it to pack the molecules in an initial configuration:

        packmol < pack.inp

If this step takes too long, the initial density may be too high. Reduce a bit and retry.

Visualize the box created:

        vmd simbox.xyz

Check that the packing is not too dense. Then run fftool again to read the coordinates from `simbox.xyz` and generate input files for OpenMM:

        fftool 300 c2c1im.zmat 300 ntf2.zmat --rho 4.0 --xml --types

This creates two input files for OpenMM:

    field.xml
    config.pdb

Familiarize yourself with their formats and content.

Copy the two input files to the `fixq` folder to run an equilibration and a production trajectory.


## System setup: polarizable force field

Starting from the two OpenMM input files, a series of tools from `pol_openmm` creates the files for polarizable simulations.

The first step is to add the Drude induced dipoles based on the atomic polarizabilities in `alpha.ff`:

        polxml

This creates the modified files containing the Drude particles and their bonds to the core atoms:

    field-p.xml
    config-p.pdb

The second step is to scale the original Lennard-Jones potentials to remove double-counting of the polarization effects (which were included implicitly). The information is given in the `fragment.ff` which contains scaling factors for the the molecular fragments composing the ions. Running the script:

        scaleLJxml -s

produces a scaled force field file:

    field-p-sc.xml

Copy the `field-p-sc.xml` and `config-p.pdb` files to the `pol` folder to run simulations with the polarizable model.

----
