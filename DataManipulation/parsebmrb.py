#!/usr/bin/python3

from statemachine import StateMachine
import os,sys, argparse
from Classes import *

def start(f): 
    # Tests the state of the file 
    print(f'\n\n     STARTING to read {f} \n--------------------------------------------------------------------------------\nNOTE: This program currently doesn\'t take account of duplicate CS recordings for\n      a single atom\n--------------------------------------------------------------------------------')
    newstate = 'tmp'
    try:
        if os.stat(f).st_size == 0:
            newstate = "empty_file"
        elif os.stat(f).st_size != 0:
            newstate = "open_file"
        else:
            sys.exit('Error: This should not be possible')
    except OSError:
        newstate = "no_file"
    if newstate == 'tmp': #really shouldn't happen
        sys.exit('Error: Something is wrong in parsebmrb.start(f). Should have overwritten newstate = \'tmp\'')
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

        if '_Assembly.Number_of_components' in line: # check only one molecule in file
            print(line.split()[1] )
            if line.split()[1] == '.': # this is sometimes used instead of 1, currently assuming they are equal
                pass
            elif int(line.split()[1]) > 1:
                sys.exit('Error: two molecules in this file. Currently can\'t handle that')
            
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
    print('WARNING: Residue.addAtoms has an issue if there are any unassigned CSs\n--------------------------------------------------------------------------------')
    molecule.initialise() # create a list of residue objects for each residue in molecule.seq
    inCS,firstLine = True, True
    id_rNum = headers.index('_Atom_chem_shift.Seq_ID')
    id_rName = headers.index('_Atom_chem_shift.Comp_ID')
    id_aName = headers.index('_Atom_chem_shift.Atom_ID')
    id_aType = headers.index('_Atom_chem_shift.Atom_type')
    id_CS = headers.index('_Atom_chem_shift.Val')
    authResNum = headers.index('_Atom_chem_shift.Auth_seq_ID')
    rNum_old = -9999
    for line in fi:
        if line.strip() == 'stop_':
            inCS = False
            break
        if inCS == True:
            tokens=line.split()
            if len(tokens) != len(headers):
                sys.exit(f'Error: There is an issue in the CS data, fewer entries than tokens for line: {line}')
            rNum, rName = int(tokens[id_rNum]), tokens[id_rName]
            aName, aType, CS = tokens[id_aName], tokens[id_aType], float(tokens[id_CS])
            if molecule.Residues[rNum].name != rName:
                sys.exit(f'Error: There is a discrepency between residue number in the CS list and the residue type in the 3-letter sequence in line:\n{line}')
            if firstLine == True:
                rNum_old = rNum
                molecule.Residues[rNum].realNum = tokens[authResNum]
                a = Atom(aName, aType, CS)
                molecule.Residues[rNum].addAtom(a)
                firstLine = False
            elif rNum != rNum_old:
                molecule.Residues[rNum].realNum = tokens[authResNum]
                a = Atom(aName, aType, CS)
                molecule.Residues[rNum].addAtom(a)
                rNum_old = rNum
            else:
                a = Atom(aName, aType, CS)
                molecule.Residues[rNum].addAtom(a)

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
    if molecule.seq != '':
        sys.exit('Error: two sequences given file. Currently can\'t handle that')
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Input BMRB file (NMRStar 3.1 only)', action='store', dest='filename')
    args = parser.parse_args()
    f = args.filename

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
    a.describe()
