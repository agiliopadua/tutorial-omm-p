# Polarizable simulations

## Contents

* `omm-p.py`: OpenMM script for simulations with a polarizable force field using Drude induced dipoles

## Equilibration

Edit the `omm-p.py` script to use the following settings:

* Temperature 323 K. 
* Drude Langevin integrator.
* Barostat, allows the system to relax to its equilibrium density at constant <em>NpT</em>.
* **Do not** set initial velocities to temperature (works better for polarizable models).
* Perform an initial energy minimization to relax the system.
* Run a 1 ns trajectory, 1 000 000 steps saving every 5000 (200 configurations) to `equil.dcd`.
* Save the last configuration to `equil.pdb` and the last state to `state-eq.xml`.

Run the equilibration:

        ./omm-p.py &> equil.out &


## Production trajectory

Modify the `omm.py` script:

* Import the integrator from `velocityverletplugin` (a better Nosé-Hoover integrator). Also import the `druderep` module to print temperatures.
* Trajectory at constant <em>NVT</em>, so no need to add a barostat.
* Do not set initial velocities to temperature.
* Do not perform an initial minimization
* Read the initial configuration and velocities from `state-eq.xml`.
* Add a `Reporter` using `druderep.DrudeTReporter` to print temperatures. Also, comment out the line in the step cycle that printed temperatures during the equilibration.
* Run a 5 ns trajectory saving 2000 snapshots to `traj.dcd`.

Change the names of output files as needed (`equil.dcd` -> `traj.dcd`; `equil.pdb` -> `last.pdb`, ...) Then run a 5 ns trajectory saving 2000 snapshots:

        ./omm-p.py &> run.out &


## Trajectory analysis

Use the Jupyter notebooks in the `../utils` folder to calculate radial distribution functions and diffusion coefficients from the trajectory.

The diffusion coefficients can be compared with experimental values from a publication available in `../refs`.

It is also interesting to plot the displacements of the Drude particles from their cores (a Jupyter notebook is provided).

----
