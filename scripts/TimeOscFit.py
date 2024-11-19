def TimeOscFit(offset = 0.0, amplitude = 40.0, period = 0.002, phase = 0.0,
      omegaCut = "0.49", Bs_Mass = (5330,5400), Ds_Mass = (1955, 1985), Bs_Lifetime = (0, 0.01), doFit = False):

   action = "fit" if doFit else "plot"
   if input("Do Bs-Bsbar asymmetry %s? [y/N] " % (action)) not in ["y", "Y"]:
       return

   print("**********************************")
   print("Doing Bs-Bsbar asymmetry %s:" % (action))
   print("offset    = " + str(offset))
   print("amplitude = " + str(amplitude))
   print("period    = " + str(period))
   print("phase     = " + str(phase))
   #print "* - Using selection:               *"
   #print "* TAGOMEGA < " + str(omegaCut)
   #print "*  Bs_Mass: " + str(Bs_Mass)
   #print "*  Ds_Mass: " + str(Ds_Mass)
   #print "*  Bs_Lifetime: " + str(Bs_Lifetime)
   print("**********************************")


   #f = TFile.Open("workspace.root")
   #w = f.Get("w")
   #assert(isinstance(w, RooWorkspace))

   #decayTime = w.var("lab0_TAU")

   # Not sure how to construct (formula)weighted histograms from the RooDataSet... So just recreate!
   #f = TFile.Open("/data/stu18q1t/LHCbMasterclass2018/data/data.root")
   f = TFile.Open("./data/data.root")
   t = f.Get("DecayTree")

   #if(useOmegaWeights) :
   #  weight_SS = "(1-2*lab0_BsTaggingTool_TAGOMEGA)"
   #  weight_OS = "(1-2*lab0_BsTaggingTool_TAGOMEGA_OS)"
   #else :
   #  weight_SS = weight_OS = "(1.)"

   cuts = "(lab0_MM > %f) && (lab0_MM < %f) && (lab2_MM > %f) && (lab2_MM < %f) && (lab0_TAU > %f) && (lab0_TAU < %f)\
       " % (Bs_Mass[0], Bs_Mass[1], Ds_Mass[0], Ds_Mass[1], Bs_Lifetime[0], Bs_Lifetime[1])

   #cuts_Bs_SS     =  "(lab0_BsTaggingTool_TAGDECISION     ==  1 && lab0_BsTaggingTool_TAGOMEGA    < "+omegaCut+")"
   #cuts_Bs_OS     =  "(lab0_BsTaggingTool_TAGDECISION_OS  ==  1 && lab0_BsTaggingTool_TAGOMEGA_OS < "+omegaCut+")"
   #cuts_antiBs_SS =  "(lab0_BsTaggingTool_TAGDECISION     == -1 && lab0_BsTaggingTool_TAGOMEGA    < "+omegaCut+")"
   #cuts_antiBs_OS =  "(lab0_BsTaggingTool_TAGDECISION_OS  == -1 && lab0_BsTaggingTool_TAGOMEGA_OS < "+omegaCut+")"
   cuts_Bs_FS     = "(lab1_ID > 0)"
   cuts_antiBs_FS = "(lab1_ID < 1)"

   cuts_Bs     = "((lab0_BsTaggingTool_TAGOMEGA_OS + lab0_BsTaggingTool_TAGOMEGA) < %f) && (lab0_BsTaggingTool_TAGDECISION ==  1 || lab0_BsTaggingTool_TAGDECISION ==  0) && (lab0_BsTaggingTool_TAGDECISION_OS != -lab0_BsTaggingTool_TAGDECISION)" % (2. * omegaCut)
   cuts_antiBs = "((lab0_BsTaggingTool_TAGOMEGA_OS + lab0_BsTaggingTool_TAGOMEGA) < %f) && (lab0_BsTaggingTool_TAGDECISION == -1 || lab0_BsTaggingTool_TAGDECISION ==  0) && (lab0_BsTaggingTool_TAGDECISION_OS != -lab0_BsTaggingTool_TAGDECISION)" % (2. * omegaCut)

   #cuts_Bs_Bs         = "("+cuts + " && " + "("+cuts_Bs_SS    +" || "+cuts_Bs_OS    +") && ("+cuts_Bs_FS    +"))"
   #cuts_antiBs_antiBs = "("+cuts + " && " + "("+cuts_antiBs_SS+" || "+cuts_antiBs_OS+") && ("+cuts_antiBs_FS+"))"
   #cuts_Bs_antiBs     = "("+cuts + " && " + "("+cuts_Bs_SS    +" || "+cuts_Bs_OS    +") && ("+cuts_antiBs_FS+"))"
   #cuts_antiBs_Bs     = "("+cuts + " && " + "("+cuts_antiBs_SS+" || "+cuts_antiBs_OS+") && ("+cuts_Bs_FS    +"))"
   cuts_Bs_Bs         = "("+cuts + " && " + "("+cuts_Bs+") && ("+cuts_Bs_FS    +"))"
   cuts_antiBs_antiBs = "("+cuts + " && " + "("+cuts_antiBs+") && ("+cuts_antiBs_FS+"))"
   cuts_Bs_antiBs     = "("+cuts + " && " + "("+cuts_Bs+") && ("+cuts_antiBs_FS+"))"
   cuts_antiBs_Bs     = "("+cuts + " && " + "("+cuts_antiBs+") && ("+cuts_Bs_FS    +"))"

   nbins = 100
   print("> Building time osc histograms...")
   cOsc = TCanvas("cOsc","cOsc", 1000, 500)
   cOsc.SetLeftMargin(0.1)
   binning = "("+str(nbins)+","+str(Bs_Lifetime[0])+","+str(Bs_Lifetime[1])+")"
   t.Draw("lab0_TAU>>dec_Bs_Bs"        +binning, cuts_Bs_Bs + "*(1+0*(lab0_MM>5400))"   )
   t.Draw("lab0_TAU>>dec_antiBs_antiBs"+binning, cuts_antiBs_antiBs + "*(1+0*(lab0_MM>5400))")
   t.Draw("lab0_TAU>>dec_Bs_antiBs"    +binning, cuts_Bs_antiBs    )
   t.Draw("lab0_TAU>>dec_antiBs_Bs"    +binning, cuts_antiBs_Bs    )
   dec_Bs_Bs         = gDirectory.Get("dec_Bs_Bs")
   dec_antiBs_antiBs = gDirectory.Get("dec_antiBs_antiBs")
   dec_Bs_antiBs     = gDirectory.Get("dec_Bs_antiBs")
   dec_antiBs_Bs     = gDirectory.Get("dec_antiBs_Bs")

   for hist in [dec_Bs_Bs,dec_antiBs_antiBs,dec_Bs_antiBs,dec_antiBs_Bs] : hist.Sumw2()

   total_notosc = dec_Bs_Bs.Clone("total_notosc")
   total_notosc.Add(dec_antiBs_antiBs, +1)

   total_osc = dec_Bs_antiBs.Clone("total_osc")
   total_osc.Add(dec_antiBs_Bs, +1)

   denom = total_notosc.Clone("denominaeiorj")
   denom.Add(total_osc, +1)

   teller = total_notosc.Clone("teller")
   teller.Add(total_osc, -1)

   asymmetry = teller.Clone("Asymmetry")
   asymmetry.Divide(teller, denom, 1, 1, "B")

   osc_Bs       = dec_Bs_Bs.Clone("osc_Bs")
   osc_Bs_denom = dec_Bs_Bs.Clone("osc_Bs_denom")
   osc_Bs.Add(       dec_Bs_antiBs, -1 )
   osc_Bs_denom.Add( dec_Bs_antiBs, +1 )
   osc_Bs.Divide( osc_Bs_denom )

   osc_antiBs       = dec_antiBs_antiBs.Clone("osc_antiBs")
   osc_antiBs_denom = dec_antiBs_antiBs.Clone("osc_antiBs_denom")
   osc_antiBs.Add(       dec_antiBs_Bs, -1 )
   osc_antiBs_denom.Add( dec_antiBs_Bs, +1 )
   osc_antiBs.Divide( osc_antiBs_denom )

   oscFull = osc_Bs.Clone("oscFull")
   oscFull.Add( osc_antiBs )

   asymmetry.SetTitle("")
   asymmetry.GetXaxis().SetTitle("Decay time [ns]")
   asymmetry.GetYaxis().SetTitle("Asymmetry [%]")
   asymmetry.SetMarkerStyle(20)
   asymmetry.SetMarkerSize(1.2)
   asymmetry.SetMarkerColor(kBlue)

   # We fitten vier parameters
   # We fitten de functie "func"
   # En intern noemen we deze "fitfunc"

   fitFunctie = "[0] + [1] * cos(2 * 3.14 * (1/[2]) * x + [3])"
   func = TF1("fitfunc", fitFunctie, Bs_Lifetime[0], Bs_Lifetime[1])
   func.SetParameters(offset, amplitude, period, phase); # begin parameters
   # Namen van de parameters
   func.SetParNames ("Offset", "Amplitude", "Period", "Phase" );
   func.SetLineColor(kRed)
   func.SetTitle("Mixing Asymmetry")
   func.SetNpx(1000)

   if doFit:
       asymmetry.Fit("fitfunc");
       print("Fit Chi-Squared: %f" % (func.GetChisquare()))
       print("Fit Reduced Chi-Squared %f" % (func.GetChisquare() / func.GetNDF()))
   """
   cOsc.Clear()
   func.Draw()
   func.GetXaxis().SetTitle("Lifetime [ns]")
   func.GetYaxis().SetTitle("(Unmixed - Mixed) / (Unmixed + Mixed)")
   func.GetYaxis().SetRangeUser(-.5, .5)
   func.GetHistogram().SetMaximum( 0.5)
   func.GetHistogram().SetMinimum(-0.5)
   asymmetry.Draw("SAME")
   cOsc.Update()
   """
   asymmetry.Draw()
   func.Draw("same")
   asymmetry.GetYaxis().SetTitle("(Unmixed - Mixed) / (Unmixed + Mixed)")
   asymmetry.GetYaxis().SetTitleSize(0.05)
   asymmetry.SetMaximum( 0.5)
   asymmetry.SetMinimum(-0.5)
   cOsc.Modified()
   cOsc.Update()

   """
   oscHist_Bs     = RooDataHist("oscHist_Bs"    , "oscHist_Bs"    , RooArgList(decayTime), osc_Bs    )
   oscHist_antiBs = RooDataHist("oscHist_antiBs", "oscHist_antiBs", RooArgList(decayTime), osc_antiBs)
   oscHist_Full   = RooDataHist("oscHist_Full"  , "oscHist_Full"  , RooArgList(decayTime), oscFull)


   print "> Overlaying fit shape..."
   m_offset = RooRealVar("m_offset","m_offset",offset,0.0,100.0)
   m_amplitude = RooRealVar("m_amplitude","m_amplitude",amplitude,0.0,100.0)
   m_period = RooRealVar("m_period","m_period",period,0.0,100.0)
   m_phase = RooRealVar("m_phase","m_phase",phase,0.0,100.0)
   model = RooFormulaVar("OscModel","OscModel","m_offset + m_amplitude * cos(2 * 3.14 * (1/m_period) * lab0_TAU + m_phase)",
         RooArgList(decayTime, m_offset, m_amplitude, m_period, m_phase) )


   cOsc.Clear()
   frame = decayTime.frame()
   frame.SetTitle("(Bs->Bs - Bs->antiBs) / (Bs->Bs + Bs -> antiBs)")
   #frame.SetTitle("(nonOsc - osc) / (nonOsc + osc)")
   RooDataHist("asymmetry", "asymmetry", RooArgList(decayTime), asymmetry).plotOn(frame, RooFit.DataError(RooAbsData.SumW2), RooFit.XErrorSize(1.))
   model.plotOn(frame)
   frame.Draw()
   cOsc.Update()
   cOsc.SaveAs("plots/TimeOsc.pdf")
   """
   input("Press enter to continue.")
   f.Close()




