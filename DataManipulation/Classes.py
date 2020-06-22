from Dict import resDict
import sys

class Molecule:
    def __init__(self, name='', numRes=0, seq='', Residues=[], seqNote='', pAssigned=0.0):
        self.name = name
        self.numRes = numRes
        self.seq = seq
        self.Residues = Residues
        self.seqNote = seqNote
        self.pAssigned = pAssigned # not played with this yet

    def describe(self):
        print('Name: {}'.format(self.name))
        print('Number of residues: {}'.format(self.numRes))
        print('Sequence note: {}'.format(self.seqNote))
        print('Sequence:\n{}'.format(self.seq))

    def initialise(self):
        c = 1						
		# Here residue numbering is simply in *this* seq, 
		# discrepencies with uniprot handled elsewhere
        for r in self.seq:
            self.Residues.append(Residue(resDict_1to3[r],c,{}))
            c += 1

    def listAtoms(self): 
        for r in self.Residues:
            print('{} {}'.format(r.name, r.num))
            if len(r.Atoms) >0:
                for a in r.Atoms:
                    r.Atoms[a].describe()
            else:
                pass
#                print('\tNone')

    def addAtom(self, a, val):
        # Adds Atom objects to a residue defined by its number in the sequence (val)
        self.Residues[val].addAtom(a)

    def countAtoms(self): 
        # counts all assigned atoms in the molecule
        c = 0
        for r in self.Residues:
             for a in r.Atoms:
                 c += 1
        print('There are {} chemical shifts.'.format(c))

class Residue:
    """
    Class object for residues
        self
        name        residue name                      str 
        num         residue number                    int 
        realNum     real residue number (authSeqID)   int
                      accounts for fragment nature / cloning artifacts
        Atoms       atom objects for this residue     dict
                    
    """

    def __init__(self, name, num=-1, realNum=-1, Atoms={}):
        self.name = str(name)
        self.num = int(num)
        self.realNum = int(realNum)
        self.Atoms= Atoms

    def describe(self):
        """
        Prints residue name, number and real number to screen
        """
        print(f'Residue: {self.name:5} {self.num:5} ({self.realNum} in full protein)')

    def listAtoms(self):
        """
        Lists the atom in the residue (giving name and CS)
        """
        for a in self.Atoms:
           self.Atoms[a].describe()

#    def addAtom(self, a):
#        """
#        Lists the atom in the residue (giving name and CS)
#        """
#        self.Atoms[a.name] = a    


#    def checkExists(self, atoms):
#        result = False
#        if len(self.Atoms) >0:
#            if set(atoms).issubset(self.Atoms.keys()):
#                result = True
#        return result


class Atom:
    """
    Class object for atoms
        self
        name        specific atom name          str 
                      eg C, CA, HG11
        atype       atom type                   str 
                      eg C, H, O
        CS          chemical shift              float
                !!!   currently no note of referencing, CH/CD etc 
        ( CS_var    chemical shift variation    tuple of floats )
                !!!   Not yet implemented
    """

    def __init__(self, name, atype, CS, CS_var=(float('NaN'),float('NaN'))):
        self.name = name
        self.atype = atype
        self.CS = CS
        self.CS_var = CS_var  # not played with this yet

    def describe(self):
        """
        Prints atom details (name and CS) to screen
        """
        print('\t{}\t {}'.format(self.name, self.CS))


class Correlation: 
    def __init__(self, res1, res2, num1, num2, atype1, atype2, val1, val2):
        self.res1 = res1
        self.res2 = res2
        self.num1 = num1
        self.num2 = num2
        self.atype1 = atype1
        self.atype2 = atype2
        self.val1 = val1
        self.val2 = val2










