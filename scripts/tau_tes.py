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

def maketesunc(low,high):
  """Interpolate."""
  return f"x<34?{low}: x<170?{low}+({high}-{low})/(170.-34.)*(x-34): {high}"

def tes():
  """TES"""
  print("\n>>> tau energy scale")
  fname   = "../data/tau/tau_tes.json"
  ptbins  = [0.,34.,170.]
  etabins = [0.,1.5,2.5]
  dms     = [0,1,10] #,11
  fesdms  = [0,1,] # for FES only DM0 and 1
  tes     = {dm: 1.0 for dm in dms}
  fes     = {dm: [1.0]*(len(etabins)-1) for dm in fesdms}
  tesuncs = {dm: (0.01,0.10) for dm in dms}
  fesuncs = {dm: [0.1]*(len(etabins)-1) for dm in fesdms}
  corr1   = Correction.parse_obj({
    'version': 0,
    'name':    "test",
    'inputs': [
      {'name': "eta",      'type': "real",   'description': "tau eta"},
      {'name': "pt",       'type': "real",   'description': "tau pt"},
      {'name': "dm",       'type': "int",    'description': "tau decay mode (0, 1, 10, or 11)"},
      {'name': "genmatch", 'type': "int",    'description': "genmatch (0 or 6: no match, jet, 1 or 3: electron, 2 or 4: muon, 5: real tau"},
      {'name': "syst",     'type': "string", 'description': "systematic 'nom', 'up', 'down'"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "category",
      'input': "genmatch",
      'keys': [1,2,5],
      'default': 1.0, # default TES if unrecognized genmatch
      'content': [
      
        # REAL TAU (genmatch==5)
        { 'nodetype': "category", # DM
          'input': "dm",
          'keys': dms,
          'default': 1.0, # default TES if unrecognized DM
          'content': [
            { 'nodetype': "category", # syst
              'input': "syst",
              'keys': ["nom","unc"],
              'content': [
                tes[dm], # central value (pt-independent)
                { 'parser': 'TFormula', # uncertainty (pt-dependent)
                  'expression': maketesunc(*tesuncs[dm]),
                  'parameters': [2], # pt
                },
              ],
            } for dm in dms
          ],
        },
        
        # E -> TAU FAKE (genmatch==1,3)
        { 'nodetype': "category", # DM
          'input': "dm",
          'keys': fesdms,
          'default': 1.0, # default FES
          'content': [
            { 'nodetype': "category", # syst
              'input': "syst",
              'keys': ["nom","up","down"],
              'content': [
                { # nominal
                  'nodetype': "binning", # eta
                  'input': "abseta",
                  'edges': etabins,
                  'content': fesuncs[dm],
                },
                { # up
                  'nodetype': "binning",
                  'input': "abseta",
                  'edges': etabins,
                  'content': fesuncs[dm],
                },
                { # down
                  'nodetype': "binning",
                  'input': "abseta",
                  'edges': etabins,
                  'content': fesuncs[dm],
                },
              ],
            } for dm in fesdms
          ],
        },
        
        # MU -> TAU FAKE (genmatch==2,4)
        { 'nodetype': "category", # syst
          'input': "syst",
          'keys': ["nom","unc"],
          'content': [
            1.00, # nominal
            0.01, # uncertainty (constant)
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
  
  

if __name__ == '__main__':
  tes()
  print()

