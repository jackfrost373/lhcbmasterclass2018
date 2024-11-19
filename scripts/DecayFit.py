def DecayDistributions(omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime):
    if input("Show decay-time distributions? [y/N] ") not in ["y", "Y"]:
        return

    from ROOT import RooFit

    DecayFit("Bs"    , "Bs",     omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)
    DecayFit("Bs"    , "antiBs", omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)
    DecayFit("antiBs", "Bs",     omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)
    DecayFit("antiBs", "antiBs", omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime)

def DecayFit(prodID, decayID, omegaCut, Bs_Mass, Ds_Mass, Bs_Lifetime):

   print("************************************")
   print("* Showing tagged decay time for "+prodID+ " -> "+decayID)
   print("*  using omega < "+str(omegaCut))
   print("************************************")

   #f = TFile.Open("/data/stu18q1t/LHCbMasterclass2018/data/data.root")
   f = TFile.Open("/project/bfys/jdevries/lhcbmasterclass2018/data/data.root")
   t = f.Get("DecayTree")

   cuts = "(lab0_MM > %f) && (lab0_MM < %f) && " \
          "(lab2_MM > %f) && (lab2_MM < %f) && " \
          "(lab0_TAU > %f) && (lab0_TAU < %f)" % \
          (Bs_Mass[0], Bs_Mass[1], Ds_Mass[0], Ds_Mass[1], 
           Bs_Lifetime[0], Bs_Lifetime[1])

   if(prodID=="Bs")      : tag =  "1"
   if(prodID=="antiBs")  : tag = "-1"
   if(decayID=="Bs")     : piID = ">1" # Bs0 -> Ds- pi+
   if(decayID=="antiBs") : piID = "<1" # Bs0 -> Ds- pi+
   cuts += "&&(( ( (lab0_BsTaggingTool_TAGDECISION    == "+tag+" && lab0_BsTaggingTool_TAGOMEGA    < "+str(omegaCut)+")   || \
               (lab0_BsTaggingTool_TAGDECISION_OS == "+tag+" && lab0_BsTaggingTool_TAGOMEGA_OS < "+str(omegaCut)+") \
             ) && lab1_ID"+piID + "))"

   cDecay = TCanvas("cdecay","cdecay")
   nbins = 100
   binning = "("+str(nbins)+","+str(Bs_Lifetime[0])+","+ \
             str(Bs_Lifetime[1])+")"
   t.Draw("lab0_TAU>>decay"+binning, cuts)
   decay = gDirectory.Get("decay")
   decay.SetTitle("Decay Time ("+prodID+" -> "+decayID+"), TagOmega < " + str(omegaCut))
   decay.GetXaxis().SetTitle("Decay time [ns]")
   decay.GetYaxis().SetTitle("N(events)")
   decay.GetYaxis().SetTitleOffset(1.2)
   decay.SetMarkerStyle(20)
   decay.SetMarkerSize(1.1)
 
   latex = TLatex()
   latex.SetNDC(True)
   latex.SetTextSize(0.08)
   latex.SetTextColor(kBlue)
   latex.DrawLatex(0.5,0.8,prodID+" #rightarrow "+decayID)
   cDecay.Update()
   cDecay.SaveAs("plots/decayTime_"+prodID+"_to_"+decayID+".pdf")

   input("Press enter to continue.")
   f.Close()



