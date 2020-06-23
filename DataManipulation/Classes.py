from Dict import resDict_1to3
import sys

class Molecule:
    """
    Class object for Molecules
        self
        name        molecule name                                 str 
        numRes      number of residues (this construct)           int 
        seq         sequence (this construct)                     str
        Residues	Residue object for each residue in seq        array
        uniProtCode UniProt code for the full protein             str
        seqNote     Any other notes for this sequence/construct   str                    
    """

    def __init__(self, name='', numRes=0, seq='', Residues=[], uniProtCode='', seqNote='', pAssigned=0.0):
        self.name = str(name)
        self.numRes = int(numRes)
        self.seq = seq
        self.Residues = Residues
        self.uniProtCode = str(uniProtCode)
        self.seqNote = str(seqNote)
#        self.pAssigned = pAssigned # not played with this yet

    def describe(self):
        """
        Describes the molecule (name, number of resiudes, any notes, sequence)
        """
        print(f'\n{self.name}\n\tNumRes: {self.numRes}\n\tSequence note: {self.seqNote}\n\tSequence: {self.seq}')

    def initialise(self):
        """
        Creates a Residue object for every residue in the sequence of *this* construct (self.seq)
        Discrepencies with the full protein numbering (artefacts, fragments) are handled at the resiude level.
        """
        c = 1						
        for r in self.seq:
            self.Residues.append(Residue(resDict_1to3[r],c,-1,{}))
            c += 1

    def listAtoms(self): 
        """
        Lists all the atoms in the molecule  
        """
        for r in self.Residues:
            r.describe()
            r.listAtoms()

#    def countAtoms(self): 
#        # counts all assigned atoms in the molecule
#        c = 0
#        for r in self.Residues:
#             for a in r.Atoms:
#                 c += 1
#        print('There are {} chemical shifts.'.format(c))

class Residue:
    """
    Class object for residues
        self
        name        residue name                      str 
        num         residue number                    int 
        realNum     real residue number (authSeqID)   int
                      should be the number from the full UniProt sequence
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

    def addAtom(self, a):
        """
        Adds an atom object to the dictionary of atoms in a Residue
        """
        self.Atoms[a.name] = a    


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
    """

    def __init__(self, name, atype, CS):
        self.name = name
        self.atype = atype
        self.CS = CS

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










