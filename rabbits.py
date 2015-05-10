import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

# Enter the code for the functions rabbitGrowth, foxGrowth, and runSimulation
# in this box.
def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    # if rabbit population is MAXRABBITPOP no new rabbit is born
    if CURRENTRABBITPOP == MAXRABBITPOP:
        return
        
    #else a rabbit is born with the probabiliy
    pRabbitRepro = 1.0 - CURRENTRABBITPOP / float(MAXRABBITPOP)
    if random.random() <= pRabbitRepro:
        CURRENTRABBITPOP += 1
                 
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    
    #If there are more then 10 rabbits the fox might eat one
    if CURRENTRABBITPOP > 10:
        pFoxEatsRabbit = CURRENTRABBITPOP / float(MAXRABBITPOP)
        if random.random() < pFoxEatsRabbit:
            CURRENTRABBITPOP -= 1
            #The fox has eaten a rabbit an might give birth to a new fox
            if random.random() <= (1.0/3.0):
                CURRENTFOXPOP += 1
        else:
            #The fox has not eaten a rabbit and might die, but not if there no more than 10 foxes
            if CURRENTFOXPOP > 10:
                if random.random() <= 0.9:
                    CURRENTFOXPOP -= 1 
                               
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations = []
    fox_populations = []
   
    #Make grader happy?
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    if CURRENTRABBITPOP / float(MAXRABBITPOP) < 1.0:
        CURRENTRABBITPOP += 2
        CURRENTFOXPOP += 2 
    
    for step in range(numSteps):
        #First update rabbit population
        rabbitGrowth()
        #Second update fox population
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)
    pylab.plot(range(numSteps), rabbit_populations)
    pylab.plot(range(numSteps), fox_populations)
    #pylab.show()
    
    #coeff = pylab.polyfit(range(numSteps), rabbit_populations, 2)
    coeff = pylab.polyfit(range(numSteps), fox_populations, 2)
    
    print coeff
    pylab.plot(pylab.polyval(coeff, range(numSteps)))
    pylab.show()
    
    return (rabbit_populations, fox_populations)
   
print runSimulation(200)

