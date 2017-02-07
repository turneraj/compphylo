#!/usr/bin/env python
# encoding: utf-8

"""
My tasks for Assignment 2.
Created by A.J. Turner on January 29, 2017
Copyright 2017 A.J. Turner. All rights reserved.
Help obtained from stackoverflow postings and S. Shakya. Collaboration with
phart for some problems.

"""
# import time is used when I want to time some of the functions
import scipy
import numpy as np
import matplotlib.pyplot as plt
import random

def myFact(minim, maxim):
    """ factorial-like function that uses a range (minimum and maximum)"""

    num = maxim
    for i in range(minim, maxim):  # iteratively going through a range
        num *= i  # mult the maximum by each value in the range from min to max
    return num  # executing the function to get the result (num)


def binomCo(k, n):
    """ calculating binomial coefficent by calculating all factorials fully,\
    piece by piece for the binomial coefficent formula"""

    # start = time.time()
    n1 = n  # saving variable to eventually store as n factorial
    k1 = k  # saving variable to eventually store as k factorial
    diff = (n - k)
    for i in range(1, n):  # n!
        n1 *= i
    for i in range(1, diff):  # (n-k)!
        diff *= i
    for i in range(1, k):  # k!
        k1 *= i
    # end = time.time()
    # elapsed = end - start
    return (n1/(diff*k1))  # equation for binomial
    # coefficient when the answer is given, it will be ('time to run', the
    # actual time, binomial coeffient)


def simpBi(k, n):
    """ function to cancel some terms in the binomial coefficient formular for\
quicker computing"""

    # start = time.time()
    n2 = n  # saving variable to eventually store as n factorial
    k2 = k  # saving variable to eventually store as k factorial
    for i in range((n - k + 1), n):  # denom of binom equation
        n2 *= i
    for i in range(1, k):  # getting k factorial
        k2 *= i
    # end = time.time()
    # elapsed = end - start
    return (n2/k2)  # returning simplified equation


def Pmf(n, k, p):
    """ Probability mass function (pmf) for the binonmial (n, p) distribution. \
Theorem 3.3.5 was used to calculate pmf."""

    biCo = simpBi(k, n)
    # print(biCo)  # to see if passing my function worked.
    return biCo*(pow(p, k))*(pow(1 - p, n - k))  # putting everything into form


def discDist():
    """ Sampling from an artbitrary distribution - function has two arguments\
, events (fishes) and probabilty of those events (catching each fish). The \
list of events and probabilities need to be the same length. Collaboration\
 with D. Elias and P Hart"""

    fishes = np.array(["guppy", "molly", "swordtail", "platy"])
    # events to sample
    probEv = np.array([0.5, 0.75, 0.2, 0.1])
    # list of probabilities for catching each type of fish in fishes list
    print("Based on the probability of catching each type of fish, when you\
 try to net a fish from a tank 10 times, with replacement,\
 you'll get", np.random.choice(fishes, 10, list(probEv)))


def likelihood(n, k, pCurr, diff):
    """ calculating the likelihood for our starting parameter, pCurr, and then
comparing that value to likelihoods for two parameters - one above (pUp = pCurr
+ diff) and one below (pDown = pCurr - diff) our starting parameter value."""

    pUp = pCurr + diff
    # print("pUP is", pUp)
    pDown = pCurr - diff
    # print("pDown is", pDown)
    biCo = simpBi(k, n)
    likepCurr = biCo*(pow(pCurr, k))*(pow(1 - pCurr, n - k))
    # print("likepCurr is", likepCurr)
    likepUp = biCo*(pow(pUp, k))*(pow(1 - pUp, n - k))
    # print("likepUp is", likepUp)
    likepDown = biCo*(pow(pDown, k))*(pow(1 - pDown, n - k))
    # print("likepDown is", likepDown)
    maxLike = max(likepCurr, likepUp, likepDown)  # obtainthe best likelihood
    if likepCurr != maxLike:  # if the likelihood of pCurr is not the max
        if likepUp > likepDown:  # if like pUp is greater than likepDown
            pCurr = pUp  # pCurr will be pUp b/c pUp should have the max like
        else:
            pCurr = pDown  # if pDown has best like, then set pCurr = pDown
    return maxLike, pCurr


def optimP(n, k, pCurr, diff, p=-1):
    """ Looping to check and update p values. p of -1 is used so that the while
 loop will always initiate...since you can't have a negative probability."""

    while pCurr != p:
        p = pCurr
        like, pCurr = likelihood(n, k, pCurr, diff)
    return like, p


def mySim(n, diff):
    """ function that will randomly draw a value for k (number of successes)\
for 100 datasets."""

    # start with p
    myP = 0.4

    # generate a lit of values for k (100 values) to get 100 datasets
    simK = []
    for num in range(100):
        simK.append(random.randrange(1, n + 1))
    # print(simK)  # checking to see if I have 100 values for k
    for k in simK:
        # calculate the max likelihood parameter of p using def likelihood
        # and def optimP with each value for k



def main():
    k = minim = 4
    n = maxim = 20
    p = 0.3
    diff = 0.001
    pCurr = p
    print("(2a: 1) The factorial of", maxim, "from range", maxim, "to\
", minim, "is", myFact(minim, maxim))
    print("\n(2a: 2a) The binonmial coefficient of", n, "choose", k, "is\
", binomCo(k, n))
    print("\n(2a: 2b) The fast way...", simpBi(k, n))
    print("\n(2a: 3) My simplified function for calculating the binomial\
coefficient takes 0.0031s to compute the binomial coefficient and my function\
 that calculates it using factorials fully is ~0.0000080s. The value of k was\
 200 and the value of n was 2704.\n")
    print("(2a: 4) PMF was found to be", Pmf(n, k, p), "when p was", p, "\n")
    discDist()
    print(optimP(n, k, pCurr, diff))
    """plist = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    llist = []
    for i in plist:
        llist.append(likelihood(n, k, i, diff=0)[0])
    # print(plist)
    # print(llist)
    plt.plot(plist, llist)
    plt.show()  # visualizing likelihood distribution to check my function"""
    mySim(n, diff)

if __name__ == '__main__':
    main()
