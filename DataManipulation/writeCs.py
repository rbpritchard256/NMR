#!/usr/bin/python3
import parsebmrb
import argparse, sys
import Dict
from Classes import *

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', type=str, help='Input BMRB file (NMRStar 3.1 only)', action='store', dest='filename')
parser.add_argument('-o', '--output', type=str, help='Select which peaks list to output HN, HC, MeTROSY', action='store', dest='output')
args = parser.parse_args()

f = args.filename
o = args.output
if o not in ['HNbb','HNall', 'HC', 'MeTROSY']:
    sys.exit('CLOSING: Output (-o/--output) must be one of HN, HC, MeTROSY')

def HNbb_peaks(molecule):
    peakList=[]
    for res in molecule.Residues:
        if 'N' in res.Atoms and 'H' in res.Atoms:
            corr = Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'H', 'N', float(res.Atoms['H'].CS), float(res.Atoms['N'].CS))
            peakList.append(corr)
    return peakList

def MeTROSY_peaks(molecule):
    peakList=[]
    for res in molecule.Residues:
        if res.name == 'ILE':
            if res.checkExists(['CD1','HD11','HD12','HD13']):
                if res.Atoms['HD11'].CS ==  res.Atoms['HD12'].CS ==res.Atoms['HD13'].CS:
                    peakList.append(Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'HD*', 'CD1', float(res.Atoms['HD11'].CS), float(res.Atoms['CD1'].CS)))
        if res.name == 'LEU':
            if res.checkExists(['CD1','HD11','HD12','HD13']):
                if res.Atoms['HD11'].CS ==  res.Atoms['HD12'].CS ==res.Atoms['HD13'].CS:
                    peakList.append(Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'HD1*', 'CD1', float(res.Atoms['HD11'].CS), float(res.Atoms['CD1'].CS)))
            if res.checkExists(['CD2','HD21','HD22','HD23']):
                if res.Atoms['HD21'].CS ==  res.Atoms['HD22'].CS ==res.Atoms['HD23'].CS:
                    peakList.append(Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'HD2*', 'CD2', float(res.Atoms['HD21'].CS), float(res.Atoms['CD2'].CS)))
        if res.name == 'VAL':
            if res.checkExists(['CG1','HG11','HG12','HG13']):
                if res.Atoms['HG11'].CS ==  res.Atoms['HG12'].CS ==res.Atoms['HG13'].CS:
                    peakList.append(Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'HG1*', 'CG1', float(res.Atoms['HG11'].CS), float(res.Atoms['CG2'].CS)))
            if res.checkExists(['CG2','HG21','HG22','HG23']):
                if res.Atoms['HG21'].CS ==  res.Atoms['HG22'].CS ==res.Atoms['HG23'].CS:
                    peakList.append(Correlation(Dict.resDictRev[res.name], Dict.resDictRev[res.name], res.num, res.num, 'HG2*', 'CG2', float(res.Atoms['HG21'].CS), float(res.Atoms['CG2'].CS)))
    return peakList


def writePeaks(molecule, peakList, o):
    n='\n'
    with open(f'{o}_{molecule.name}.peaks','w') as fo:
        fo.write('Assignment               w1          w2\n')
        for p in peakList:
            name = f'{p.res1}{p.num1}{p.atype1}-{p.res2}{p.num2}{p.atype2}'
            fo.write(f"{name:<20} {p.val1:10.3f} {p.val2:10.3f}{n}")
#input NH, meTROSY, HC

molecule = parsebmrb.parseBMRB(f)
peakList = MeTROSY_peaks(molecule)
writePeaks(molecule, peakList, o)


# extract based on HN
# extract based on HC
# extract based on NH

# write/save peak list in Sparky format





