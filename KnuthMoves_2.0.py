#!/usr/bin/env python
# coding: utf-8

# In[149]:


from sage.graphs.graph_input import from_dict_of_lists
import sage.graphs.graph_plot

def main(n, show_equiv_class_list, show_graph):
    ##### BEGIN ELI'S ADDITION
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
            g.add_edge(me[i][0], me[i][1], "KB")
        else:
            g.add_edge(me[i][0], me[i][1], me[i][2])
        i = j
    ### END ELI'S ADDITION
    list_of_equiv_classes = g.connected_components()
    if show_equiv_class_list:
        print("======= Knuth/P-Tableau Equivalence Classes =======")
        print(list_of_equiv_classes)
        print("===================================================")
    if show_graph:
        print("There are", len(list_of_equiv_classes), "equivalence classes.")
        show_specific_equiv_class = input("Display a specific equivalence class? (y/n): ").lower()
        if show_specific_equiv_class == "y":
            eq_cl = input("Equivalence Class? (E.g., 13875(10)6249)): ")
            eq_cl_perm = permToCorrectFormat(eq_cl)
            dictOfTimes = ss_times(n)
            if dictOfTimes[eq_cl_perm] == 0:
                searchForVert = "RW: "+str(eq_cl)+", t="+str(dictOfTimes[eq_cl_perm])
            else:
                searchForVert = str(eq_cl)+", t="+str(dictOfTimes[eq_cl_perm])
        else:
            first_class = int(input("first equiv. class to graph? "))
            last_class = int(input("last equiv. class to graph? "))
        fs = int(input("Enter desired figure size: (typically ~ <number of elements graphed>): "))
        ar = float(input("Enter desired aspect ratio (typically ~ 0.5): "))
        vs = int(input("Enter desired vertex size (typically 10000): "))
        ps = input("Would you like the graph to be ordered like a Hasse diagram? (y/n): ").lower()
        if ps == "y":
            ps = "ranked"
        else:
            ps == None
        list_of_edges = g.edges() #CHANGED FROM generateData(n)
        if show_specific_equiv_class == "n":
            desired_equiv_classes = list_of_equiv_classes[first_class-1:last_class]
            desired_elts = []
            for elt in desired_equiv_classes:
                for subelt in elt:
                    desired_elts.append(subelt)
            display_edges = []
            for edge in list_of_edges:
                if edge[0] in desired_elts and edge[1] in desired_elts:
                    display_edges.append(edge)
        else:
            display_edges = list_of_edges
        g = Graph(display_edges, weighted = True, loops=True)
        print("======= Selected Graph Loading =======")
        ##### Begin Relabeling
        rrws = getReadingWords(g)
        for rrw in rrws:
            rrw_highlighted = "RW: "+str(rrw)
            g.relabel({rrw: rrw_highlighted})
        for vertex in g.to_dictionary():
            vert = stripToDigits(vertex)
            pi = permToCorrectFormat(vert)
            dictOfTimes = ss_times(n)
            g.relabel({vertex: str(vertex)+", t="+str(dictOfTimes[pi])})
        finalDict = g.to_dictionary()
        ##### Begin Heights
        dictOfHeights = {}
        for key in finalDict:
            invs = stripToPerm(key).number_of_inversions()
            if not invs in dictOfHeights:
                dictOfHeights[invs] = [key]
            else:
                dictOfHeights[invs].append(key)
        done = False
        if show_specific_equiv_class == "y":
            connLs = g.connected_components_subgraphs()
            for connComp in connLs:
                if done:
                    break
                theComponent = connComp
                theComponentDict = connComp.to_dictionary()
                for key in connComp:
                    if key == searchForVert:
                        done = "True"
                        break
            altDictOfHeights = {}
            for key in theComponentDict:
                invs = stripToPerm(key).number_of_inversions()
                if not invs in altDictOfHeights:
                    altDictOfHeights[invs] = [key]
                else:
                    altDictOfHeights[invs].append(key)
            done = False
            plt = theComponent.plot(edge_labels = True, transparent = True, figsize = fs, aspect_ratio = ar, layout = ps, vertex_size = vs, edge_labels_background="#EFEFEF", vertex_color = "white", edge_color="#FF0000", heights = altDictOfHeights)
            plt.show()
        else:
            plt = g.plot(edge_labels = True, transparent = True, figsize = fs, vertex_size = vs, layout = ps, edge_labels_background="#EFEFEF", vertex_color = "white", edge_color="#FF0000", heights = dictOfHeights)
            plt.show()
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


