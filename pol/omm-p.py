#!/usr/bin/env python

import sys
import datetime
import numpy as np

import openmm
from openmm import app
from openmm import unit

#from velocityverletplugin import VVIntegrator
#import drudetrep

field = 'field-p-sc.xml'
config = 'config-p.pdb'
#config = 'equil.pdb'

temperature = 323.0*unit.kelvin
pressure = 1.0*unit.bar

print('#', datetime.datetime.now())
print()

print('#', field, config)
forcefield = app.ForceField(field)
pdb = app.PDBFile(config)

modeller = app.Modeller(pdb.topology, pdb.positions)

print('#  ', modeller.topology.getNumResidues(), 'molecules',
    modeller.topology.getNumAtoms(), 'atoms',
    modeller.topology.getNumBonds(), 'bonds')

box = modeller.topology.getUnitCellDimensions()
print('#   box', box.x, box.y, box.z, 'nm')

system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME,
    nonbondedCutoff=12.0*unit.angstrom, constraints=app.HBonds,
    ewaldErrorTolerance=1.0e-5)

print('# Drude Langevin integrator', temperature)
integrator = openmm.DrudeLangevinIntegrator(temperature, 5/unit.picosecond,
    1*unit.kelvin, 20/unit.picosecond, 1.0*unit.femtosecond)
#print('# Drude temperature-grouped integrator', temperature)
#integrator = VVIntegrator(temperature, 5/unit.picosecond,
#    1*unit.kelvin, 20/unit.picosecond, 1*unit.femtosecond)

integrator.setMaxDrudeDistance(0.2*unit.angstrom)
print('#   max Drude distance', integrator.getMaxDrudeDistance())

print('#   barostat', pressure)
barostat = openmm.MonteCarloBarostat(pressure, temperature)
#barostat.setFrequency(0)    # for constant NVT
system.addForce(barostat)

platform = openmm.Platform.getPlatformByName('CUDA')
#platform.setPropertyDefaultValue('Precision', 'mixed')
#properties = {'DeviceIndex': '0', 'Precision': 'mixed'}
properties = {'Precision': 'single'}

# force settings before creating Simulation
for i, f in enumerate(system.getForces()):
    f.setForceGroup(i)

sim = app.Simulation(modeller.topology, system, integrator, platform, properties)

sim.context.setPositions(modeller.positions)
#sim.context.setVelocitiesToTemperature(temperature)

## read coords and velocities from checkpoint (replaces sim.context.setPositions and setVelocitiesToTemperature)
## do only on the same machine
#print('# coordinates and velocities from equil.chk')
#sim.loadCheckpoint('equil.chk')

## read coords and velocities from restart file (replaces sim.context.setPositions and setVelocitiesToTemperature)
## any machine
#print('# coordinates and velocities from equil.rst')
#with open('equil.rst', 'r') as f:
#   sim.context.setState(openmm.XmlSerializer.deserialize(f.read()))

#print('# coordinates and velocities from state-eq.xml')
#sim.loadState('state-eq.xml')

#state = sim.context.getState()
#sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())

platform = sim.context.getPlatform()
print('# platform', platform.getName())
for prop in platform.getPropertyNames():
    print('#  ', prop, platform.getPropertyValue(sim.context, prop))

state = sim.context.getState(energy=True)
print('# PotentielEnergy', state.getPotentialEnergy())

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(energy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

## minimize only when starting from fresh conf, not after equilibration
print('# Minimizing.energy...')
sim.minimizeEnergy(maxIterations=500)
state = sim.context.getState(energy=True)
print('# PotentielEnergy', state.getPotentialEnergy())

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(energy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

sim.reporters = []
sim.reporters.append(app.StateDataReporter(sys.stdout, 5000, step=True,
    speed=True, temperature=True, separator='\t',
    totalEnergy=True, potentialEnergy=True, density=True))
sim.reporters.append(app.DCDReporter('equil.dcd', 5000, enforcePeriodicBox=False))
#sim.reporters.append(app.CheckpointReporter('equil.chk', 100000))
#sim.reporters.append(drudetrep.DrudeTReporter(sys.stdout, 5000, modeller.topology, system))

for i in range(200):
    sim.step(5000)

    # comment this out if using the DrudeTReporter
    print('#  Tdrude ',  integrator.computeDrudeTemperature())

print("# Force groups")
for i, f in enumerate(system.getForces()):
    state = sim.context.getState(energy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

state = sim.context.getState(positions=True, velocities=True, enforcePeriodicBox=True)
coords = state.getPositions()
sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())
app.PDBFile.writeFile(sim.topology, coords, open('equil.pdb', 'w'))

sim.context.setTime(0)
sim.context.setStepCount(0)
sim.saveState('state-eq.xml')
print('# state saved to state-eq.xml')

print()
print('#', datetime.datetime.now())
