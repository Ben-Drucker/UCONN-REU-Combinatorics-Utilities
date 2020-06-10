#!/usr/bin/env python
# coding: utf-8

'''
This function finds the DL value for a given number of subsequences k (requested by user) by checking all possible 
combinations of k consecutive subsequences (decompositions)

Inputs:
    1. p: Permutation
    2. k: DL subscript (i.e. # of subsequences requested)

Outputs:
    1. D^L value for the given permutation and k
'''

DL_cheat_sheet = {}

def DL_k_copy(p,k):
    
    global DL_cheat_sheet
    
    #convert Permutation to List
    p_list = []
    for elt in range(len(p)):
        p_list.append(p(elt + 1))
        
    # We need to turn our input into something that python knows how to hash. i.e., a tuple of tuples
    key = (tuple(p_list),k)
    if (key in DL_cheat_sheet): 
        return DL_cheat_sheet[key]
    
    if (len(p) == 1):
        return 1
    if (k == 1):
        size = permutation.to_standard(p).reverse().longest_increasing_subsequence_length()
        return size
            
    DL = 0
    for break_pt in range(len(p) - 1):
        p1 = p_list[:break_pt+1]
        p2 = p_list[break_pt+1:]
        if (k >= 2): #recurse
            size1 = permutation.to_standard(p1).reverse().longest_increasing_subsequence_length()
            size2 = DL_k_copy(permutation.to_standard(p2),k-1)
            value = size1 + size2
            if (value > DL): DL = value
                
    #Adding to DL_cheat_sheet            
    if (len(DL_cheat_sheet) <= 1000000): #DL_cheat_sheet stores the 1000000 most recent answers
        DL_cheat_sheet[key] = DL
    else:
        DL_cheat_sheet = {}
                
    return DL

##############################################################################################################

'''
This function finds the best place to split a subsequence into two pieces which will yield the highest DL value

Inputs:
    1. Permutation (as a list)

Outputs:
    1. The DL value of the best split
    2. One pair of subsequences which yield this best DL value
'''

def Best_Split(p_list):
    DL_of_Best_Split = 0
    subs = []
    for my_break in range(len(p_list) - 1):
        p1 = p_list[:my_break+1]
        p2 = p_list[my_break+1:]
        size1 = permutation.to_standard(p1).reverse().longest_increasing_subsequence_length()
        size2 = permutation.to_standard(p2).reverse().longest_increasing_subsequence_length()
        value = size1 + size2
        if (value > DL_of_Best_Split): 
            DL_of_Best_Split = value
            subs = [p1,p2]
            

    return DL_of_Best_Split, subs #two subsequences of best split
##############################################################################################################

'''
This function takes a permutation list and looks for the best place to split the list. The new subsequences
are stored in split_list_list, the list of all resulting subsequences. The process repeats, but now the permutation
list is a list of all resulting subsequences. It will output the value it thinks is DL according to this algorithm.

Inputs:
    1. p: Permutation
    2. Num_subsequences: (i.e. k) (i.e. # of subsequences requested)

Outputs:
    1. DL_k_list: List of DL values from 1 to k (i.e. # of subsequences requested)
    2. DL_k: DL value for k subsequences
'''

def Q1_DL_k(p,num_subsequences):
    
    if (len(p) == 1):
        return 1
    
    #convert Permutation to List (p_list)
    p_list = []
    for elt in range(len(p)):
        p_list.append(p(elt + 1))
    
    #Let's create k subsequences:
    DL_k_list = []
    
    for k in range(1,num_subsequences+1):       
        DL = 0
        if (k == 1):
            DL_k = permutation.to_standard(p).reverse().longest_increasing_subsequence_length()
            split_list_list = [p_list]
            DL_k_list.append(DL_k)

        else:
            for perm in range(len(split_list_list)): #perm = number of subsequences in decomposition
                value, subs_list_list = Best_Split(split_list_list[perm]) #best split amongst all subsequences
                if (value > DL):
                    DL = value
                    best_subsequences_list_list = subs_list_list
                    break_pt = perm
                    
            subtract = permutation.to_standard(split_list_list[break_pt]).reverse().longest_increasing_subsequence_length()
            DL_k = (DL_k_list[-1] - subtract) + DL
            DL_k_list.append(DL_k)
            

            #rewrite split_list_list entirely with added split
            new_list = []
            for ind in range(len(split_list_list)):
                if (ind==break_pt):
                    new_list.append(best_subsequences_list_list[0])
                    new_list.append(best_subsequences_list_list[1])
                else:
                    new_list.append(split_list_list[ind])
            split_list_list = new_list

    return DL_k_list, DL_k


##############################################################################################################


'''
QUESTION 1: Can you find a decomposition of DL_(k+1) by taking any decomposition of DL_(k) and splitting 
one of the subsequences into two?

ANSWER: No. Try the Permutation 63417285.
'''

