#!/usr/bin/env python3

"""
My tasks for Assignment 3.
Created by A.J. Turner on February 15, 2017.
Copyright 2017 A.J. Turner. All rights reserved.
Code modified from Week3_IntroToImportanceSampling (author jembrown) for like, prior, and posterior functions, and for coin flipping. Collaboration with P. Hart and D. Elias.
"""
from scipy.stats import binom, uniform
from random import random, gauss
import matplotlib.pyplot as plt
import numpy as np



def like(k, n, p, testingPrior=False):
    """Defining general function to calculate likelihoods if p<0 or p>1. Also, included a boolean switch to have this function always return 1, in order to test the prior."""

    if testingPrior:  # If True, this will always return 1. This can be useful if one wants
        return 1      # to test the machinery by estimating a known distribution (the prior).
    if p < 0:
        return 0
    elif p > 1:
        return 0
    else:
        return binom.pmf(k, n, p)


def prior(p):
    """Defining function to calculate prior density - uniform [0,1]"""

    return uniform.pdf(p) # by default, uniform is from 0 to 1
    # uniform has to have a finite upper bound and we have to pick one...
    # mean of the uniform is just 0.5


def posterior(k, n, p):
    """Defining function to calculate the unnormalized posterior density"""

    posterior = prior(p) * like(k, n, p, testingPrior=False)
    return posterior


def myDraw(n, p):
    """Drawing samples from a proposal distribution"""

    sample = np.random.binomial(n, p, 1)
    # print(type(sample))
    return sample


def chain(n, k, p, s):
    """Function to run a Markov chain with the proposal distribution"""
    pCurr = p
    pNew = s
    print (pNew)
    r = posterior(k, n, pNew)/posterior(k, n, pCurr)  # new parameter to propose
    #print(r)
    #print(pNew)
    #for 
    if r < 1: 
            pCurr = pCurr
    else:
            pCurr = pNew
    #Not sure how to code it...but I need to create a way to sometimes accept the step down (when r is less than 1)
    # to do this, I could somehow add and if statement that draws a random float value between 0 and 1 and compares that value to what I have for r (ratio. if the random value is greater than the value for r, accept the proposed move. if the random value is less than the value for r, reject the proposed move and make another copy of the pCurr in the chain.)
        
    #print (pCurr, pNew)    


"""
def traceIt(s):
    # Not sure how to do this...tried to immitate: http://isaacslavitt.com/2013/12/30/metropolis-hastings-and-slice-sampling/

    n = 50000  # number of replicates
    fig, (ax0, ax1) = plt.subplots(2, 1)  # setting the axes
    plt.plot(ax0, np.arange(n), s)
    ax0.set_xlabel('iteration number')  # x-axis label
    ax0.set_ylabel('value of sampled v')  # y-axis label
    plt.show()
"""

def histos(s):
    """attempting to plost histograms of parameter values, priors, liklihoods,and posteriors...but I need to generate more samples to plot"""

    count, bins, ignored = plt.hist(s, 10, normed=True)
    plt.show()

def main():
    # Defining data for binomial - in this case coin flips (2 outcomes)
    flips = ["H","T","H","T","H"]
    n = len(flips)        # Number (n) of binomial trials
    k = sum([1 for fl in flips if fl == "H"])  # Counting heads as successes(k)
    p = 0.3
    #defining data for normal distribution
    mu, sigma = 0, 1 # mean, standard deviation
    s = np.random.normal(mu, sigma, 100)  # generating rando norm. dist.
    print("The likelihood of my proposal", like(k, n, p,testingPrior=False))
    print("The prior is", prior(p))
    print("The posterior density estimate is", posterior(k, n, p))
    s = myDraw(n,p)
    #print(s)
    chain(n, k, p, s)
    #traceIt(s)
    histos(s)
    
    print("1. If the proposal distribution is too large, then the markov chain could simply move around the tail end of the target distribution and never get good mixing because you would have low rates of acceptance when proposing new parameters. If the proposal distribution is super tiny, then you will accept proposed parameters frequently and take a long time to mix and converge at the target distributon. ")

if __name__ == '__main__':
    main()