# In[150]:


import sage.combinat.permutation as permutation

def stripToPerm(vertx):
    base = stripToDigits(vertx)
    baseLs = removeDuplicates(base)
    if "0" in baseLs:
        baseLs.remove("0")
    return permToCorrectFormat(baseLs)

def stripToDigits(string):
    result = ""
    for letter in string:
        if letter.isdigit() or "(" in letter or ")" in letter:
            result += letter
    return result

def permToCorrectFormat(perm):
    if "(" in perm:
        listOfIndices = []
        outputLs =[]
        parenContent = ""
        inParens = False
        for i in range(len(perm)):
            if not perm[i] in "()" and not inParens:
                outputLs.append(int(perm[i]))
            else:
                inParens = True
            if inParens:
                if not perm[i] in "()":
                    parenContent += perm[i]
                if perm[i] == ")":
                    outputLs.append(int(parenContent))
                    parenContent = ""
                    inParens = False
    else:
        outputLs = []
        for letter in perm:
            outputLs.append(int(letter))
    return Permutation(outputLs)

def SD_eq_RSK(perm):
    SD = SolitonDecomp(perm)
    P = RSK(perm)[0]
    if SD == P:
        return True
    else:
        return False

def BBS_move(old_state):
    # takes a list containing the integers 1-n (as well as an
    # unspecified # of zeroes) and preforms a "Fukuda" BBS move on it

    state = []
    for elt in old_state:
        state.append(elt)

    # naive method of preforming a move, runs in cubic? time
    # still fast enough for relatively small permuations
    n = max(state)
    for i in range(1,n+1):
        # checks the location of each integer 1-n
        j = state.index(i)
        # if there is a zero to the right of i, preform a swap
        if 0 in state[j+1:]:
            k = state[j+1:].index(0)
            state[j], state[k+j+1] = state[k+j+1], state[j]
        # otherwise, stick i on the end of the list and put a zero where i was
        else:
            state.append(i)
            state[j] = 0

    return state

def BBS(arrangement, t):
    if t >= 0:
        system = [arrangement]
        for move in range(t):
            step = BBS_move(system[move])
            system.append(step)
        # THIS IS DIFFERENT FROM WHAT BBS FUNCTION RETURNS IN bbs_system.py
        # RETURNS ALL CONFIGS FOR times 0,1,...,t
        return system

    system = [arrangement]
    for move in range(-t):
        step = backward_move(system[move])
        system.append(step)
    return system

def SolitonDecomp(config):
    # takes an arrangement of balls (as a list) and returns its SolitonDecomp as a Tableau
    # CONTINGENT on BBS always being sorted after n moves
    # it shouldn't be too hard to insert logic that checks to make sure we've reached when we reach a steady state
    # just feels like too much work right now
    # besides, it seems quite likely that in fact bbs IS always sorted after n moves

    # find the BBS configuration at t = n
    n = max(config)
    final = BBS(config, n)[n - 1]

    # create a list of lists sc that will store the soliton content
    sc = [[]]
    # sol_num tracks which soliton we're on (from left to right)
    sol_num = 0
    l = len(final)
    for i in range(l):
        if final[i] != 0:
            # put the current value on the end of the current soliton
            sc[sol_num].append(final[i])
            if i < l - 1:
                if final[i] >= final[i + 1]:
                    # if the next entry is smaller than current one, make a new soliton
                    sol_num = sol_num + 1
                    sc.append([])
    # sc has the solitons in the reverse order, so we have to reverse it
    return Tableau(sc[::-1])

