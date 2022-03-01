from collections import deque
from distutils.util import strtobool
import heapq
import itertools
import math
import pickle
import sys

# Given rational p/q > 1, this code generates an automaton to find a palindromic or antipalindromic A and B such that A/B = p/q.

# state = (-q < carry_left_diff < p, 0 \leq B_carry_right < p, 0 \leq A_carry_right < q, savedSymbols, numSymbols, phase)

def generateAutomata(p, q, b, ASet, BSet, verbose):  
    # p,q - positive integers, p > q.
    # b - integer base, b > 1.
    # ASet, BSet - either "pal" or "apal", chooses between palindromes and antipalindromes.
    # verbose - boolean, extra output for debugging.

    # The following are several helper functions.
    # Afterwards, there's a more detailed overview of the process.
    
    def loadingPhase(state, toLoad): # Start by loading input into the saved symbols.
        states[state] = list()
        initUnloadingPhase(state, True if toLoad == state[4] else False) # Early abort from loading phase. Implicitly fill with zeroes.

        for i in range(1 if toLoad == state[4] else 0, b): # Ensure that the input doesn't start with a zero.
            currentA = (q * ATransform(i)) + state[2]
            currentLeftCarry = (q * i) - (p * 0) + (b * state[0])
            if currentLeftCarry >= p or currentLeftCarry <= -q:
                continue
            for j in range(1 if toLoad == state[4] else 0, b):
                currentB = (p * BTransform(j)) + state[1]
                if (currentA % b) != (currentB % b):
                    continue
                newState = (currentLeftCarry, currentB // b, currentA // b, (state[3] * b) + j, state[4], 1 if toLoad == 1 else 0)
                states[state].append((i, j, newState))

                if toLoad == 1: # If loading is complete, switch phase.
                    queue.append(newState)
                else:
                    loadingPhase(newState, toLoad-1)

        if verbose:
            print("loading1", state)

    def shiftingPhase(): # Once we've loaded the correct number of digits, shift arbitrarily and try to unload at every step.
        while len(queue):
            state = queue.popleft()
            if state in states: # This check could be done at the append to take less memory, but I think it'd be slower.
                continue
            states[state] = list()
            initUnloadingPhase(state, False)

            topSymbol = state[3] // (b**(state[4] - 1))
            newSavedSymbols = ((state[3] % (b**(state[4] - 1))) * b)
            for i in range(b):
                currentA = (q * ATransform(i)) + state[2]
                currentLeftCarry = (q * i) - (p * topSymbol) + (b * state[0])
                if currentLeftCarry >= p or currentLeftCarry <= -q:
                    continue
                for j in range(b):
                    currentB = (p * BTransform(j)) + state[1]
                    if (currentA % b) != (currentB % b):
                        continue
                    newState = (currentLeftCarry, currentB // b, currentA // b, newSavedSymbols + j, state[4], 1)
                    states[state].append((i, j, newState))
                    queue.append(newState)

            if verbose:
                print("shifting", state)

    def initUnloadingPhase(state, first):
        # Start unload. Nondeterministically choose if B has odd length then check all the cases for odd length if so.
        # if first==true then the automata hasn't read any symbols yet and therefore B must be a single symbol.
        if first == False:
            unloadingPhase(state) # len(B) not odd

        # len(B) odd
        topSymbol = state[3] // (b**(state[4] - 1))
        newSavedSymbols = (state[3] % (b**(state[4] - 1)))
        for i in range(1 if first else 0, b):
            currentA = (q * ATransform(i)) + state[2]
            currentLeftCarry = (q * i) - (p * topSymbol) + (b * state[0])
            if currentLeftCarry >= p or currentLeftCarry <= -q:
                continue
            for j in range(1 if first else 0, b):
                if BTransform(j) != j:
                    continue
                currentB = (p * BTransform(j)) + state[1]
                if currentA % b != currentB % b:
                    continue
                newState = (currentLeftCarry, currentB // b, currentA // b, newSavedSymbols, state[4] - 1, 2)
                states[state].append((i, -1 - j, newState)) # The negative number isn't input to the automata, just to help computation later.
                if newState in states:
                    continue
                states[newState] = list()
                unloadingPhase(newState)

        if verbose:
            print("init unloading", state)
                

    def unloadingPhase(state): # Unload until we reach one of the terminal cases. Each unload removes two symbols from state[3]. If A has odd length, state[4] will also be odd.
        if state[4] == 0: #terminal, len(A) not odd
            if state[0] == state[1] - state[2]:
                states[state].append(("", "", "accept"))
                if verbose:
                    print("found an accept")

        elif state[4] == 1: #terminal, len(A) odd
            currentB = (p * BTransform(state[3])) + state[1]
            for i in range(b):
                if ATransform(i) != i:
                    continue
                currentA = (q * ATransform(i)) + state[2]
                if currentA % b != currentB % b:
                    continue
                if state[0] == (currentB // b) - (currentA // b):
                    states[state].append((-1 - i, "", "accept")) # The negative number isn't input to the automata, just to help computation later.
                    if verbose:
                        print("found an accept, sigma_A=" + str(i))

        else:
            topSymbol = state[3] // (b**(state[4] - 1))
            bottomSymbol = state[3] % b
            newSavedSymbols = (state[3] % (b**(state[4] - 1)))//b
            currentB = (p * bottomSymbol) + state[1]
            for i in range(b):
                currentA = (q * ATransform(i)) + state[2]
                if currentA % b != currentB % b:
                    continue
                currentLeftCarry = (q * i) - (p * topSymbol) + (b * state[0])
                if currentLeftCarry >= p or currentLeftCarry <= -q:
                    continue
                newState = (currentLeftCarry, currentB // b, currentA // b, newSavedSymbols, state[4]-2, 2)
                states[state].append((i, "", newState))
                if newState in states:
                    continue
                states[newState] = list()
                unloadingPhase(newState)

        if verbose:
            print("unloading", state)

    def zeroDifference(): # This is a separate function for handling when 0 < log_b(p/q) < 1. Essentially the same but with no saved symbols.
        while len(zeroQueue):
            state = zeroQueue.popleft()
            if state in states:
                continue
            states[state] = list()

            # Unloading
            if state[0] == state[1] - state[2] and state[5] != -2: # Ensure that it's not the initial state.
                states[state].append(("", "", "accept"))
            else:
                for i in range(1 if state[5] == -2 else 0, b):
                    if ATransform(i) != i:
                        continue
                    currentA = (q * ATransform(i)) + state[2]
                    for j in range(1 if state[5] == -2 else 0, b):
                        if BTransform(j) != j:
                            continue
                        currentB = (p * BTransform(j)) + state[1]
                        if currentA % b != currentB % b:
                            continue
                        if state[0] == (currentB // b) - (currentA // b):
                            states[state].append((-1 - i, -1 - j, "accept")) # The negative number isn't input to the automata, just to help computation later.

            # Shift
            for i in range(1 if state[5] == -2 else 0, b):
                currentA = (q * ATransform(i)) + state[2]
                for j in range(1 if state[5] == -2 else 0, b):
                    currentB = (p * BTransform(j)) + state[1]
                    if currentA % b != currentB % b:
                        continue
                    currentLeftCarry = (q * i) - (p * j) + (b * state[0])
                    if currentLeftCarry >= p or currentLeftCarry <= -q:
                        continue
                    newState = (currentLeftCarry, currentB // b, currentA // b, -1, -1, -1)
                    states[state].append((i, j, newState))
                    zeroQueue.append(newState)

            if verbose:
                print("zero shifting", state)

    if p <= q or b <= 1:
        print("Requires b >= 2 and p > q")
        return None

    if ASet not in ["pal", "apal"] or BSet not in ["pal", "apal"]:
        print("Requires ASet, BSet \\in {\"pal\", \"apal\"}")
        return None

    # Setup the transformation for antipalindromes if required.
    if ASet == "pal":
        ATransform = lambda s: s
    elif ASet == "apal":
        ATransform = lambda s: b-1-s

    if BSet == "pal":
        BTransform = lambda s: s
    elif BSet == "apal":
        BTransform = lambda s: b-1-s

    # Get the possible differences in length between A and B.
    lower = math.floor(math.log(p/q, b))
    upper = math.ceil(math.log(p/q, b))

    states = dict() # Dictionary representing the automata states and transitions.
    states["start"] = []
    states["accept"] = []

    queue = deque() # Queue of states we need to add to the automata.
    zeroQueue = deque() # Separate queue for handling when lower = 0.

    # state = (-q < carry_left_diff < p, 0 \leq B_carry_right \leq p, 0 \leq A_carry_right \leq q, savedSymbols, numSymbols, phase)
    # States are a tuple of 6 integers.
    # The left carry difference is between -q and p.
    # The B carry is less than p.
    # The A carry is less than q.
    # We need to save up to log_b(n) symbols to make everything line up.
    # We store them as a single integer whose digits in base b that are the saved symbols.
    # We keep track of how many symbols we are currently saving (or going to save if we're currently loading) with the fifth element of the tuple.
    # We keep track of the phase the state is in with the last element of the tuple, i.e. 0:Loading, 1:Shifting, 2:Unloading
    # The only edges between states of different phases are of the form phase 0 -> 1, 0 -> 2, 1 -> 2

    # Start state is "start" and we non-deterministically choose the size difference between A and B.
    # This size difference is always the ceiling or floor of math.log(n, b)
    # The end state is "accept".

    # The algorithm overview is as follows:
    # We start by checking the right side equations and start loading up the saved symbols.
    # We save at most as many symbols as the difference in length between A and B.
    # Once you have reached the maximum number of saved symbols, you cycle through them, deleting the oldest one and adding the new one when you read in a new symbol.
    # At any state, you can start unloading, i.e. reading {0, 1, \cdots b-1} \times {X} and seeing if you get an equality at the end.
    # The unloading functions are called after each state is reached in either loading or shifting.
    # When you've found all reachable states from loading and shifting and unloaded all of them, you're done, return all the states.
    # The equations checked ensure that P*B = Q*A.
    # More detail on the equations, algorithm, and results can be found at: link.to.paper

    if lower == 0: # Special case for 1 < p/q < b
        states["start"].append(("", "", (0, 0, 0, -1, -1, -2))) # The -2/-1 at state[5] keep the zero difference states separate from the rest.
        states["start"].append(("", "", (0, 0, 0, 0, 1, 0)))
        loadingPhase((0, 0, 0, 0, 1, 0), 1)
        shiftingPhase()
        zeroQueue.append((0, 0, 0, -1, -1, -2))
        zeroDifference()
        return states

    elif lower != upper:
        states["start"].append(("", "", (0, 0, 0, 0, lower, 0)))
        states["start"].append(("", "", (0, 0, 0, 0, upper, 0)))
        loadingPhase((0, 0, 0, 0, lower, 0), lower)
        loadingPhase((0, 0, 0, 0, upper, 0), upper)
        shiftingPhase()
        return states

    else: # Edge case if upper=lower
        states["start"].append(("", "", (0, 0, 0, 0, lower, 0)))
        loadingPhase((0, 0, 0, 0, lower, 0), lower)
        shiftingPhase()
        return states

# Given an automaton, steps through it and finds the minimal paths to each state, also returns the palindrome that leads to accept.
# This is a simple Dijkstra's but a better implementation could probably save some time on the heap inserts.
def getMinimalPaths(p, q, automata, base, ASet, BSet, fullScan):
    if not automata: # Pass through a not found result.
        return None

    # Setup the transformation for antipalindromes if required.
    if ASet == "pal":
        ATransform = lambda s: s
    elif ASet == "apal":
        ATransform = lambda s: base-1-s

    if BSet == "pal":
        BTransform = lambda s: s
    elif BSet == "apal":
        BTransform = lambda s: base-1-s

    stateHeap = []
    pathTo = dict()
    processed = set()
    processed.add("start")
    pathTo["start"] = (0, 0, -1) # if B = bcb^R then this is (len(B), b, c)
    for nextState in automata["start"]:
        pathTo[nextState[2]] = (0, 0, -1)
        heapq.heappush(stateHeap, (0, 0, -1, nextState[2])) # (len(B), b, midB, state)
    while stateHeap:
        path = heapq.heappop(stateHeap)
        if path[3] in processed:
            continue
        processed.add(path[3])

        if path[3] == (math.inf, "accept"):
            if fullScan:
                continue
            else:
                break

        for nextState in automata[path[3]]:
            # Skip anything we've already been to.
            if nextState[2] in processed:
                continue

            # Add the current transition symbol to the path to the state.
            lenB = path[0]
            B = path[1]
            midB = path[2]
            state = nextState[2]
            
            if nextState[1] != "":
                if nextState[1] < 0:
                    midB = -1 - nextState[1] # Handle the middle index
                    lenB += 1
                else:
                    B = (B * base) + nextState[1]
                    lenB += 2

            if state == "accept":
                state = (math.inf, "accept")

            # If this path is an improvement, add it to the heap.
            if state not in pathTo or pathTo[state] > (lenB, B, midB):
                pathTo[state] = (lenB, B, midB)
                heapq.heappush(stateHeap, (lenB, B, midB, state))

    if (math.inf, "accept") not in pathTo:
        return None, pathTo

    path = pathTo[(math.inf, "accept")]
    B = numberToBase(path[1], base) if path[1] > 0 else []
    B = B + ([path[2]] if path[2] != -1 else []) + [BTransform(s) for s in B[::-1]]
    B = listToInt(B, base)
    return ((p * B) // q, B), pathTo

# Finds all states such that they have a path to the accept and gets that path length
# This is designed for the loop checking to get the number of solutions.
# At this point, it works similarly to getMinimalPaths. However, it always goes through the whole automaton where getMinimalPaths might end earlier.
# WARNING: the shortest distanceToAccept value might not show the shortest A/B because of the nondeterminism shenanigans.
# Use getMinimalPaths for shortest paths.
def pathScan(automata):
    distanceToAccept = {}
    parents = {}
    parents["start"] = []
    for state in states:
        for child in states[state]:
            if child[2] not in parents:
                parents[child[2]] = []
            parents[child[2]].append(state)
    queue = deque()
    queue.append(("accept", 0))
    while queue:
        state, distance = queue.popleft()
        if state not in distanceToAccept or distance < distanceToAccept[state]:
            distanceToAccept[state] = distance
            for parent in parents[state]:
                queue.append((parent, distance+1))
    return distanceToAccept, parents

# Build a new automata that only includes states that lead to accept using the distanceToAccept dictionary from pathScan.
def simplifiedAutomata(states, distanceToAccept):
    newStates = {}
    for state in states:
        if state in distanceToAccept:
            newStates[state] = []
            for child in states[state]:
                if child[2] in distanceToAccept:
                    newStates[state].append(child)
    return newStates

# Assumes the automata has the property all states lead to accept.
def checkLoop(states):
    visited = set()
    queue = deque()
    queue.append("start")
    while queue:
        state = queue.popleft()
        if state == "accept":
            continue
        for child in states[state]:
            if child[2] in visited:
                return True
            else:
                visited.add(child[2])
                queue.append(child[2])
    return False

# Convert of list of symbols to an integer
def listToInt(l, base):
    result = 0
    power = 1
    for i in l[::-1]:
        result += power * i
        power *= base
    return result

# Convert an integer to a list of symbols.
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

# Small function to make multiprocessing easier
def getSmallestRatio(p, q, b, ASet, BSet):
    states = generateAutomata(p, q, b, ASet, BSet, False)
    result, _ = getMinimalPaths(p, q, states, b, ASet, BSet, False)
    if result:
        return (p, q, result[0], result[1])
    else:
        return (p, q, -1, -1)

# Another function for multiprocessing
def getSmallestRatioPacked(args):
    return getSmallestRatio(args[0], args[1], args[2], args[3], args[4])

if __name__ == "__main__":
    def info():
        print("Builds an automata for given integers p, q and base that accepts an input string from which an A and B such that A/B = p/q and A and B are palindromes or antipalindromes in base can be found.",
        "Usage: python3 QuotientOfPalEqualsRational.py p q base ASet BSet verbose? saveStates?",
        "    p, q, base - integers, p > 1, p > q, base > 1"
        "    ASet, BSet \\in {\"pal\", \"apal\"}",
        "    verbose, saveStates - booleans, verbose gives extra debug output, saveStates saves the dictionary as a pickle file"
        "Output: p, q, A, B",
        sep="\n", flush=True)

    if len(sys.argv) == 8:
        p = int(sys.argv[1])
        q = int(sys.argv[2])
        b = int(sys.argv[3])
        ASet = sys.argv[4]
        BSet = sys.argv[5]
        verbose = strtobool(sys.argv[6])
        saveStates = strtobool(sys.argv[7])

        if ASet not in ["pal", "apal"] or BSet not in ["pal", "apal"]:
            info()
            exit()

        states = generateAutomata(p, q, b, ASet, BSet, verbose)
        result, toPath = getMinimalPaths(p, q, states, b, ASet, BSet, False)
        if result:
            print(p, q, result[0], result[1], flush=True)
        else:
            print(p, q, -1, -1, flush=True)

        if saveStates:
            with open("_".join(map(str, sys.argv[1:6]))+"_automata.pickle", "wb") as f:
                pickle.dump(states, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        info()
