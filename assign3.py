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


def like(k, n, p, testingPrior = False):
    """Defining general function to calculate likelihoods if p<0 or p>1. Also, included a boolean switch to have this function always return 1 in order to test the prior. Adopted from J. Brown."""

    if testingPrior:  # If True, this will always return 1.
        return 1      # to test the machinery by estimating a known distribution (the prior).
    if p < 0:
        return 0
    elif p > 1:
        return 0
    else:
        return binom.pmf(k, n, p)


def prior(p):
    """Defining function to calculate prior density - uniform [0,1]. Adopted from J. Brown."""

    return uniform.pdf(p) # by default, uniform is from 0 to 1
    # uniform has to have a finite upper bound and we have to pick one...
    # mean of the uniform is just 0.5


def posterior(k, n, p):
    """Defining function to calculate the unnormalized posterior density. Adopted from J. Brown."""

    posterior = prior(p) * like(k, n, p, testingPrior = False)
    return posterior


def myDraw(pCurr, k, n, p):
    """Drawing samples from a proposal distribution and deciding to accept that proposed parameter or stick with the previous value for another iteration through chain."""

    numReps = 1
    numValues = 1
    uniScale = 1
    pNew = uniform.rvs(size = numValues, loc = p, scale = uniScale)
    rando = np.random.uniform(0, 1)
    # rvs means no matter what, give my random draws
    # somehow you want to make loc the pcurrent value so that each time you make a draw...it's reasonable and not random
    r = posterior(k, n, pNew)/posterior(k, n, pCurr)
    if r >= 1: 
        p_val = pNew
    elif rando <= r:
        p_val = pNew
    else: 
        p_val = pCurr
    # print("the p_val is", p_val)
    return p_val


def chain(n, k, pCurr, p):
    """Function to run a Markov chain with the proposal distribution"""

    ngen = 200
    likes = []
    priors = []
    posts = []
    p_vals = []
    p_val = myDraw(pCurr, k, n, p)  # starting value for the chain to get going
    for proposal in range(ngen):  # for-loop to run chain ngen times
        p_val = myDraw(p_val, k, n, p)  # proposing a parameter
        p_vals.append(p_val)  # appending parameter to list of parameters in chain
        mylike = like(k, n, p_val, testingPrior = False) # likelihood of param
        likes.append(mylike)  # appending each likelihood to list of likes
        myprior = prior(p_val)  # prior for each param
        priors.append(myprior)  # appending prior values to a list
        myposterior = posterior(k, n, p_val)  # posterior probability of param
        posts.append(myposterior)  # appending posts to a list
    # print("list of p_vals", sorted(p_vals))  # checking values in all lists
    # print("list of likes", likes)
    # print("list of priors", priors)
    # print("lis of posterior probs", posts)
    # plotting histograms of each list created in for-loop above 
    # histograms are not taking frequency of param into account..not sure why
    count, bins, ignored = plt.hist(p_vals, 20, normed = 1, facecolor = "green")
    plt.title("Histogram of Parameters")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
    count, bins, ignored = plt.hist(likes, 20, normed = 1, facecolor = "blue")
    plt.title("Histogram of Likelihoods")
    plt.grid(True)
    plt.show()
    count, bins, ignored = plt.hist(priors, 20, normed = 1, facecolor = "red")
    plt.title("Histogram of Priors")
    plt.grid(True)
    plt.show()
    count, bins, ignored = plt.hist(posts, 20, normed = 1, facecolor = "black")
    plt.title("Histogram of Posterior Probs")
    plt.grid(True)
    plt.show()
    # plotting trace plots....
    fig,ax = plt.subplots()  # start of trace plot of parameters
    ax.plot(p_vals)
    x =ax.set(xlabel = 'Samples', ylabel = 'Parameters')
    plt.show()
    fig,ax = plt.subplots()  # start of trace plot of likelihoods
    ax.plot(likes)
    x = ax.set(xlabel = 'Samples', ylabel = 'Likelihoods')
    plt.show()
    fig,ax = plt.subplots()  # start of trace plot of priors
    ax.plot(priors)
    x = ax.set(xlabel = 'Samples', ylabel = 'Priors')
    plt.show()
    fig,ax = plt.subplots()  # start of trace plot of likelihoods
    ax.plot(posts)
    x = ax.set(xlabel = 'Samples', ylabel = 'Posterior Probabilities')
    plt.show()


def main():
    # Defining data for binomial - in this case coin flips (2 outcomes)
    flips = ["H","H","H","T","H"]
    # flips = flips*2  # easy way to increase both trial size and successes
    n = len(flips)        # Number (n) of binomial trials
    k = sum([1 for fl in flips if fl == "H"])  # Counting heads as successes(k)
    p = 0.3
    pCurr = p
    #defining data for normal distribution
    mu, sigma = 0, 1 # mean, standard deviation
    s = np.random.normal(mu, sigma, 100)  # generating rando norm. dist.
    like(k, n, p, testingPrior = False)
    prior(p)
    posterior(k, n, p)
    chain(n, k, pCurr, p)
    print("\n1. If the proposal distribution is too large, then the markov chain could simply move around the tail end of the target distribution and never get good mixing or converge on the target distribution because you would have low rates of acceptance when proposing new parameters. If the proposal distribution is super tiny, then you will accept proposed parameters frequently and take a long time to mix and converge at the target distributon. ")
    print("\n2. The chain takes maybe 10 samples to burn-in when the dataset is small (say 5-20 trials for n). When the dataset is increased to around 100 trials, the burn-in increases to around 100 samples.")
    print("\n3. Dataset for a Normal is defined, however, couldn't figure out an easy way to propose parameters for both mean and standard deviation.")
    print("\n4. I'm not confident that I sampled well...sometimes my trace plots look okay and well-mixed, but when increases in dataset size occur (trials/successes), those plots look like a skyline. I also have no idea how to run multiple independent analyses - partition job on separate cores on laptop?")

if __name__ == '__main__':
    main()