print('Question 1:')
import sage.combinat.permutation as permutation
p = Permutation([6,3,4,1,7,2,8,5])
n = len(p)

for i in range(n):
    i += 1
    correct_DLk = DL_k_copy(p,i)
    foo, test_DLk = Q1_DL_k(p,i)
    if (test_DLk != correct_DLk):
        print('Failure. At k =',i,', the DL according to Q1 algorithm is',test_DLk,', but the correct DL_k is',correct_DLk)
        break 


##############################################################################################################


'''
This iterative function finds the length of longest decreasing subsequence

Inputs:
    1. A: subsequence as a list
    
Outputs:
    1. L: Length of longest decreasing subsequence of the subsequence A
'''

def LDS(A):

# list to store sub-problem solution. L[i] stores the length
# of the longest decreasing subsequence ends with A[i]
    L = [0] * len(A)

    # longest decreasing subsequence ending with A[0] has length 1
    L[0] = 1

    # start from second element in the list
    for i in range(1, len(A)):

        # do for each element in sublist A[0..i-1]
        for j in range(i):
            # find longest decreasing subsequence that ends with A[j]
            # where A[j] is more than the current element A[i]

            if A[j] > A[i] and L[j] > L[i]:
                L[i] = L[j]

        # include A[i] in LDS
        L[i] = L[i] + 1

    # return longest decreasing subsequence (having maximum length)
    return max(L)


##############################################################################################################


'''
This function finds the DL value and all good decompositions for a given k.

Inputs:
    1. p_list: Permutation as a list
    2. k: D^L subscript (i.e. # of subsequences requested)
    
Outputs:
    1. DL: value for that DL_k
    2. good_decompositions: decompositions which yield themselves to the DL value
'''

DL_cheat_sheet = {}

def Q2_DL_k(p_list,k): #takes in p as a list
    
    global DL_cheat_sheet
    
    # We need to turn our input into something that python knows how to hash. i.e., a tuple of tuples
    key = (tuple(p_list),k)
    if (key in DL_cheat_sheet): 
        return DL_cheat_sheet[key]
    
    #Initializing variables and lists
    DL = 0
    all_decompositions_values = [0]*(len(p_list)-1)
    all_decompositions = [0]*(len(p_list)-1)
    all_breaks = [[]]*(len(p_list)-1)
    good_decompositions_values = []
    good_decompositions = []
    good_breaks = []
      
    if (len(p_list) == 1):
        DL = 1
        return DL, [[p_list]]
    
    if (k == 1):
        DL = LDS(p_list)
        return DL, [[p_list]]
            
    for my_break in range(len(p_list) - 1):
        p1 = p_list[:my_break+1]
        p2 = p_list[my_break+1:]
        size1 = LDS(p1)
        size2, all_decomps_list = Q2_DL_k(p2,k-1)
        value = size1 + size2
        if (value > DL): 
            DL = value
            
        all_decompositions_values[my_break] = value
        
        # all_decomps_list: is the list of decompositions for the recursive subproblem
        # p1 is the part of the partition that we want to add to each of the decompositions in size2[1]
        new_decompositions_list = []
        for old_decompositions in all_decomps_list:
            new_decompositions = [p1] + old_decompositions
            new_decompositions_list.append(new_decompositions)
        all_decompositions[my_break] = new_decompositions_list 
        

    for ind in range(len(all_decompositions_values)):
        if (all_decompositions_values[ind] == DL):
            good_decompositions_values.append(all_decompositions_values[ind])
            good_decompositions.extend(all_decompositions[ind])
            
    #Adding to DL_cheat_sheet            
    if (len(DL_cheat_sheet) <= 10000000): #DL_cheat_sheet stores the 1000000 most recent answers
        DL_cheat_sheet[key] = DL, good_decompositions
    else:
        print('overflow')
        DL_cheat_sheet = {}
            
    return DL, good_decompositions


##############################################################################################################


'''
This function takes a decomposition and turns it into a list of break points.

Inputs:
    1. decomposition
    
Outputs:
    1. breaks_list: list of places to break
'''
def decomposition_to_breaks_list(decomposition):
    breaks_list = []
    break_pt = -1
    for x in decomposition:
        break_pt = break_pt + len(x)
        breaks_list.append(break_pt)
    return breaks_list

##############################################################################################################
'''
This function takes a list of decompositions and turns it into a list of lists of break points.

Inputs:
    1. list_of_decompositions
    
Outputs:
    1. breaks_list_list: list of lists of places to break
'''

def list_of_decompositions_to_list_of_breaks_lists(list_of_decompositions):
    breaks_list_list = []
    for x in list_of_decompositions:
        breaks_list_list.append(decomposition_to_breaks_list(x))
    return breaks_list_list


##############################################################################################################


