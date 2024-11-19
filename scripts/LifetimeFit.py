def LifetimeFit(Bs_Mass, Ds_Mass, Bs_Lifetime, Bs_fitRange):
   if input("Do lifetime fit? [y/N] ") not in ["y", "Y"]:
      return

   #f = TFile.Open("/data/stu18q1t/LHCbMasterclass2018/data/data.root")
   f = TFile.Open("/project/bfys/jdevries/lhcbmasterclass2018/data/data.root")
   t = f.Get("DecayTree")

   cDecay = TCanvas("cdecay","cdecay")
   cDecay.SetLeftMargin(0.16)

   cuts = "(lab0_MM > %f) && (lab0_MM < %f) && " \
          "(lab2_MM > %f) && (lab2_MM < %f) && " \
          "(lab0_TAU > %f) && (lab0_TAU < %f)" % \
          (Bs_Mass[0], Bs_Mass[1], Ds_Mass[0], Ds_Mass[1], 
           Bs_Lifetime[0], Bs_Lifetime[1])
   nbins = 100
   binning = "("+str(nbins)+","+str(Bs_Lifetime[0])+","+ \
             str(Bs_Lifetime[1])+")"
   t.Draw("lab0_TAU>>decay"+binning, cuts)
   decay = gDirectory.Get("decay")
   
   fitFunctie = "[0] * exp(-x/[1])"
   func = TF1("fitfunc", fitFunctie, Bs_fitRange[0], Bs_fitRange[1])
   func.SetParameters(3500,0.0015); # begin parameters
   func.SetParNames ("Amplitude", "Lifetime");
   func.SetLineColor(kRed)

   decay.SetTitle("")
   decay.GetXaxis().SetTitle("Decay time [ns]")
   decay.GetYaxis().SetTitle("N(events)")
   decay.GetYaxis().SetTitleOffset(1.2)
   decay.SetMarkerStyle(20)
   decay.SetMarkerSize(1.1)
 
   decay.Fit("fitfunc","","",Bs_fitRange[0], Bs_fitRange[1])
   
   cDecay.Update()
   cDecay.SaveAs("plots/decayTime.pdf")
   
   print("************************************")
   print("* Showing decay-time distribution")
   print("* --> Fitted lifetime = %.6f +- %.6f ps" % (1000*func.GetParameter(1), 1000*func.GetParError(1)))
   print("************************************")
   
   input("Press enter to continue.")
   f.Close()

