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
# f = TFormula('f',sf)
# for x in [10,20,29,30,31,35,45,100,200,499,500,501,750,999,1000,1001,1500,2000]: x, f.Eval(x)

def tid():
  """Tau ID SF"""
  print("\n>>> tau ID SF")
  fname   = "../data/tau/tau_tid.json"
  ptbins  = [0.,34.,170.]
  dms     = [0,1,10] #,11
  wps     = ['Tight'] #'Loose','Medium','Tight']
  sf      = "x<20?0: x<25?1.00: x<30?1.01: x<35?1.02: x<40?1.03: 1.04"
  sfup    = "x<20?0: x<25?1.10: x<30?1.11: x<35?1.12: x<40?1.13: x<500?1.14: x<1000?1.04+0.2*x/500.: 1.44"
  sfdn    = "x<20?0: x<25?0.90: x<30?0.91: x<35?0.92: x<40?0.93: x<500?0.94: x<1000?1.04-0.2*x/500.: 0.64"
  ptsfs   = {wp: {'nom':sf, 'up':sfup, 'down':sfdn} for wp in wps}
  corr1   = Correction.parse_obj({
    'version': 0,
    'name':    "DeepTau2017v2p1VSjet_test",
    'inputs': [
      {'name': "pt",       'type': "real",   'description': "tau pt"},
      {'name': "dm",       'type': "int",    'description': "tau decay mode (0, 1, 10, or 11)"},
      #{'name': "genmatch", 'type': "int",    'description': "genmatch (0 or 6: no match, jet, 1 or 3: electron, 2 or 4: muon, 5: real tau"},
      {'name': "wp",       'type': "string", 'description': "DeepTauVSjet WP: VVVLoose-VVTight"},
      {'name': "syst",     'type': "string", 'description': "systematic 'nom', 'up', 'down'"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': 'category',
      'input': "wp",
      'keys': wps,
      'default': 1.0, # default TES if unrecognized genmatch
      'content': [
      
        # REAL TAU (genmatch==5)
        { 'nodetype': 'category', # syst
          'input': "syst",
          'keys': ['nom','up','down'],
          'content': [
            {  # central (pt-dependent)
              'parser': 'TFormula',
              'expression': ptsfs[wp]['nom'],
              'parameters': [1], # pt
            },
            { # up (pt-dependent)
              'parser': 'TFormula',
              'expression': ptsfs[wp]['up'],
              'parameters': [1], # pt
            },
            { # down (pt-dependent)
              'parser': 'TFormula',
              'expression': ptsfs[wp]['down'],
              'parameters': [1], # pt
            },
          ],
        } for wp in wps
        
      ],
    },
  })
  print(corr1)
  print(corr1.data.content)
  print(f">>> Writing {fname}...")
  with open(fname,'w') as fout:
    fout.write(corr1.json(exclude_unset=True,indent=2))
  
  

if __name__ == '__main__':
  tid()
  print()

