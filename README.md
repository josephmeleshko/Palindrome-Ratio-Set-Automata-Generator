# Palindrome Ratio Set Automata Generator

Let $$PAL_k \subset \mathbb{N}$$ be the set of integers that are palindromes in base $k$.
Let $$APAL_k \subset \mathbb{N}$$ be the set of integers that are antipalindromes in base $k$.
Given $$A, B \subseteq \mathbb{N}$$, let $$A/B = \{a/b \mid a \in A, b \in B - \{0\}\}$$ be the ratio set of $$A$$ and $$B$$.
This code builds a finite automaton for a given $$p,q \in \mathbb{N}$$ and $$A, B \in \{PAL, APAL\}$$ that accepts pairs $$\langle a,b\rangle$$ such that $$a \in A, b \in B$$ and $$a/b = p/q$$.

More information on the algorithm and results can be found at <<LINK TO ARXIV HERE>>.

Basic usage is
```python
python3 PalindromeRatioAutomataGenerator.py p q base ASet BSet verbose? saveStates?
```
Where
- $$p$$, $$q$$ and $$base$$ are integers such that $$p > q$$ and $$base > 1$$.
- $$ASet, BSet \in \{``pal", ``apal"\}$$. (To choose between palindromes and antipalindromes.)
- verbose is a boolean for extra debug input.
- saveStates is a boolean that saves the produced automata as a pickled python dictionary.

and it prints,
```
p q A B
```
where $$A \in ASet, B \in BSet$$ and $$A$$ and $$B$$ are minimal such that $$A/B = p/q$$.

To directly build and work with the produced automaton, use
```python
PalindromeRatioAutomataGenerator.generateAutomata(p, q, b, ASet, BSet, verbose)
```
which returns a dictionary where the keys are states and the values are lists which have the transitions and where they lead.

For bulk processing to reproduce our general results,
```python
python3 bulkInteger.py start stop base ASet BSet threads
```
which prints
```
p A B
```
as above with $$q = 1$$ for $$start \leq p < stop$$ using $$threads$$ threads.
Or alternatively,
```python
python3 bulkRational.py start stop base ASet BSet threads
```
which prints
```
p q A B
```
for $$start \leq p < stop$$, $$1 \leq q < p$$, and $$\operatorname{gcd}(p, q) = 1$$.

The bulk processing scripts use python's multiprocessing for multithreading and tqdm for ongoing progress information but the main automata generator only uses basic python.
Pypy seems to significantly speed up processing but isn't necessary.
