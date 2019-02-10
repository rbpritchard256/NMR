from Dict import resDict

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
        for r in self.seq:
            self.Residues.append(Residue(resDict[r],c,{}))
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
        print('WARNING: Residue.addAtoms has an issue if there are any unassigned CSs')
        self.Residues[val].addAtom(a)

    def countAtoms(self): 
        # counts all assigned atoms in the molecule
        c = 0
        for r in self.Residues:
             for a in r.Atoms:
                 c += 1
        print('There are {} chemical shifts.'.format(c))

class Residue:
    def __init__(self, name, num=-1, Atoms={}):
        self.name = name
        self.num = num
        self.Atoms= Atoms

    def describe(self):
        print('Name: {}'.format(self.name))
        print('Number: {}'.format(self.num))

    def listAtoms(self):
        for a in self.Atoms:
           self.Atoms[a].describe()

    def addAtom(self, a):
        self.Atoms[a.name] = a

class Atom:
    def __init__(self, name, atype, CS, CS_var=(float('NaN'),float('NaN'))):
        self.name = name
        self.atype = atype
        self.CS = CS
        self.CS_var = CS_var  # not played with this yet

    def describe(self):
        print('\t{}\t {}'.format(self.name, self.CS))
