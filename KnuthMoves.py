#!/usr/bin/env python
# coding: utf-8

# In[56]:


from multiprocessing import Pool
from sage.graphs.graph_input import from_dict_of_lists

def get_small_data(equivalence_class_representitive, show_equiv_class_list, show_graph):
    n = len(equivalence_class_representitive)
    g = Graph(generateData(n), weighted = True, loops=True)
    list_of_equiv_classes = g.connected_components()
    list_of_edges = generateData(n)
    for equiv_class in list_of_equiv_classes:
        if equivalence_class_representitive in equiv_class:
            found = equiv_class 
            if show_equiv_class_list:
                print("Equivalence Class Containing", equivalence_class_representitive,"is\n",str(found))
    if show_graph:
        display_edges = []
        for edge in list_of_edges:
            if edge[0] in found and edge[1] in found:
                display_edges.append(edge)
        g = Graph(display_edges, weighted = True, loops=True)
        fs = int(input("Enter desired figure size: "))
        print("======= Selected Graph Loading =======")
        g.show(edge_labels = True, figsize = fs, vertex_size=0, edge_color="#FF0000")
        
def get_big_data(n, show_equiv_class_list, show_graph):
    g = Graph(generateData(n), weighted = True, loops=True,multiedges=True)
    
    # this code is meant to combine multiple edges between permutations
    me = g.multiple_edges()
    i = 0
    while i < len(me):
        j = i + 1
        while me[j][0] == me[i][0] and me[j][1] == me[i][1]:
            j = j + 1
            if j > len(me) - 1:
                break
        t = me[i][2]
        flag = False
        for k in range(i + 1, j):
            if me[k][2] != t:
                flag = True
        g.delete_multiedge(me[i][0], me[i][1])
        if flag:
            g.add_edge(me[i][0], me[i][1], "both")
        else:
            g.add_edge(me[i][0], me[i][1], me[i][2])
        i = j
    #g.remove_loops()
    
    list_of_equiv_classes = g.connected_components()
    if show_equiv_class_list:
        print("======= Knuth/P-Tableau Equivalence Classes =======")
        print(list_of_equiv_classes)
        print("===================================================")
    if show_graph:
        print("There are", len(list_of_equiv_classes), "equivalence classes.")
        first_class = int(input("first equiv. class to graph? "))
        last_class = int(input("last equiv. class to graph? "))
        fs = int(input("Enter desired figure size: "))
        list_of_edges = g.edges()
        desired_equiv_classes = list_of_equiv_classes[first_class-1:last_class-1]
        desired_elts = []
        for elt in desired_equiv_classes:
            for subelt in elt:
                desired_elts.append(subelt)
        display_edges = []
        for edge in list_of_edges:
            if edge[0] in desired_elts and edge[1] in desired_elts:
                display_edges.append(edge)
        g = Graph(display_edges, weighted = True, loops=True)
        print("======= Selected Graph Loading =======")
        g.show(edge_labels = True, figsize = fs, vertex_size=0, edge_color="#FF0000")

def Knuth_Moves_From_Perm(perm):
    permL = list(perm)
    Done = False
    result = []
    for index in range(len(perm)-2):
        permL = list(perm)
        elt1 = perm[index]
        elt2 = perm[index+1]
        elt3 = perm[index+2]
        testMiniPerm = perm[index:index+3]
        if has_2_1_3(testMiniPerm):
            permL[index+1]=elt3
            permL[index+2]=elt2
            type = "K1"
            info = (Permutation(permL), type)
        elif has_2_3_1(testMiniPerm):
            permL[index+1]=elt3
            permL[index+2]=elt2
            type = "K1"
            info = (Permutation(permL), type)
        elif has_3_1_2(testMiniPerm):
            permL[index]=elt2
            permL[index+1]=elt1
            type = "K2"
            info = (Permutation(permL), type)
        elif has_1_3_2(testMiniPerm):
            permL[index]=elt2
            permL[index+1]=elt1
            type = "K2"
            info = (Permutation(permL), type)
        else:
            info = []
        if len(info) > 0:
            result.append(info)
    return result

def getOutWord(ls):
    result = ""
    for elt in ls:
        result +=str(elt)
    return result

def removeDuplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
def generateData(n):
    resultDict = {}
    permList = list(Permutations(n))
    for elt in permList:
        resultDict[elt] = Knuth_Moves_From_Perm(elt)
    edges = []
    for perm in resultDict:
        edgeDataSlice = [str(getOutWord(perm))]
        if len(resultDict[perm])>0:
            for dataPiece in resultDict[perm]:
                edgeDataSlice.append(str(getOutWord(dataPiece[0])))
                edgeDataSlice.append(str(getOutWord(dataPiece[1])))
                edges.append(tuple(edgeDataSlice))
                edgeDataSlice = [str(getOutWord(perm))]
        else:
            edges.append((str(getOutWord(perm)), str(getOutWord(perm))))
    return edges

def has_2_1_3(perm):
    if perm[1]<perm[0]<perm[2]:
        return True
    else:
        return False
def has_1_3_2(perm):
    if perm[0]<perm[2]<perm[1]:
        return True
    else:
        return False
def has_3_1_2(perm):
    if perm[1]<perm[2]<perm[0]:
        return True
    else:
        return False
def has_2_3_1(perm):
    if perm[2]<perm[0]<perm[1]:
        return True
    else:
        return False


# In[58]:


# INSTRUCTIONS TO GET MANY EQUIVALENCE CLASSES:
# get_big_data is the main function of this program.
# n (INT) is the desired size of a permutation.
# show_equiv_classes (BOOL) determines whether or not a list of Knuth equiv. classes should be shown.
# show_graph (BOOL) determines whether not a graph is shown. Here there will be options for user input. Just in type and press enter.

#EXAMPLE:
get_big_data(n = 4, show_equiv_class_list = True, show_graph = True)

################################################################################################################################################

# INSTRUCTIONS TO GET A SINGLE EQUIVALENCE CLASS AND ITS GRAPH:
# get_small_data is the main function of this program.
# the options here are similar to the options in get_big_data and/or are self-explanitory.

#EXAMPLE:
get_small_data(equivalence_class_representitive = "3412", show_equiv_class_list = True, show_graph = True)

