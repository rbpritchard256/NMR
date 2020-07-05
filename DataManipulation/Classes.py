from Dict import resDict_1to3
import sys

class Molecule:
    """
    Class object for Molecules
        self
        name        molecule name                                 str 
        numRes      number of residues (this construct)           int 
        seq         sequence (this construct)                     str
        Residues	Residue object for each residue in seq        dict
        uniProtCode UniProt code for the full protein             str
        seqNote     Any other notes for this sequence/construct   str                    
    """

    #TO DO write internal checks for seq/numRes/Residues etc to be consistent

    def __init__(self, name=None, numRes=0, seq=None, Residues=None, uniProtCode='', seqNote=''):
        self.name = str(name)
        self.numRes = int(numRes)
        self.seq = seq
        if Residues:
          self.Residues = Residues
        else:
          self.Residues = {}
        self.uniProtCode = str(uniProtCode)
        if seq:
          self.seq = seq
        else:
          self.seq = ''
        self.seqNote = str(seqNote)
        if self.numRes == 0 and self.seq != '':
            self.numRes = len(self.seq)
        if self.numRes != len(self.seq) and self.seq != '':
            sys.exit(f'Error: number of residues doesn\'t match the sequence')

    def describe(self):
        """
        Describes the molecule (name, number of resiudes, any notes, sequence)
        """
        print(f'{self.name}\n\tNumRes: {self.numRes}\n\tSequence note: {self.seqNote}\n\tSequence: {self.seq}')

    def initialise(self):
        """
        Creates a Residue object for every residue in the sequence of *this* construct (self.seq)
        Discrepencies with the full protein numbering (artefacts, fragments) are handled at the resiude level.
        """
        c = 1
        for r in self.seq:
            self.Residues[c] = Residue(resDict_1to3[r],c,'',{})
            c += 1

    def listResidues(self): 
        """
        Lists all the residues in the molecule  
        """
        for r in self.Residues:
            res = self.Residues[r]
            print(f'{res.num:^5}({res.realNum:^5}){res.name:^8}{len(res.Atoms)} atoms')

    def listAtoms(self): 
        """
        Lists all the atoms in the molecule  
        """
        for r in self.Residues:
            self.Residues[r].describe()
            self.Residues[r].listAtoms()

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
        realNum     real residue number (authSeqID)   str
                      should be the number from the full UniProt sequence
                      accounts for fragment nature / cloning artifacts
                      Can be possibly '.' / 'NaN' / negative
        Atoms       atom objects for this residue     dict
                    
    """

    def __init__(self, name, num, realNum=None, Atoms=None):
        self.name = str(name)
        self.num = int(num)
        if realNum:
          self.realNum = realNum
        else:
          self.realNum = None
        if Atoms:
          self.Residues = Atoms
        else:
          self.Atoms = {}

    def describe(self):
        """
        Prints residue name, number and real number to screen
        """
        rNum = ''
        try:
            int(self.realNum)
            rNum = self.realNum
        except ValueError:
            if len(self.Atoms) > 0:
                rNum = '-'
            else:
                rNum = ''
        print(f'Residue: {self.name:5} {self.num:5} (RealSeqID: {rNum})')

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
        name        specific atom name                      str 
                      eg C, CA, HG11
        atype       atom type                               str 
                      eg C, H, O 
        CS          assigned / average chemical shift       float
                !!!   currently no note of referencing, CH/CD etc 
        var         variation in CS                         float
        CSlist      chemical shift                          tuple
    """

    def __init__(self, name, atype, CS=-1, var=-1, CSlist=None):
        self.name = name
        self.atype = atype
        self.CS = CS
        self.var = var
        if CSlist:
          self.CSlist = CSlist
        else:
          self.CSlist = []

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