'''
This function checks if the first list contains all elements in the second list

Inputs:
    1. big_list: first list (bigger one)
    
Outputs:
    1. sub_list: second list (smaller one)
'''
def sublist_in_list(big_list, sub_list):
    #check if my_list contains all elements in my_sublist

    result =  all(elem in big_list  for elem in sub_list)

    if result:
        #big_list contains all elements in sub_list 
        return True
    else :
        #big_list does not contains all elements in sub_list
        return False


##############################################################################################################


'''
This function checks the question, "Can every good decomposition of k+1 subsequences be reached from
a good decomposition of k subsequences?"

Inputs:
    1. p_list: permutation as a list
    
Outputs:
    1. True: If answer to question is true
    2. False: If answer to question is false
'''

def check_all_sublists(p_list):
    count_list = []
    n = len(p_list)
    comparison_list = []
    for k in range(1,n):
        foo,my_sublist= Q2_DL_k(p_list,k)
        bar,my_list= Q2_DL_k(p_list,k+1)
        count = 0
        for x in list_of_decompositions_to_list_of_breaks_lists(my_list):
            for y in list_of_decompositions_to_list_of_breaks_lists(my_sublist):
                if(sublist_in_list(x,y)):
                    count+=1
                    break
        if (count==len(list_of_decompositions_to_list_of_breaks_lists(my_list))):
            count_list.append(k)
        comparison_list.append(k)
    if (count_list == comparison_list):
        return True
    else:
        return False


##############################################################################################################


'''
QUESTION 2: Can you find every DL_(k+1) by finding at least one decomposition for DL_k and splitting one of the subsequences 
#in that decomposition in half?

ANSWER: No. Try the Permutation 326159487.
'''

print('Question 2:')
Failures = 0
for p in Permutations(6):
    
    #convert Permutation to List (p_list)
    p_list = []
    for elt in range(len(p)):
        p_list.append(p(elt + 1))
    
    if(check_all_sublists(p_list) == False):
        Failures += 1
        print(p_list)
print('Failures:',Failures)


##############################################################################################################


'''
This function prints out one path of connected good decompositions (if one exists)

Inputs:
    1. p_list: permutation as a list
    
Outputs:
    1. One path of connected good decompositions
    2. 'Fail' if one path does not exist for the permutation
    
Note:
    1. I'm not actually sure if this works yet...
'''
def tree_of_decompositions(p_list): #takes in a list
    
    #start tree
    n = len(p_list)
    bar,my_list= Q2_DL_k(p,n)
    k = n
    while (k > 1):
        foo,my_sublist= Q2_DL_k(p,k-1)
        bar,my_list= Q2_DL_k(p,k)
        countx = -1
        for x in list_of_partitions_to_list_of_breaks_lists(my_list):
            countx +=1
            county = -1
            for y in list_of_partitions_to_list_of_breaks_lists(my_sublist):
                county += 1
                if(sublist_in_list(x,y)):
                    if(k==n):
                        print('k=',n,':',my_list[countx])
                        print('k=',k-1,':',my_sublist[county])
                    else:
                        print('k=',k-1,':',my_sublist[county])
                    break
                else:
                    if(countx == len(list_of_partitions_to_list_of_breaks_lists(my_list))):
                        print('fail')
            break
        k = k - 1


##############################################################################################################


'''
This function checks if one path of connected good decompositions exists

Inputs:
    1. p_list: permutation as a list
    
Outputs:
    1. True: If one path of connected good decompositions exists
    2. False: If otherwise
    
Note:
    1. I'm not actually sure if this works yet...
'''
def Q3(p_list): #takes in a list
    
    #start tree
    n = len(p_list)
    k = n
    while (k > 1):
        foo,my_sublist= Q2_DL_k(p,k-1)
        bar,my_list= Q2_DL_k(p,k)
        countx = 0
        for x in list_of_partitions_to_list_of_breaks_lists(my_list):
            countx +=1
            for y in list_of_partitions_to_list_of_breaks_lists(my_sublist):
                if(sublist_in_list(x,y)):
                    break
                else:
                    if(countx == len(list_of_partitions_to_list_of_breaks_lists(my_list))):
                        return False
            break
        k = k - 1
        
    return True


##############################################################################################################


'''
QUESTION 3: Can we always find a path to connect good decompositions from k=1 to k=n?

ANSWER: Yes (up to n=9) (If my code is correct...)
'''

print('Question 3:')
Failures = 0
for p in Permutations(8): #want to check for n=10 next!
    
    #convert Permutation to List (p_list)
    p_list = []
    for elt in range(len(p)):
        p_list.append(p(elt + 1))
    
    #Checking Q3
    if (Q3(x) != True):
        print(x)
        Failures += 1
        break
        
if(Failures==0):
    print('Q3 lives on to the next n!')
else:
    print('Failure')





