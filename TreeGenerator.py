
import dendropy
from ML.treeClassifier import getClass

def PureKingmanTreeConstructor(amount,pop_size=1,minimum=0.1,maximum=1):
    """
    Generates trees under the unconstrained Kingman’s coalescent process.

    amount: amount of trees to Create
    pop_size: some parameter of dendropy's pure_kingman_tree function
    minimum: minimum tolerable branch length
    maximum: maximum tolerable branch length

    Output: A set of tree strings
    """
    TaxonNamespace = dendropy.TaxonNamespace(["A","B","C","D"])
    #Gemerate trees
    trees = set()
    while len(trees) < amount:
        tree = dendropy.simulate.treesim.pure_kingman_tree(TaxonNamespace,pop_size)
        #if getClass(str(tree)) == 0:
        #Remove if tree has too short branch Length
        invalid = False
        for edge in tree.edges():
            if (edge.length < minimum and edge.length != 0) or (edge.length > maximum):
                invalid = True
                break
        if not invalid:
            trees.add(tree)
    return trees

def newickToStructure(newickTree):
    (a,b,c) = tuple(newickTree.coalescence_intervals()[4:])
    return f"-I 4 1 1 1 1 -n 2 1.0 -n 3 1.0 -n 1 1.0 -n 4 1.0 -ej {a} 1 2 -en {a} 2 {b} -ej {b} 2 3 -en {b} 3 {b} -ej {c} 3 4 -en {c} 4 {b}"

def generate(amount):
    """
    Inputs: amount of trees
    Output: a set of alpha tree structures
    """
    return [newickToStructure(tree) for tree in PureKingmanTreeConstructor(amount)]

# def generateStructure(x,y,z):
#     a = z
#     b = z + y
#     c = z + y + x
#     return f"-I 4 1 1 1 1 -n 2 1.0 -n 3 1.0 -n 1 1.0 -n 4 1.0 -ej {a} 1 2 -en {a} 2 {b} -ej {b} 2 3 -en {b} 3 {b} -ej {c} 3 4 -en {c} 4 {b}"
#
# structures = {
#     #'XinhaoTree': "-I 4 1 1 1 1 -n 2 1.0 -n 3 1.0 -n 1 1.0 -n 4 1.0 -ej {2.5} 1 2 -en 2.5 2 4.0 -ej {4.0} 2 3 -en 4.0 3 4.0 -ej {11.25} 3 4 -en 11.25 4 4.0",
#     'O': generateStructure(2.5,1.5,7.25),
#     'A': generateStructure(1.0,1.0,7.25),
#     'B': generateStructure(.5,.5,7.25),
#     'C': generateStructure(.15,.5,7.25),
#     'D': generateStructure(.15,.15,7.25),
#     'E': generateStructure(.1,.1,7.25)
# }
