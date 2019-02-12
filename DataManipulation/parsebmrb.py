#!/usr/bin/python3

from statemachine import StateMachine
import os,sys
from Classes import *

def start(f): 
    # Tests the state of the file 
    print('--------------------------------------------------------------------------------\nNOTE: This program currently takes *no* account of duplicate CS recordings\n      for a single atom\n--------------------------------------------------------------------------------')
    newstate = 'tmp'
    try:
        if os.stat(f).st_size == 0:
            newstate = "empty_file"
        elif os.stat(f).st_size != 0:
            newstate = "open_file"
        else:
            sys.exit('This should not happen')
    except OSError:
        newstate = "no_file"
    if newstate == 'tmp': #really shouldn't happen
        sys.exit('PersonalError: what on earth have you done!')
    return (newstate, f)

def open_file(f):
    fi = open(f, 'r')
    molecule = Molecule()
    return ('read_lines', (f, fi, molecule))

def read_lines(cargo):
    '''
    Goes through the file and directs to various functions depending on text/position in file.
    Extracts information to Molecule class object containing Residues and which contain Atoms
    '''
    f, fi, molecule = cargo[0], cargo[1], cargo[2]
    r = ('end_reading', (f, fi,molecule))
    for line in fi:
        if 'NMR_STAR_version' in line: # check version, currently only supports 3.1
            line = next(fi) # currently skips the detailed version
            version = get_info(line)
            if version != '3.1':
                print("Closing.\nFile: '{}' is not NMR STAR version 3.1".format(f))
                quit()
        if '_Entity.Name' in line: # get molecule name
            molecule.name = get_info(line)
        if line.strip() == '_Entity.Polymer_seq_one_letter_code': # get sequence
            next(fi)
            r = ('get_sequence', (f, fi, molecule))
            break
        if '_Entity.Polymer_author_seq_details' in line: # get any sequence notes
            molecule.seqNote = get_info(line)
        if line.strip() == '_Atom_chem_shift.Assigned_chem_shift_list_ID': # get CS
            next(fi)
            r = ('get_CS', (f, fi, molecule))
            break
    return r

def get_sequence(cargo): 
    # Imports the *single letter* sequence
    f, fi, molecule = cargo[0], cargo[1], cargo[2]
    seq, inseq = '', True
    for line in fi:
        if line.strip() == ';':
            inseq = False
        if inseq == True:
            seq = seq+line.strip()
        else:
            break
    molecule.seq = seq
    molecule.numRes= len(seq.strip())
    return ('read_lines',(f, fi, molecule))
        
def get_CS(cargo): 
    # Gets the CS for each atom
    f, fi, molecule = cargo[0], cargo[1], cargo[2]
    print('WARNING: Residue.addAtoms has an issue if there are any unassigned CSs')
    molecule.initialise() # create a list of residue objects, one for each residue in molecule.seq
    inCS = True
    c = 0
    for line in fi:
        if line.strip() == 'stop_':
            inCS = False
            break
        if inCS == True:
            tokens = line.split()
            val = int(tokens[4])-1
            a = Atom(tokens[7],tokens[8],float(tokens[10]))
            molecule.addAtom(a, val)
        else:
            break
    return ('read_lines',(f, fi, molecule))


def get_info(line):
    tokens = line.split()
    if len(tokens) > 1:
        info = ' '.join(tokens[1:])
    elif len(tokens) <= 1:
        print('Closing. \n Not enough tokens for information - there is an issue in the code here, go fix it')
    return info


def end_reading(cargo):
    f, fi, molecule = cargo[0], cargo[1], cargo[2]
    print("Finished reading file: '{}'".format(f))
    return ('', (f,fi,molecule))

def empty_file(f):
    print("Closing.\nFile: '{}' is empty".format(f))
    quit()

def no_file(f):
    print("CLOSING: File: '{}' does not exist".format(f))
    quit()

def parseBMRB(f): 
    # This is the actual program
    m = StateMachine()
    m.add_state("Start", start)
    m.add_state("open_file", open_file)
    m.add_state("read_lines", read_lines)
    m.add_state("get_sequence", get_sequence)
    m.add_state("get_CS", get_CS)
    m.add_state("end_reading", end_reading, end_state=1)
    m.add_state("empty_file", empty_file)
    m.add_state("no_file", no_file)
    m.set_start("Start")
    a = m.run(f)[2]
    return a


if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", start)
    m.add_state("open_file", open_file)
    m.add_state("read_lines", read_lines)
    m.add_state("get_sequence", get_sequence)
    m.add_state("get_CS", get_CS)
    m.add_state("end_reading", end_reading, end_state=1)
    m.add_state("empty_file", empty_file)
    m.add_state("no_file", no_file)
    m.set_start("Start")
    a = m.run('26012_3.1')[2]
    a.describe()
