#! /usr/bin/env python3
# Author: Izaak Neutelings (January 2021)
# https://github.com/nsmith-/correctionlib/blob/master/convert.ipynb
# https://github.com/cms-tau-pog/TauIDSFs/blob/master/utils/createSFFiles.py
import sys; sys.path.append('..')
from correctionlib.schemav1 import Correction, CorrectionSet
import json, jsonschema

# SIMPLE TEST
def test():
  
  # CREATE & WRITE 1D
  print(">>> 1D SFs")
  xbins = [0.0,1.1,2.5]
  nsfs  = len(xbins)-1
  sfs   = [float(s) for s in range(nsfs)]
  print(xbins,sfs)
  corr1 = Correction.parse_obj({
    'version': 0,
    'name':    "test",
    'inputs': [
      {'name': "eta", 'type': "real", 'description': "tau eta"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "binning",
      'edges': xbins,
      'content': sfs,
    },
  })
  print(corr1)
  print(corr1.data.content)
  #help(corr1)
  
  # CREATE & WRITE 2D
  print("\n>>> 2D SFs")
  xbins = [0.0,1.1,2.5]
  ybins = [20.0,50.0,100.0]
  nsfs2 = (len(xbins)-1)*(len(ybins)-1)
  sfs2  = [float(s) for s in range(nsfs2)]
  print(xbins,ybins,sfs)
  corr2 = Correction.parse_obj({
    'version': 0,
    'name':    "test",
    'inputs': [
      {'name': "eta", 'type': "real", 'description': "tau eta"},
      {'name': "pt",  'type': "real", 'description': "tau pt"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "multibinning",
      'edges': [ xbins, ybins ],
      'content': sfs2,
    },
  })
  print(corr2)
  
  # WRITING
  set = CorrectionSet.parse_obj({
    'schema_version': 1,
    'corrections': [corr1,corr2,]
  })
  for fname, data in [("../data/tau/tau_test1.json",corr1),
                      ("../data/tau/tau_test2.json",corr2),
                      ("../data/tau/tau_test.json",set)]:
    print(f">>> Writing {fname}...")
    with open(fname,'w') as fout:
      fout.write(data.json(exclude_unset=True,indent=2))
  
  ## READ & VALIDATE
  #with open("tau_test.json") as fin:
  #  data = json.load(fin)
  #  jsonschema.validate(data,CorrectionSet.schema())
  

if __name__ == '__main__':
  print()
  test()
  print()
  
