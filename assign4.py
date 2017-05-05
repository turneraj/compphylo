"""
We will need to draw random numbers (using random) and we will need to use
some special functions for matrices (using numpy).
Help and collaboration provided by Diego Elias, Pam Hart, and Jessica Storer.
"""
import random
import numpy

class MarkovChain(object):
    """
    A discrete-state, discrete-time Markov chain.
    """
    def __init__(self, stateSpace = [], qMat = [], numIter = 50, numChain = 1, simList = [] ):
        """
        Initializing variables that are necessary for simulating a discrete-time Markov chain:
            - state space
            - Q-matrix (transition matrix)
            - number of iterations
            - number of chains
            - list of simulated states (or list of lists for >1 chain)
        """
        self.stateSpace = stateSpace  # state space
        self.qMat = qMat  # Q-matrix
        self.numIter = numIter  # number of iterations
        self.numChain = numChain  # number of chains
        self.simList = simList  # list of lists to hold simulated chains
                    
    def discSamp(self,states=[],probs=[]):
        """
        Samples from an arbitrary discrete distribution.
        States and probs lists must be equal in length. Probs must sum to 1.
        """
        r = random.random()
        cumulProb = 0
        index = 0
        for p in probs:
            cumulProb = cumulProb + p
            if r < cumulProb:
                return states[index]
            index += 1
        print("ERROR: Probabilities did not add to 1!")

    def run(self,startState):
        """
        Method to simulate the states sampled by a Markov chain.
        """
        
        # Reset chains here to empty list of lists
        self.simList = []
        
        # For loop across chains (we'll simulate chains one at a time)
        for n in range(self.numChain):
            # Initialize this chain to an empty list
            self.simList.append([])
            # Add starting state to this chain
            state = self.stateSpace[0]
            
            # For loop across iterations for this chain
            for it in range(self.numIter):             
                # Draw the next state using the discSamp function. This function
                # takes two arguments:
                #   (1) The list of possible states
                #   (2) The row of probabilities from the Q-matrix, 
                #       conditioned on the current state.
                state = self.discSamp(self.stateSpace, self.qMat[self.stateSpace.index(state)])
                
                # Add the new state to this chain.
                self.simList[n].append(state)
         
    def showChain(self, numChain = 0, place = -1):
        """
        Method to simply print out the states sampled by a chain. Provide
        ability to print a particular iteration of a chain or the whole chain.
        """
        if place is -1:
            # Print out entire chain
            print(self.simList[numChain])
            
        elif place > -1 and place < len(self.simList[numChain]):
            # Print just that iteration in that chain
            print(self.simList[numChain][place])
        
    def stateFreqs(self, state = None, start = 0, end = None):
        """
        Method to calculate and print the frequencies of a particular state
        across chains.
        """

        if end is None:
            # By default, set end to last iteration
            end = self.simList[numChain][it]
            
        # Initialize list of frequencies
        freqs = []
        
        # For loop from start iteration to end iteration
        for it in range(self.numIter[numChain]):
            # Initialize variable to hold counts of state across chains
            count = 0
            
            # For loop across chains
            for n in range(self.numChain):
                
                # Check if the current state is the state of interest
                if current == self.qMat[self.stateSpace.index(state)]:
                    # If so, add to the count
                    count += 1
                else: break  
            # Divide by total num of chains and add freq to list
            freq = count/self.numChain
            freqs.append(freq)
            
        # Print or return the list of frequencies
        print(freqs)

    def forwardProb(self, numChain, numIter):
        """
        Calculate the probability of observing the full set of states 
        simulated for a particular chain, assuming the chain went in a 
        forward direction.
        """

        # Initialize the probability to 1.0
        prob = 1.0
        
        # For loop across iterations     
        for it in range(self.numIter):
            # Find the index of the state for the current iteration (A)
            A = self.qMat[self.stateSpace.index(A)]
            # Find the index of the state for the next iteration (B)
            B = self.qMat[self.stateSpace.index(B+1)]
            # Multiply overall probability by P(B|A) using Q-matrix
            prob *= self.qMat[A][B]
            
        # Return the probability
        return prob
    
    def reverseProb(self, numChain, numIter):
        """
        Calculate the probability of observing the full set of states 
        simulated for a particular chain, assuming the chain went in a 
        REVERSE direction.
        
        The code for this method is just like forwardProb, but your for
        loop should run in reverse - from the end of the chain back to the
        beginning.
        """

         # Initialize the probability to 1.0
        prob = 1.0
        
        # For loop across iterations     
        for it in range(0, self.numIter, -1):
            # Find the index of the state for the current iteration (A)
            A = self.qMat[self.stateSpace.index(A)]
            # Find the index of the state for the next iteration (B)
            B = self.qMat[self.stateSpace.index(B+1)]
            # Multiply overall probability by P(B|A) using Q-matrix
            prob *= self.qMat[A][B]
            
        # Return the probability
        return prob
 


       
    def margForwardProb(self, numIter, qMat, numChain):
        """
        Calculate the MARGINAL probability of starting in one state and ending
        """

        # Raise your Q-matrix to the power of the number of iterations. You'll
        # need numpy.linalg.matrix_power() for this.
        Qmat = numpy.matrix(self.qMat)
        numpy.linalg.matrix_power(Qmat * self.numIter)
        # Find the index of the starting state for the chain (S)
        start = self.discSamp(self.stateSpace, self.qMat[self.stateSpace.index(start)])
        # Find the index of the ending state for the chain (E)
        end =  self.simList[numChain].index(end)
        # Look up P(E|S) in the new matrix

        # Return the relevant probability       
        return 


