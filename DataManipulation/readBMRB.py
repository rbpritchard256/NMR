#!/usr/bin/python

import sys




def readBMRB(f, checkFile):
  '''
  Reads the BMRB file and returns data = {('1',[Met]'):{'N': 117, 'Ca':60 }, ...}.
  Only orders the ones I've thought of and the rest get added at the end. 
  '''
  with open(f,'r') as fi: 
    for line in fi:
      
  getCS(f, checkFile)
  return data

def getCS(f,checkFile):
  data = {}
  c = 0

      c +=1
      tokens = line.split()
      if checkFile != False:
        if len(tokens) != 24:
          sys.exit('\nBMRB file in wrong format (sorry!).\nExited at line {} which does not 24 words.'.format(c))
      res = tokens[4]
      resname = tokens[6]
      atom = tokens[7]
      val = float(tokens[10])
      if (res,resname) not in data:
        data[(res, resname)] = {}
        data[(res, resname)][atom] = val
      else:
        data[(res, resname)][atom] = val
  return data

def parseBMRB(data):
    line = ''
    line = line+f[0]+'\t' # res number
    line = line+f[1]+'\t' # res name 
    track = []
    List = ['N', 'NE', 'NZ', 'C', 'CA', 'CB', 'CG', 'CD', 'CE', 'CZ', 'CN', 'H', 'HA', 'HB', 'HB1', 'HB2']  
    for atom in List:
      val, track = getVal(atom,data[f])
    print(line, aval, track)

def getVal(atom, res):
  val, track = '', False 
  if atom in res:
    val = str(res[atom])
    track =  True
  return val, track


File = 'bmrb_26012'
checkFile = True
data = readBMRB(File, checkFile)




for l in data:
    print(l, data[l]) 