def ss_times(n):
    # takes an integer n and returns a dictionary with keys for each
    # permutation in Sn and values equal to number of BBS moves it takes to reach a steady state

    stopping_times = {}
    for sigma in SymmetricGroup(n):
        p = Permutation(sigma)
        perm = list(p)
        sd = SolitonDecomp(perm)

        # grabs the reading word of SolitonDecomp
        sd_list = []
        for l in sd[::-1]:
            for num in l:
                sd_list.append(num)

        # configs is a list containing the configuration of our permutation after t BBS moves at index t
        configs = BBS(perm, n)

        # check each time t=0,1,...,n to see if the configuration is in the steady state order
        # the first such time is the stopping time, so we store it in the dictionary and move onto the next perm
        for t in range(n + 1):
            cur = []
            for elt in configs[t]:
                if elt != 0:
                    cur.append(elt)
            if sd_list == cur:
                stopping_times[p] = t
                break

    return stopping_times

def backward_ss(pi):
    # make n backward moves, see what time we reach a steady state

    perm = list(pi)
    n = max(perm)
    # a list where the ith index is the config at t = -i
    sys = BBS(perm, -n)

    steady = []
    for elt in sys[n]:
        if elt != 0:
            steady.append(elt)

    for t in range(n + 1):
        cur = []
        for elt in sys[t]:
            if elt != 0:
                cur.append(elt)
            if cur == steady:
                return -t

def backward_move(old_state):
    # reverse and complement
    n = max(old_state)
    state = []
    for elt in old_state[::-1]:
        if elt == 0:
            state.append(elt)
        else:
            state.append(n + 1 - elt)

    # preform a BBS move on the reversed complement and then return
    # the reversed complement of that
    mid_state = BBS_move(state)
    new_state = []
    for elt in mid_state[::-1]:
        if elt == 0:
            new_state.append(elt)
        else:
            new_state.append(n + 1 - elt)

    return new_state


# In[151]:


def getReadingWords(graph):
    rrws = []
    dictOfEdges = graph.to_dictionary()
    for key in dictOfEdges:
        if is_reading_word(permToCorrectFormat(key)):
            rrws.append(key)
    return rrws

def is_reading_word(Perm):
    descents = getDescents(Perm)
    proto_tab = partitionAfterIndex(Perm,descents)
    proto_tab.reverse()
    if is_weakly_len_decr(proto_tab):
        tab = Tableau(proto_tab)
        #tab.pp()
        return tab.is_standard()
    else:
        return False

def is_weakly_len_decr(ls):
    for i in range(len(ls)-1):
        if len(ls[i])<len(ls[i+1]):
            return False
    return True

def partitionAfterIndex(Perm, indicies):
    returnList = []
    prevIndex = 0
    indicies.append(len(Perm))
    for index in indicies:
        returnList.append(Perm[prevIndex:(index+1)])
        prevIndex = index + 1
    return returnList

def getDescents(Perm):
    asc = []
    for i in range(len(Perm)-1):
        if Perm[i]>Perm[i+1]:
            asc.append(i)
    return asc


# In[152]:


def getSubset(n,k):
    ls = [Permutations(n).identity()]
    current = Permutations(n).identity()
    for i in range(k):
        ls.append((next(current)))
        current = next(current)
    return ls


# In[ ]:


# INSTRUCTIONS:
# n (INT) is the desired size of a permutation.
# show_equiv_classes (BOOL) determines whether or not a list of Knuth equiv. classes should be shown.
# show_graph (BOOL) determines whether not a graph is shown. Here there will be options for user input. Just in type and press enter.
# follow prompts to generate Graph

#EXAMPLE:

main(n = 6, show_equiv_class_list = False, show_graph = True)

#Output:
#>>> There are 26 equivalence classes.
#>>> Display a specific equivalence class? (y/n): y
#>>> Equivalence Class? (E.g., 13875(10)6249)): 51342
#>>> Enter desired figure size: (typically ~ factorial(<number of elements graphed>))20
#>>> Enter desired aspect ratio (typically ~ 0.5): .5
#>>> Enter desired vertex size (typically 10000): 10000
#>>> Would you like the graph to be ordered like a Hasse diagram? (y/n): y
#>>> ======= Selected Graph Loading =======
