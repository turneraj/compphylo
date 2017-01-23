#!/usr/bin/env python
# encoding: utf-8

"""
My tasks for Assignment 1.
Created by A.J. Turner on January 17, 2017
Copyright 2017 A.J. Turner. All rights reserved.
Help obtained from stackoverflow postings.
"""


def lenSeq(mySeq):
    """finding the length of input dna sequence"""

    print("\nThe length of the sequence is:", len(mySeq), "bases")
    # gets the number of nucleotides (length of bases) in sequence


def transcribe(mySeq):
    """transcribes dna to rna by replacing thymine with uracil"""

    rna = mySeq.replace('t', 'u')  # replace function to convert T to U
    return rna  # return ends execution of function, gives result when called


def revComp(mySeq):
    """provide reverse compliment of dna"""

    reverseComp = ""  # empty string created to store the rev complement below
    for nucleotide in range(len(mySeq)-1, -1, -1):
        reverseComp = reverseComp + mySeq[nucleotide]  # should reverse seq
    reverseComp = reverseComp.replace("a", "T").replace("t", "A").replace("\
c", "G").replace("g", "C").lower()  # provides rev comp in all lowercase
    return reverseComp


def codons(mySeq):
    """extracting codon positions from sequence"""

    codons = []  # creating empty list for codons to store from for loop below
    for n in range(0, len(mySeq), 3):  # looks over seq every three characters
        codon = mySeq[n:n+3]  # creates codon (3 bases) and moves to next 3
        codons.append(codon)  # appending each codon into the above list
    print("\nThis is the 13th codon: ", codons[12])  # using index to get codon
    print("This is the 14th codon: ", codons[13], "\n")


def transIt(mySeq):
    """translating nucleotide sequence into amino acids using vert mito code"""

    upperSeq = mySeq.upper()
    AAs = "FFLLSSSSYY**CCWWLLLLPPPPHHQQRRRRIIMMTTTTNNKKSS**VVVVAAAADDEEGGGG"
    Base1 = "TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG"
    Base2 = "TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG"
    Base3 = "TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG"
    # the above code is from vertebrate mitochondrial code
    aaDict = {}  # create empty dictionary to store key (codon) and value (aa)
    for i in range(len(Base1)):
        aaDict[Base1[i]+Base2[i]+Base3[i]] = AAs[i]
        # for loop to add base positions together to correspond to AAs
    codons = []  # creating empty list for codons to store from for loop below
    for n in range(0, len(upperSeq), 3):  # looks over seq by three characters
        codon = upperSeq[n:n+3]  # creates codon (3 bases) and moves to next 3
        codons.append(codon)  # appends all codons into the empty list 'codons'
    aaS = []  # empty list to store amino acids translated from seq
    for cod in codons:  # for looping through codons from our dna seq
        if len(cod) == 3:  # check codon to be 3 nucleotides long, execute if Y
            aa = aaDict[cod]  # get value(aa) of codon when it matches dic
            # key(condon)
            aaS.append(aa)  # storing amino acids that were translated from seq
        else:  # if the codon is less than 3 nucleotides, just continue loop
            continue
    return aaS


def main():
    mySeq = "aaaagctatcgggcccataccccaaacatgttggttaaaccccttcctttgctaattaatccttac\
gctatctccatcattatctccagcttagccctgggaactattactaccctatcaagctaccattgaatgttagcc\
tgaatcggccttgaaattaacactctagcaattattcctctaataactaaaacacctcaccctcgagcaattgaa\
gccgcaactaaatacttcttaacacaagcagcagcatctgccttaattctatttgcaagcacaatgaatgcttga\
ctactaggagaatgagccattaatacccacattagttatattccatctatcctcctctccatcgccctagcgata\
aaactgggaattgccccctttcacttctgacttcctgaagtcctacaaggattaaccttacaaaccgggttaatc\
ttatcaacatgacaaaaaatcgccccaatagttttacttattcaactatcccaatctgtagaccttaatctaata\
ttattcctcggcttactttctacagttattggcggatgaggaggtattaaccaaacccaaattcgtaaagtccta\
gcattttcatcaatcgcccacctaggctg"
    lenSeq(mySeq)
    print("\nThe RNA would be:\n", transcribe(mySeq))
    print("\nThe reverse complement is:\n", revComp(mySeq))
    codons(mySeq)
    print("\n The amino acids are:\n", transIt(mySeq))


if __name__ == '__main__':
    main()
