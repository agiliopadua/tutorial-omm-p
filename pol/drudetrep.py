#!/usr/bin/env python

import numpy as np

from openmm import unit


class DrudeTReporter(object):
    """DrudeTReporter outputs the temperatures of atoms and Drude degrees of freedom
    in a polarizable simulation"""

    kB = unit.BOLTZMANN_CONSTANT_kB/(unit.joule/unit.kelvin)
    NA = unit.AVOGADRO_CONSTANT_NA*unit.mole

    def __init__(self, file, reportInterval, topology, system):
        """Create a DrudeTReporter

        Parameters
        ----------
        file : string or file
            The file to write to, specified as a file name or file object
        reportInterval : int
            The interval (in time steps) at which to write frames
        topology : Topology
            The topology of the system
        system : System
            The system to report on
        """

        self._openedFile = isinstance(file, str)
        if self._openedFile:
            self._out = open(file, 'w')
        else:
            self._out = file
        self._reportInterval = reportInterval

        self.iat = [ i for i, atom in enumerate(topology.atoms()) if atom.name[0] != 'D' ]
        self.idr = [ i for i, atom in enumerate(topology.atoms()) if atom.name[0] == 'D' ]
        nat = len(self.iat)
        ndr = len(self.idr)

        nall = topology.getNumAtoms()
        self.mall = np.array([ system.getParticleMass(i)/unit.dalton for i in range(nall) ])

        ncons = system.getNumConstraints()

        self.dof_all = 3*nall - ncons
        self.dof_at = 3*nat - ncons
        self.dof_dr = 3*ndr

        # reduced mass of DC-DP pairs
        self.mu = np.zeros(nall)
        for i in self.idr:
            self.mu[i] = 1.0/(1.0/self.mall[i-1] + 1.0/self.mall[i])
        self.mu = self.mu.reshape((nall, 1))
        self.vdr = np.zeros((nall, 3))

        # add Drude masses back to cores
        self.mat = np.copy(self.mall)
        for i in self.idr:
            self.mat[i-1] += 0.4
        self.mat = self.mat.take(self.iat)
        self.mat = self.mat.reshape((nat, 1))

        self.mall = self.mall.reshape((nall, 1))

        self._out.write(f'# {nat} atoms {ndr} DP {ncons} constraints\n')


    def describeNextReport(self, simulation):
        """Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : Simulation
            The Simulation to generate a report for

        Returns
        -------
        dict
            A dictionary describing the required information for the next report
        """

        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return {'steps': steps, 'periodic': None, 'include': ['velocities']}


    def report(self, simulation, state):
        """Generate a report.

        Parameters
        ----------
        simulation : Simulation
            The Simulation to generate a report for
        state : State
            The current state of the simulation
        """

        vel = state.getVelocities(asNumpy=True)/(unit.nanometer/unit.picosecond)
        Tall = np.sum(self.mall*vel**2)/(self.dof_all*self.kB)*(1e3/self.NA)*unit.kelvin
        vat = vel.take(self.iat, axis=0)
        Tat = np.sum(self.mat*vat**2)/(self.dof_at*self.kB)*(1e3/self.NA)*unit.kelvin

        for i in self.idr:
            self.vdr[i] = vel[i] - vel[i-1]
        Tdr = np.sum(self.mu*self.vdr**2)/(self.dof_dr*self.kB)*(1e3/self.NA)*unit.kelvin
        
        self._out.write(f'# Tall {Tall} Tatoms {Tat} Tdrude {Tdr}\n')


    def __del__(self):
        if self._openedFile:
            self._out.close()
