#! /usr/bin/env python
# Author: Izaak Neutelings (January 2021)
# https://root.cern/doc/master/classTHistPainter.html
from __future__ import print_function
from ROOT import gStyle, TFile, TH1F, TH2F, TCanvas, kBlue
from array import array
gStyle.SetOptStat(False)  # no stat. box
gStyle.SetOptTitle(False) # no hist title
gStyle.SetEndErrorSize(5) # end of error bars


def test():
  
  xtitle = "Electron |#eta|"
  ytitle = "Electron p_{T} [GeV]"
  dtitle = "#tau_{h} decay mode"
  stitle = "Electron ID/ISO SF"
  etitle = "#tau_{h} energy scale"
  xbins  = [0.0,1.5,2.5] # eta
  ybins  = [0.0,20,50,100] # pT
  dms    = [0,1,10] #11]
  dbins  = [float(i) for i in range(len(dms)+1)] # DM
  nxbins = len(xbins)-1
  nybins = len(ybins)-1
  ndbins = len(dms)
  sfs1   = [(0.84,0.10),(0.91,0.15),]
  sfs2   = [(0.90,0.10),(1.00,0.10),(0.80,0.15),
            (1.10,0.15),(0.85,0.15),(1.00,0.15),]
  sfs3   = [(0.97,0.12),(1.01,0.10),(0.98,0.17),]
  
  # TH1
  print(">>> 1D SFs")
  hist1 = TH1F('hist1','hist1',nxbins,array('d',xbins))
  hist1.SetLineWidth(2)
  hist1.SetLineColor(kBlue)
  hist1.SetMarkerStyle(8)
  hist1.SetMarkerSize(1.5)
  hist1.SetMarkerColor(kBlue)
  for i, (sf,err) in enumerate(sfs1,1):
    hist1.SetBinContent(i,sf)
    hist1.SetBinError(i,err)
  hist1.SetMinimum(0.0)
  hist1.SetMaximum(1.1)
  canvas = TCanvas('canvas','canvas',100,100,700,600)
  canvas.SetMargin(0.10,0.04,0.11,0.02) # LRBT
  hist1.Draw('E1')
  hist1.GetXaxis().SetTitle(xtitle)
  hist1.GetYaxis().SetTitle(stitle)
  hist1.GetXaxis().SetTitleSize(0.050)
  hist1.GetYaxis().SetTitleSize(0.050)
  hist1.GetXaxis().SetTitleOffset(1.00)
  hist1.GetYaxis().SetTitleOffset(0.97)
  hist1.GetXaxis().SetLabelSize(0.045)
  hist1.GetYaxis().SetLabelSize(0.045)
  canvas.SaveAs("hist1D.png")
  canvas.SaveAs("hist1D.pdf")
  
  # TH2
  print(">>> 2D SFs")
  hist2 = TH2F('hist2','hist2',nybins,array('d',ybins),nxbins,array('d',xbins))
  for i, (sf,err) in enumerate(sfs2,1):
    hist2.SetBinContent(i,sf)
    hist2.SetBinError(i,err)
  
  # TH1 - categories
  print(">>> 1D SFs")
  hist3 = TH1F('hist3','hist3',ndbins,0,ndbins)
  hist3.SetLineWidth(2)
  hist3.SetLineColor(kBlue)
  hist3.SetMarkerStyle(8)
  hist3.SetMarkerSize(1.5)
  hist3.SetMarkerColor(kBlue)
  for i, (sf,err) in enumerate(sfs3,1):
    hist3.SetBinContent(i,sf)
    hist3.SetBinError(i,err)
  hist3.SetMinimum(0.0)
  hist3.SetMaximum(1.3)
  canvas = TCanvas('canvas','canvas',100,100,700,600)
  canvas.SetMargin(0.10,0.04,0.11,0.02) # LRBT
  hist3.Draw('E1')
  for i, dm in enumerate(dms,1):
    hist3.GetXaxis().SetBinLabel(i,str(dm))
  hist3.GetXaxis().SetTitle(dtitle)
  hist3.GetYaxis().SetTitle(etitle)
  hist3.GetXaxis().SetTitleSize(0.050)
  hist3.GetYaxis().SetTitleSize(0.050)
  hist3.GetXaxis().SetTitleOffset(1.00)
  hist3.GetYaxis().SetTitleOffset(0.97)
  hist3.GetXaxis().SetLabelOffset(0.003)
  hist3.GetXaxis().SetLabelSize(0.075)
  hist3.GetYaxis().SetLabelSize(0.045)
  canvas.SaveAs("hist1D_categories.png")
  canvas.SaveAs("hist1D_categories.pdf")
  
  
  

if __name__ == '__main__':
  print()
  test()
  print()
  
