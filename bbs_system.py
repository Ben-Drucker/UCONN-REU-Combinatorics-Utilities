#!/usr/bin/env python
# coding: utf-8

# In[35]:


# BBS is apparently already implemented, but seemed more complicated than we needed?
# I couldn't figure out how to use it
def BBS_move(old_state):
    # takes a list containing the integers 1-n (as well as an
    # unspecified # of zeroes) and preforms a "Fukada" BBS move on it

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
        # returns only the state at time t, but can modify to return all intermediate steps
        return system[t]
    
    system = [arrangement]
    for move in range(-t):
        step = backward_move(system[move])
        system.append(step)
        
    return system[-t]

def SolitonContent(config):
    # takes an arrangement of balls (as a list) and returns its SolitonContent as a Tableau
    # CONTINGENT on BBS always being sorted after n moves
    # it shouldn't be too hard to insert logic that checks to make sure we've reached when we reach a steady state
    # just feels like too much work right now
    # besides, it seems quite likely that in fact bbs IS always sorted after n moves
    
    # find the BBS configuration at t = n
    n = max(config)
    final = BBS(config, n)
    
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


# In[36]:


# examples:
pi = [4,2,6,1,3,5,7]

# BBS_move does a single "Fukada" move
print(BBS_move(pi), '\n')

# BBS calls for a parameter t and returns the result after t moves
t = 2
print(BBS(pi, t), '\n')

# SolitonContent returns the SolitonContent of a permuation
SolitonContent(pi).pp() # pretty printing
print('\n')

# can also now put negative values for time arg in BBS
# the printing is a bit awkward since it aligns on the left
for time in range(0, -4, -1):
    print(BBS([7,8,3,4,6,1,2,5], time))

