#!/bin/env python
##################################
#== IMPORTS ======================
##################################
from ROOT import *
gROOT.ProcessLine(".x lhcbStyle.C")
TH1.SetDefaultSumw2(True)
exec(open('./scripts/MassFit.py').read())
exec(open('./scripts/LifetimeFit.py').read())
exec(open('./scripts/DecayFit.py').read())
exec(open('./scripts/TimeOscFit.py').read())

##################################
#== BODY =========================
##################################

# SELECTION ######################
Bs_Mass      = (4800, 6000)
Ds_Mass      = (1880, 2080)
Bs_Lifetime  = (0.0 , 0.01)

# MASS FITS ######################

MassFit("Ds",Bs_Mass, Ds_Mass, Bs_Lifetime)
MassFit("Bs",Bs_Mass, Ds_Mass, Bs_Lifetime)

# DECAY-TIME FITS ################

Bs_fitRange = (0.0 , 0.01)

LifetimeFit(Bs_Mass, Ds_Mass, Bs_Lifetime, Bs_fitRange)

omegaCut = 0.42

DecayDistributions(omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)

# OSCILLATION FIT ################

offset     = 0.0
amplitude  = 0.4
period     = 0.001
phase      = 0.0

TimeOscFit(offset, amplitude, period, phase, omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime, False)

##################################
