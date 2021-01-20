#! /usr/bin/env python3
# Author: Izaak Neutelings (January 2021)
# https://github.com/nsmith-/correctionlib/blob/master/convert.ipynb
# https://github.com/cms-tau-pog/TauIDSFs/blob/master/utils/createSFFiles.py
# https://cms-nanoaod-integration.web.cern.ch/integration/master-106X/mc102X_doc.html#Tau
import sys; sys.path.append('..')
assert sys.version_info>=(3,8),"Python version must be newer than 3.8, currently %s.%s"%(sys.version_info[:2])
from correctionlib.schemav1 import Correction
#from correctionlib.schemav1 import CorrectionSet
import json, jsonschema


def etf():
  """e -> tauh fake rate SF"""
  print("\n>>> e -> tauh fake rate SF")
  fname = "../data/tau/tau_etf.json"
  xbins = [0.0,1.460,1.558,2.3]
  nsfs  = len(xbins)-1
  wps   = ['Medium',] # 'Tight','VTight','VVTight']
  sfs   = {wp: [1.0 for s in range(nsfs)] for wp in wps}
  uncs  = {wp: [0.1 for s in range(nsfs)] for wp in wps}
  print(xbins,sfs)
  corr1 = Correction.parse_obj({
    'version': 0,
    'name':    "test",
    'inputs': [
      {'name': "eta",      'type': "real",   'description': "tau eta"},
      {'name': "genmatch", 'type': "int",    'description': "genmatch (0 or 6: no match, jet, 1 or 3: electron, 2 or 4: muon, 5: real tau"},
      {'name': "wp",       'type': "string", 'description': "DeepTauVSe WP: VVVLoose-VVTight"},
      {'name': "syst",     'type': "string", 'description': "systematic 'nom', 'up', 'down'"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': { # category:genmatch -> category:WP -> category:syst -> binning:eta
      'nodetype': "category",
      'input': "genmatch",
      'keys': [1],
      'default': 1.0, # default value
      'content': [
        { 'nodetype': "category", # WP
          'input': "wp",
          'keys': wps,
          'content': [
            { 'nodetype': "category", # syst
              'input': "syst",
              'keys': ["nom", "unc"],
              'content': [
                { 'nodetype': "binning", # eta
                  'input': "abseta",
                  'edges': xbins,
                  'content': sfs[wp],
                },
                { 'nodetype': "binning",
                  'input': "abseta",
                  'edges': xbins,
                  'content': uncs[wp],
                },
              ],
            } for wp in wps
          ],
        },
      ],
    },
  })
  print(corr1)
  print(corr1.data.content)
  print(f">>> Writing {fname}...")
  with open(fname,'w') as fout:
    fout.write(corr1.json(exclude_unset=True,indent=2))
  

def mtf():
  """mu -> tauh fake rate SF"""
  print("\n>>> mu -> tauh fake rate SF")
  fname = "../data/tau/tau_mtf.json"
  xbins = [0.0,0.4,0.8,1.2,1.7,2.3]
  nsfs  = len(xbins)-1
  wps   = ['Medium','Tight','VTight']
  sfs   = {wp: [1.0 for s in range(nsfs)] for wp in wps}
  uncs  = {wp: [0.1 for s in range(nsfs)] for wp in wps}
  print(xbins,sfs)
  corr1 = Correction.parse_obj({
    'version': 0,
    'name':    "test",
    'inputs': [
      {'name': "eta",      'type': "real",   'description': "tau eta"},
      {'name': "genmatch", 'type': "int",    'description': "genmatch (0 or 6: no match, jet, 1 or 3: electron, 2 or 4: muon, 5: real tau"},
      {'name': "wp",       'type': "string", 'description': "DeepTauVSe WP: VVVLoose-VVTight"},
      {'name': "syst",     'type': "string", 'description': "systematic 'nom', 'up', 'down'"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': { # category:genmatch -> category:WP -> category:syst -> binning:eta
      'nodetype': "category",
      'input': "genmatch",
      'keys': [2],
      'default': 1.0, # default value
      'content': [
        { 'nodetype': "category", # WP
          'input': "wp",
          'keys': wps,
          'content': [
            { 'nodetype': "category", # syst
              'input': "syst",
              'keys': ["nom", "unc"],
              'content': [
                { 'nodetype': "binning", # eta
                  'input': "abseta",
                  'edges': xbins,
                  'content': sfs[wp],
                },
                { 'nodetype': "binning",
                  'input': "abseta",
                  'edges': xbins,
                  'content': uncs[wp],
                },
              ],
            } for wp in wps
          ],
        },
      ],
    },
  })
  print(corr1)
  print(f">>> Writing {fname}...")
  with open(fname,'w') as fout:
    fout.write(corr1.json(exclude_unset=True,indent=2))
  
  

if __name__ == '__main__':
  etf()
  mtf()
  print()

