################################################################################
#
# RevBayes Example: Bayesian inference of phylogeny using a GTR+Gamma+Inv
#			substitution model on a single gene.
#
# authors: Sebastian Hoehna, Michael Landis, and Tracy A. Heath
#
################################################################################


### Read in sequence data for the gene
data = readDiscreteCharacterData("data/cich95.nex")

# Get some useful variables from the data. We need these later on.
n_species <- data.ntaxa()
n_branches <- 2 * n_species - 3
taxa <- data.taxa()


mvi = 0 
mni = 0


######################
# Substitution Model #
######################

# specify the stationary frequency parameters
pi_prior <- v(1,1,1,1) 
pi ~ dnDirichlet(pi_prior)
moves[++mvi] = mvBetaSimplex(pi, weight=2.0)
moves[++mvi] = mvDirichletSimplex(pi, weight=1.0)


# specify the exchangeability rate parameters
er_prior <- v(1,1,1,1,1,1)
er ~ dnDirichlet(er_prior)
moves[++mvi] = mvBetaSimplex(er, weight=3.0)
moves[++mvi] = mvDirichletSimplex(er, weight=1.5)


# create a deterministic variable for the rate matrix, GTR
Q := fnGTR(er,pi) 


#############################
# Among Site Rate Variation #
#############################

# among site rate variation, +Gamma4
alpha_prior_mean <- ln(2.0)
alpha_prior_sd <- 0.587405
alpha ~ dnLognormal( alpha_prior_mean, alpha_prior_sd )
sr := fnDiscretizeGamma( alpha, alpha, 4, false )
moves[++mvi] = mvScale(alpha, lambda=1.0, weight=2.0)


# the probability of a site being invariable, +I
p_inv ~ dnBeta(1,1)
moves[++mvi] = mvBetaProbability(p_inv, weight=2.0)


##############
# Tree model #
##############

out_group = clade("Onil_1675")
# Prior distribution on the tree topology	
topology ~ dnUniformTopology(taxa, outgroup=out_group)
moves[++mvi] = mvNNI(topology, weight=5.0)
moves[++mvi] = mvSPR(topology, weight=1.0)

# Branch length prior
for (i in 1:n_branches) {
    bl[i] ~ dnExponential(10.0)
	moves[++mvi] = mvScale(bl[i])
}

TL := sum(bl)
	
psi := treeAssembly(topology, bl)




###################
# PhyloCTMC Model #
###################

# the sequence evolution model
seq ~ dnPhyloCTMC(tree=psi, Q=Q, siteRates=sr, pInv=p_inv, type="DNA")

# attach the data
seq.clamp(data)


############
# Analysis #
############

mymodel = model(psi)

# add monitors
monitors[++mni] = mnScreen(alpha, p_inv, TL, printgen=1000)
monitors[++mni] = mnFile(psi, filename="output/cich95.trees", printgen=10)
monitors[++mni] = mnModel(filename="output/cich95.log",printgen=10)

# run the analysis
mymcmc = mcmc(mymodel, moves, monitors, nruns=2)
mymcmc.burnin(100000,200)
mymcmc.run(1000000)


# summarize output
treetrace = readTreeTrace("output/cich95.trees")
#treetrace.summarize()

map_tree = mapTree(treetrace,"output/cich95.tre")


# you may want to quit RevBayes now
q()


