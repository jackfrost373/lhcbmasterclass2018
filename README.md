# Bs Oscillation Masterclass
Welcome to this LHCb Masterclass, in which you will use actual LHCb data to observe Bs mesons oscillating into their antiparticles and back. This project requires the following libraries:
  * Python 2.6 or newer
  * ROOT 5 or 6
  * RooFit
  * PyRoot

## Files
This project contains a number of files to help get you from a raw data file to a fit. The following files are available:
  * Selection.py allows you to make a clean selection of the raw data sample you have been provided with.
  * MassFit.py allows you to make a fit to the reconstructed Bs mass, using the data output by Selection.py.
  * DecayFit.py allows you to cut on the reconstructed Bs lifetime, and then make an exponential fit to that variable.
  * main.py contains commands to run all the above scripts. At the beginning of the files are some tuples, which represent the cuts that will be made by the other scripts.
