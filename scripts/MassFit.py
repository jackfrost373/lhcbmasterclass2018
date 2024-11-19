def MassFit(particle, Bs_Mass, Ds_Mass, Bs_Lifetime) :
   if input("Do %s mass fit? [y/N] " % (particle)) not in ["y", "Y"]:
       return

   print("************************************")
   print("* Doing mass fit                   *")
   print("************************************")

   #f = TFile.Open("/data/stu18q1t/LHCbMasterclass2018/data/data.root")
   f = TFile.Open("/project/bfys/jdevries/lhcbmasterclass2018/data/data.root")
   t = f.Get("DecayTree")

   cMass = TCanvas("cMass_"+particle, "cMass"+particle)
   cMass.SetLeftMargin(0.17);

   cuts = "(lab0_MM > %f) && (lab0_MM < %f) && " \
          "(lab2_MM > %f) && (lab2_MM < %f) && " \
          "(lab0_TAU > %f) && (lab0_TAU < %f)" % \
          (Bs_Mass[0], Bs_Mass[1], Ds_Mass[0], Ds_Mass[1], 
           Bs_Lifetime[0], Bs_Lifetime[1])

   if (particle == "Bs"):
     mass =  RooRealVar("BsMass", "B_{s} mass", 
                         Bs_Mass[0], Bs_Mass[1], "MeV/c^{2}")
     meanRange = [5366., 5360., 5372.]
     binning = "(100,"+str(Bs_Mass[0])+","+str(Bs_Mass[1])+")"
     t.Draw("lab0_MM>>hMass"+binning,cuts)
   if (particle == "Ds"):
     mass =  RooRealVar("DsMass", "D_{s} mass", 
                        Ds_Mass[0], Ds_Mass[1], "MeV/c^{2}")
     meanRange = [1970., 1965., 1975.]
     binning = "(100,"+str(Ds_Mass[0])+","+str(Ds_Mass[1])+")"
     t.Draw("lab2_MM>>hMass"+binning,cuts)
   hMass = gDirectory.Get("hMass")
   mean  = RooRealVar("mean",  "mass (MeV)",  meanRange[0], meanRange[1], 
                                              meanRange[2]) ;
   width = RooRealVar("width", "width (MeV)", 15.,   5.,   50.) ;
   const = RooRealVar("const", "bg const", -0.005, -0.1, 0.1);

   sigModel = RooGaussian(   "sigModel", "signal PDF", mass, mean, width) ;
   bkgModel = RooExponential("bkgModel", "bkgrnd PDF", mass, const) ;

   Nsig = RooRealVar("Nsig", "signal Yield", 10000., 0., 10000000.);
   Nbkg = RooRealVar("Nbkg", "bkgrnd Yield", 10000., 0., 10000000.);
   model = RooAddPdf("model", "full PDF", RooArgList(sigModel, bkgModel), 
                     RooArgList(Nsig, Nbkg));

   # Make a binned RooDataHist to speed up fit
   dataBinned = RooDataHist("dataBinned","dataBinned", RooArgList(mass),hMass)
   RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
   result=model.fitTo(dataBinned, RooFit.Save(True), RooFit.PrintLevel(-1))
   result.Print()

   frame = mass.frame()
   frame.SetStats(False)
   frame.SetTitle("Fit to the %s mass" % (particle))
   dataBinned.plotOn(frame, RooFit.DataError(RooAbsData.SumW2))
   model.plotOn(frame, RooFit.LineColor(4 ) ) #9
   model.plotOn(frame, RooFit.LineColor(8 ), RooFit.LineStyle(2), RooFit.Components("sigModel"), RooFit.Name("sig") )
   model.plotOn(frame, RooFit.LineColor(46), RooFit.LineStyle(2), RooFit.Components("bkgModel"), RooFit.Name("bkg") )

   frame.SetTitleOffset(1.2, "Y")
   frame.SetTitleOffset(1.0, "X")
   frame.Draw()

   leg = TLegend(0.64, 0.77, 0.89, 0.89)
   leg.AddEntry(frame.findObject("sig"), "Signal ("+particle+")", "l")
   leg.AddEntry(frame.findObject("bkg"), "Background", "l")
   leg.Draw("same")

   cMass.Update()
   cMass.SaveAs("plots/MassFit"+particle+".pdf")
   print(" > Showing mass fit for %s" % (particle))
   print(" > Signal events:     %d +- %d" % (Nsig.getVal(), Nsig.getError()))
   print(" > Background events: %d +- %d" % (Nbkg.getVal(), Nbkg.getError()))
   from math import sqrt
   #print Nsig.getVal() / sqrt(Nsig.getVal()+Nbkg.getVal())
   
   input("Press enter to continue.")
   f.Close()

