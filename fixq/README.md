# Fixed-charge simulations

## Contents

* `omm.py`: OpenMM script for simulations with a fixed-charge force field

## Equilibration

Edit the `omm.py` script to use the following settings:

* Temperature 323 K, a lower viscosity helps. 
* Langevin integrator, fast and robust, a great choice for the equilibration phase. It is also an acceptable choice when computing thermodynamic and structural quantities. However, since it is a stochastic integrator, dynamic quantities are not faithfully computed.
* Barostat, allows the system to relax to its equilibrium density at constant <em>NpT</em>.
* Set initial velocities to temperature.
* Perform an initial energy minimization to relax the system.
* 1 ns trajectory, 1 000 000 steps saving every 5000 (200 configurations) to `equil.dcd`.
* Save the last configuration to `equil.pdb` and the last state to `state-eq.xml`.

Then run the equilibration:

        ./omm.py &> equil.out &

Follow the progress with:

        tail -f equil.out

Note the execution speed in ns/day. This run should take less than 10 min on an average GPU.

Use vmd to visualize the trajectory:

        vmd -e ../utils/pbc-com.vmd config.pdb equil.dcd

Plot the density to see if the system has reached equilibrium.


## Production trajectory

Modify the `omm.py` script:

* Nosé-Hoover integrator, a deterministic integrator that gives correct dynamics.
* Trajectory at constant <em>NVT</em>, so no need to add a barostat.
* Do not set initial velocities to temperature.
* Do not perform an initial minimization
* Read the initial configuration and velocities from `state-eq.xml`.
* Run a 5 ns trajectory saving 2000 snapshots to `traj.dcd`.

Change the names of output files as needed (`equil.dcd` -> `traj.dcd`; `equil.pdb` -> `last.pdb`, ...) Then run a 5 ns trajectory saving 2000 snapshots:

        ./omm.py &> run.out &


## Trajectory analysis

Use the Jupyter notebooks in the `../utils` folder to calculate radial distribution functions and diffusion coefficients from the trajectory.

The diffusion coefficients can be compared with experimental values from a publication available in `../refs`.

----
