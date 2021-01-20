#! /usr/bin/env python3
# Author: Izaak Neutelings (January 2021)
# https://github.com/nsmith-/correctionlib/blob/master/convert.ipynb
# https://github.com/cms-tau-pog/TauIDSFs/blob/master/utils/createSFFiles.py
import sys; sys.path.append('..')
assert sys.version_info>=(3,8),"Python version must be newer than 3.8, currently %s.%s"%(sys.version_info[:2])
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
    'name':    "test_1D",
    'inputs': [
      {'name': "eta", 'type': "real", 'description': "tau eta"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "binning",
      'input': "eta",
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
    'name':    "test_2D",
    'inputs': [
      {'name': "eta", 'type': "real", 'description': "tau eta"},
      {'name': "pt",  'type': "real", 'description': "tau pt"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "multibinning",
      'inputs': ["eta","pt"],
      'edges': [ xbins, ybins ],
      'content': sfs2,
    },
  })
  print(corr2)
  
  # CREATE & WRITE category
  print("\n>>> category SFs")
  keys = [0,1,2]
  sfs3 = [float(s) for s in range(len(keys))]
  corr3 = Correction.parse_obj({
    'version': 0,
    'name':    "test_category",
    'inputs': [
      {'name': "dm", 'type': "int", 'description': "decay mode"},
    ],
    'output': {'name': "weight", 'type': "real"},
    'data': {
      'nodetype': "category",
      'input': "dm",
      'keys': keys,
      'default': 1.,
      'content': sfs3,
    },
  })
  print(corr3)
  
  # WRITING
  print("\n>>> Writing...")
  set = CorrectionSet.parse_obj({
    'schema_version': 1,
    'corrections': [corr1,corr2,corr3,]
  })
  for fname, data in [("../data/tau/tau_test1.json",corr1),
                      ("../data/tau/tau_test2.json",corr2),
                      ("../data/tau/tau_test3.json",corr3),
                      ("../data/tau/tau_test.json",set)]:
    print(">>>  ",fname)
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
  
