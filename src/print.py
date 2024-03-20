import ROOT

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

import DataFormats.FWLite as fwlite
events = fwlite.Events("file:run321167_ZeroBias_AOD.root")
tracks = fwlite.Handle("std::vector<reco::Track>")
MVAs = fwlite.Handle("std::vector<float>")

for i, event in enumerate(events):
	if i >= 5: break # print info only about the first 5 events
	print "Event", i
	event.getByLabel("generalTracks", tracks)
	event.getByLabel("generalTracks", "MVAValues", MVAs)

	numTotal = tracks.product().size()
	if numTotal == 0: continue
	numLoose = 0
	numTight = 0
	numHighPurity = 0

	for j, (track, mva) in enumerate(zip(tracks.product(),MVAs.product())):
		if track.quality(track.qualityByName("loose")): numLoose += 1
		if track.quality(track.qualityByName("tight")): numTight += 1
		if track.quality(track.qualityByName("highPurity")): numHighPurity += 1

    		print "	Track", j,
    		print "\t charge/pT: %.3f" %(track.charge()/track.pt()),
    		print "\t phi: %.3f" %track.phi(),
    		print "\t eta: %.3f" %track.eta(),
    		print "\t dxy: %.4f" %track.dxy(),
    		print "\t dz: %.4f"  %track.dz()
		print "\t nHits: %s" %track.numberOfValidHits(), "(%s P+ %s S)"%(track.hitPattern().numberOfValidPixelHits(),track.hitPattern().numberOfValidStripHits()),
		print "\t algo: %s" %track.algoName(),
		print "\t mva: %.3f" %mva

	print "Event", i,
	print "numTotal:", numTotal,
	print "numLoose:", numLoose, "(%.1f %%)"%(float(numLoose)/numTotal*100),
	print "numTight:", numTight, "(%.1f %%)"%(float(numTight)/numTotal*100),
	print "numHighPurity:", numHighPurity, "(%.1f %%)"%(float(numHighPurity)/numTotal*100)