qMat = [[0.5, 0.5], [0.3, 0.7]]
stateSpace = ["S", "R"]  
chain = MarkovChain(stateSpace=stateSpace, qMat=qMat)
chain.run(startState="S")
chain.showChain(numChain=0, place=-1)
print(chain.simList)
print(chain.statFreqs(state = None, start = 0, end = None))


"""
Part 2: Extend (or define a new) class for discrete-state, continuous-time chains
    - Be able to simulate waiting times and draws of new states
    - If you know stationary frequencies, be able to normalize Q-matrix
        - i.e., weighted average of diagonal entries is 1
    - Be able to calculate the probability of a sequence of changes
        - Going forward
        - Going backward
"""

class contMC(object):
    """
    This class defines values needed for a markov chain to run.
    """

    def __init__(self, stateSpace, eq, R, brl, nSites, startSeq = [], endSeq = []):
        """
        Initializing variables associated with the markov chain
        - state space
        - Q matrix
        - length of branches
        - number of sites
        -list of simulated states (or list of lists for >1 site)
        -list of waiting times (or list of lists for >1 site)
        - starting sequence (empty if simulating)
        - ending sequence (empty if simulating)
        """

        self.stateSpace = stateSpace    # state spae
        self.eq = eq                    # equilibrium freq
        self.R = R                      # exchangeabilities
        self.Q = []                         # Q-matrix
        self.brl = brl                  # branch length
        self.nSites = nSites            # number of sites (chains)
        self.simStates = []             # list of simulated states
        self.waitTimes = []             # list of waiting times
        self.startSeq = startSeq        # starting sequence
        self.endSeq = endSeq            # ending sequence
        self.likelihood = 1             # overall likelihood


    def discreteDraw(self, sampStates=[], probs=[]):
        """
        drawing a sample from an arbitrary distribution
        """

        r = random.random()
        cumulProb = 0
        index = 0
        for p in probs:
            cumulProb = cumulProb + p 
            if r <cumulProb:
                return states[index]
            index += 1

    def clear(self):
        """
        Method to empty our lists of simulated states and waiting times
        """
        self.simStates = []
        self.waitTimes = []
        self.likelihood = 1

    def createQ(self):
        """
        Method to create Q-matrix from equilibrium frequencies and exhangeabilities
        """
        
        numStates = len(self.stateSpace)
        Q = numpy.matrix(numpy.zeros(shape=(numStates,numStates)))
        for row in range(numStates):        # rows
            for col in range(numStates):    # columns
                if (row != col):
                    Q[row,col] = self.eq[col]
        rIndex = 0
        for row in range(numStates):
            for col in range(numStates):
                if [col > row]:
                    Q[row,col] *= self.R[rIndex]
                    rIndex += 1
        rIndex = 0
        for col in range(numStates):
            for row in range(numStates):
                if [col < row]:
                    Q[row,col] *= self.R[rIndex]
                    rIndex += 1
        for state in range(numStates):
            Q[state, state] = 


    def run(self):
        """
        Method to simulate the states sampled by a Markov Chain
        """

        #reset chains here to empty list
        self.clear()

        # for loop across chains
        for site in range(self.nSites):  # allows to do multiple chains

            # define starting sequence
            if len(self.startSeq) < site:
                self.startSeq[site] = self.discreteDraw(self.stateSpace, self.eq)

"""        
Part 3: Simulate DNA evolution along a branch under Jukes-Cantor
    - Define a discrete-state (4 nucleotides), continuous-time chain
    - Be sure to normalize Q-matrix (equal nucleotide frequencies)
    - Draw a list of starting nucleotides
    - For each one, simulate evolution along a branch of given length
        - Store character states and waiting times for these simulations
"""
JKmat = [[-1, 1/3, 1/3, 1/3], [1/3, -1, 1/3, 1/3], [1/3, 1/3, -1, 1/3], [-1, 1/3, 1/3, -1]]


"""   
Part 4: Generalize the Jukes-Cantor model to simulate under GTR. Verify that the simulation
    is working properly by:
    - Comparing forward and reverse probabilities for simulated histories
    - Simulate along very long branches to ensure that state frequencies match expectations
    - Compare the average number of changes to the expected branch length
"""



