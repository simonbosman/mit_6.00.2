# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def runDrugSimulation(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, delaySteps):
    
    #create some resistant viruses
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for virus in range(numViruses)] 
    #infect the patient 
    patient = TreatedPatient(viruses, maxPop)
    
    #run simulation for delayed time steps
    for idx in range(delaySteps):
        patient.update()
   
    #add guttagonol
    patient.addPrescription('guttagonol')
    
    #run simulation for another 150 time steps
    for idx in range(150):
        patient.update()
    
    return patient.getTotalPop()
    

def runTwoDrugsSimulation(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, delaySteps):
      
    #create some resistant virusesgeinformeerd
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for virus in range(numViruses)] 
    
    #infect the patient 
    patient = TreatedPatient(viruses, maxPop)
    
    #run simulation for 150 steps
    for idx in range(150):
        patient.update()
    
    #add guttagonol
    patient.addPrescription('guttagonol')
   
    #run simulation for delayed time steps
    for idx in range(delaySteps):
        patient.update()
   
    #add grimpex
    patient.addPrescription('grimpex')
        
    #run simulation for another 150 time steps
    for idx in range(150):
        patient.update()
   
    return patient.getTotalPop()   
    
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    totPops = [0] * numTrials
    for idx in range(numTrials):
        totPops[idx] = runDrugSimulation(100, 1000, 0.1, 0.05,  {'guttagonol': False}, 0.005, 75)
    
    #Plot the graph
    pylab.hist(totPops, bins=10)
    pylab.title('Simulation for 1000 trials one drug')
    pylab.show()

 

#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    totPops = [0] * numTrials
    for idx in range(numTrials):
        totPops[idx] = runTwoDrugsSimulation(100, 1000, 0.1, 0.05,  {'guttagonol': False, 'grimpex': False}, 0.005, 0)
    
    #Plot the graph
    pylab.hist(totPops, bins=10)
    pylab.title('Simulation for 1000 trials two drugs')
    pylab.show()



#simulationDelayedTreatment(1000)
simulationTwoDrugsDelayedTreatment(1)               
                       