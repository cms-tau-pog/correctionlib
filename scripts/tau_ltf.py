#! /usr/bin/env python3
# Author: Izaak Neutelings (January 2021)
# https://github.com/nsmith-/correctionlib/blob/master/convert.ipynb
# https://github.com/cms-tau-pog/TauIDSFs/blob/master/utils/createSFFiles.py
# https://cms-nanoaod-integration.web.cern.ch/integration/master-106X/mc102X_doc.html#Tau
import sys; sys.path.append('..')
from correctionlib.schemav1 import Correction
#from correctionlib.schemav1 import CorrectionSet
import json, jsonschema
# antiEleEtaBins = ( 0.0, 1.460, 1.558, 2.3 )
# antiMuEtaBins  = ( 0.0, 0.4, 0.8, 1.2, 1.7, 2.3 )

# e -> tauh fake rate SF
def etf():
  print(">>> 1D SFs")
  xbins = [0.0,1.460,1.558,2.3]
  nsfs  = len(xbins)-1
  wps   = ['Medium',] # 'Tight']
  sfs   = {wp: [1.0 for s in range(nsfs)] for wp in wps}
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
    'data': { # category WP -> category syst -> binning eta
      'nodetype': "category",
      #'input': "genmatch",
      'keys': [1,'*'],
      'content': [
        { 'nodetype': "category", # WP
          #'input': "wp",
          'keys': wps,
          'content': [
            { 'nodetype': "category", # syst
              #'input': "syst",
              'keys': ["nom", "up", "down"],
              'content': [
                { 'nodetype': "binning", # nominal
                  #'input': "eta",
                  'edges': xbins,
                  'content': sfs.get(wp,[1.]), },
                { 'nodetype': "binning", # up
                  #'input': "eta",
                  'edges': xbins,
                  'content': sfs.get(wp,1.), },
                { 'nodetype': "binning", # down
                  #'input': "eta",
                  'edges': xbins,
                  'content': sfs.get(wp,1.), },
              ],
            } for wp in wps
          ],
        },
        1.0, # default value
      ],
    },
  })
  print(corr1)
  print(corr1.data.content)
  #help(corr1)
  with open("../data/tau/tau_ltf.json", "w") as fout:
    fout.write(corr1.json(exclude_unset=True,indent=2))
  
  

if __name__ == '__main__':
  print()
  etf()
  print()
