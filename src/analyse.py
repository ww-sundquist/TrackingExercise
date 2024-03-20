import math
import DataFormats.FWLite as fwlite
import ROOT

events = fwlite.Events("file:output.root")
secondaryVertices = fwlite.Handle("std::vector<reco::VertexCompositeCandidate>")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

cosAngle_hist = ROOT.TH1F("cosAngle", "cosAngle", 100, -1.0, 1.0)
cosAngle_zoom_hist = ROOT.TH1F("cosAngle_zoom", "cosAngle_zoom", 100, 0.99, 1.0)
ksmasses1_hist = ROOT.TH1F("ksmass_hist", "Kshort mass distribution (no cuts); Mass [GeV]; N_{events}", 100, 0.2, 0.8)
ksmasses2_hist = ROOT.TH1F("ksmass_hist", "Kshort mass distribution (cut on dot product of momentum and displacement); Mass [GeV]; N_{events}", 100, 0.2, 0.8)

events.toBegin()

for i, event in enumerate(events):
	event.getByLabel("offlinePrimaryVertices", primaryVertices)
	event.getByLabel("SecondaryVerticesFromLooseTracks", "Kshort", secondaryVertices)
#	print "Event:", i
	for sv in secondaryVertices.product():
		svx = sv.vx()
		svy = sv.vy()
		svz = sv.vz()

		px = sv.px()
		py = sv.pz()
		pz = sv.pz()

		p = (px**2 + py**2 + pz**2)**0.5

#		print "     Normalized momentum (3-)vector: ", px/p, py/p, pz/p
		projlist = []
		projdislist = []
		for pv in primaryVertices.product():
			pvx = pv.x()
			pvy = pv.y()
			pvz = pv.z()

			dx = svx - pvx
			dy = svy - pvy
			dz = svz - pvz

			dl = ( (dx)**2 + (dy)**2 + (dz)**2 )**0.5

#			print "          Displacement vector: ", dx/dl, dy/dl, dz/dl		

			dpProj = ( (px*dx) + (py*dy) + (pz*dz) )/(p*dl)
			projlist.append(dpProj)
			projdislist.append(1.0 - dpProj)

		ksmasses1_hist.Fill(sv.mass())

		cosAngle_inst = projlist[projdislist.index(min(projdislist))]
		cosAngle_hist.Fill(cosAngle_inst)
		if cosAngle_inst > 0.99:
			ksmasses2_hist.Fill(sv.mass())

c1 = ROOT.TCanvas( "c1", "c1", 800, 800 )
cosAngle_hist.Draw()
c1.SaveAs("cosAngles.png")

c2 = ROOT.TCanvas( "c2", "c2", 800, 800 )
ksmasses2_hist.Draw()
c2.SaveAs("ksmasses2.png")

c3 = ROOT.TCanvas( "c3", "c3", 800, 800 )
ksmasses1_hist.Draw()
c3.SaveAs("ksmasses1.png")
