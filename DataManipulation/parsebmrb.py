#!/usr/bin/python3

from statemachine import StateMachine
import os,sys
from Classes import *

def start(f): 
    # Tests the state of the file 
    print('--------------------------------------------------------------------------------\nNOTE: This program currently takes *not* account of duplicate CS recordings\n      for a single atom\n--------------------------------------------------------------------------------')
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
        sys.exit('Something is wrong in parsebmrb.start(f). Should have overwritten newstate = \'tmp\'')
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

        if line.strip() == 'loop_': # indicates the start of a set of headers
            r = ('get_headers', (f, fi, molecule))
            break

        if '_Entity.Name' in line: # get molecule name
            molecule.name = get_info(line)
        if line.strip() == '_Entity.Polymer_seq_one_letter_code': # get sequence
            next(fi)
            r = ('get_sequence', (f, fi, molecule))
            break
        if '_Entity.Polymer_author_seq_details' in line: # get any sequence notes
            molecule.seqNote = get_info(line)
    return r

def get_headers(cargo):
    # Extracts data headers (list after '_loop' in star 3.1)
    f, fi, molecule = cargo[0], cargo[1], cargo[2]
    headers = []
    for line in fi:
        if line.strip() != '':
            headers.append(line.strip())
        else:
            break
    if headers[-1] == '_Atom_chem_shift.Assigned_chem_shift_list_ID': # get the chemical shift
        r = ('get_CS',(f, fi, molecule, headers))
    elif headers[-1] == '_Entity_db_link.Entity_ID': # get the uniProt number
        r = ('get_uniProt', (f, fi, molecule, headers))
    else:
        r = ('read_lines',(f, fi, molecule))
    return r
        
def get_CS(cargo): 
    # Gets the CS for each atom
    f, fi, molecule, headers = cargo[0], cargo[1], cargo[2], cargo[3]
    print('WARNING: Residue.addAtoms has an issue if there are any unassigned CSs')
    molecule.initialise() # create a list of residue objects for each residue in molecule.seq
    inCS = True
    id_rNum = headers.index('_Atom_chem_shift.Seq_ID')
    id_aName = headers.index('_Atom_chem_shift.Atom_ID')
    id_aType = headers.index('_Atom_chem_shift.Atom_type')
    id_CS = headers.index('_Atom_chem_shift.Val')
    authResNum = headers.index('_Atom_chem_shift.Auth_seq_ID')
    id_rNum_old = ''
    for line in fi:
        if line.strip() == 'stop_':
            inCS = False
            break
        if inCS == True:
            tokens=line.split()
            if id_rNum != id_rNum_old:
               molecule.Residues[int(tokens[id_rNum])-1].realNum = int(tokens[authResNum])
            resNum = int(tokens[id_rNum])-1
            a = Atom(tokens[id_aName],tokens[id_aType],float(tokens[id_CS]))
            molecule.Residues[id_rNum].addAtom(a)
        else:
            break
    return ('read_lines',(f, fi, molecule))

def get_uniProt(cargo):
    # Extracts the uniprot code for the molecule
    f, fi, molecule, headers = cargo[0], cargo[1], cargo[2], cargo[3]
    i_db = headers.index('_Entity_db_link.Database_code')
    i_code = headers.index('_Entity_db_link.Accession_code')
    tokens = next(fi).split()
    if tokens[i_db] == 'UNP':
        molecule.uniProtCode = tokens[i_code]
    else:
        print(f'There is no Uniprot number for this construct\n{tokens[i_db]} database used instead')
        molecule.uniProtCode = 'not uniProt'
    return ('read_lines',(f, fi, molecule))


def get_info(line):
    # Returns the value for line with format _header     value
    tokens = line.split()
    if len(tokens) > 1:
        info = ' '.join(tokens[1:])
    elif len(tokens) <= 1:
        print('Closing. \n Not enough tokens for information - there is an issue in the code here, go fix it')
    return info


def get_sequence(cargo): 
    # Imports the *single letter* sequence of this construct (spans several lines)
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
    m.add_state("get_headers", get_headers)
    m.add_state("get_uniProt", get_uniProt)
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
    m.add_state("get_headers", get_headers)
    m.add_state("get_uniProt", get_uniProt)
    m.add_state("end_reading", end_reading, end_state=1)
    m.add_state("empty_file", empty_file)
    m.add_state("no_file", no_file)
    m.set_start("Start")
    a = m.run('26012_3.1')[2]
    a.describe()
