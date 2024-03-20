import DataFormats.FWLite as fwlite
import math
import ROOT

events = fwlite.Events("file:run321167_ZeroBias_AOD.root")
primaryVertices = fwlite.Handle("std::vector<reco::Vertex>")

rho_z_histogram = ROOT.TH2F("rho_z", "rho_z", 100, 0.0, 30.0, 100, 0.0, 10.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    for vertex in primaryVertices.product():
   	 rho_z_histogram.Fill(abs(vertex.z()),
                    		 math.sqrt(vertex.x()**2 + vertex.y()**2))

c = ROOT.TCanvas("c", "c", 800, 800)
rho_z_histogram.SetTitle('Primary vertices; z [cm]; rho [cm]')
rho_z_histogram.Draw("colz")
c.SaveAs("rho_z.png")

# # #

deltaz_histogram = ROOT.TH1F("deltaz", "deltaz", 1000, -20.0, 20.0)

events.toBegin()
for event in events:
    event.getByLabel("offlinePrimaryVertices", primaryVertices)
    pv = primaryVertices.product()
    for i in xrange(pv.size() - 1):
   	 for j in xrange(i + 1, pv.size()):
   		 deltaz_histogram.Fill(pv[i].z() - pv[j].z())

c = ROOT.TCanvas ("c", "c", 800, 800)
deltaz_histogram.SetTitle('PV spread; Distance between PVS [cm]; N_{events}')
deltaz_histogram.Draw()
c.SaveAs("deltaz.png")
