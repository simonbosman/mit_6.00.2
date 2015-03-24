import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    def pick_ball(bucket):
        return random.choice(range(len(bucket)))
    
    three_balls = 0
    
    for num in range(numTrials):
    
        bucket = ['r','r','r','g','g','g']
        balls = []
    
        for i in range(3):
            ball = pick_ball(bucket)
            balls.append(bucket.pop(ball))
     
        if sum( [1 for ball in balls if ball == balls[0]]) == 3:
           three_balls += 1
     
    return three_balls/float(numTrials)
    
print noReplacementSimulation(3)