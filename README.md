# Palindrome Ratio Set Automata Generator

Let <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/6154537fab020032645292c797182864.svg?invert_in_darkmode" align=middle width=78.23056725pt height=13.7899245pt/></p> be the set of integers that are palindromes in base <img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.075367949999992pt height=22.831056599999986pt/>.
Let <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/071ae9037d1df7744561261516c0793d.svg?invert_in_darkmode" align=middle width=90.55936559999999pt height=13.7899245pt/></p> be the set of integers that are antipalindromes in base <img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/63bb9849783d01d91403bc9a5fea12a2.svg?invert_in_darkmode" align=middle width=9.075367949999992pt height=22.831056599999986pt/>.
Given <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/f0e4363d806f3a896fc59cc4d255d263.svg?invert_in_darkmode" align=middle width=66.7178952pt height=14.52054615pt/></p>, let <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/d11449b0c236ebbd671557070878f99a.svg?invert_in_darkmode" align=middle width=243.4621728pt height=16.438356pt/></p> be the ratio set of <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/9fe95515a9500cc7779b059643c7c7ce.svg?invert_in_darkmode" align=middle width=12.32879835pt height=11.232861749999998pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/83ff68299814eab9602cad34b564ae2a.svg?invert_in_darkmode" align=middle width=13.2934098pt height=11.232861749999998pt/></p>.
This code builds a finite automaton for a given <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/d5a576ca7800c541bcca77f60e8bd68b.svg?invert_in_darkmode" align=middle width=55.467853649999995pt height=14.52054615pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/e94fc246c4f51e9e8cdbf2c03677f5ff.svg?invert_in_darkmode" align=middle width=161.79794895pt height=16.438356pt/></p> that accepts pairs <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/dc0711ea2b7aef9dff2edbda5f9b7392.svg?invert_in_darkmode" align=middle width=35.835267599999995pt height=16.438356pt/></p> such that <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/bc6cc0801152a6f0e414db09afc486de.svg?invert_in_darkmode" align=middle width=88.85431829999999pt height=14.611878599999999pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/3b52ef2a6896d07a4ddbeada1b91c0f7.svg?invert_in_darkmode" align=middle width=70.29867239999999pt height=16.438356pt/></p>.

More information on the algorithm and results can be found at <<LINK TO ARXIV HERE>>.

Basic usage is
```python
python3 PalindromeRatioAutomataGenerator.py p q base ASet BSet verbose? saveStates?
```
Where
- <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/3ceb13107024b0fcb56c22464beee0a1.svg?invert_in_darkmode" align=middle width=8.27056725pt height=10.2739725pt/></p>, <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/5ea75157477d5d4abab688eea47348b8.svg?invert_in_darkmode" align=middle width=7.92810645pt height=10.2739725pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/edf787010429c5cbc8115c7ac7b56257.svg?invert_in_darkmode" align=middle width=31.103567549999998pt height=11.4155283pt/></p> are integers such that <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/4fcccaed053977b00a3913c0bd2c7a76.svg?invert_in_darkmode" align=middle width=38.1163035pt height=12.05823135pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/a854c76e23e8bbece2e59498126f7917.svg?invert_in_darkmode" align=middle width=61.24040834999999pt height=12.05823135pt/></p>.
- <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/47fcf67d06e7a6aeed6266c106a23861.svg?invert_in_darkmode" align=middle width=211.94088299999999pt height=16.438356pt/></p>. (To choose between palindromes and antipalindromes.)
- verbose is a boolean for extra debug input.
- saveStates is a boolean that saves the produced automata as a pickled python dictionary.

and it prints,
```
p q A B
```
where <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/c4999c34b05ce9fa7639bb96f240c411.svg?invert_in_darkmode" align=middle width=147.96779909999998pt height=14.42921205pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/9fe95515a9500cc7779b059643c7c7ce.svg?invert_in_darkmode" align=middle width=12.32879835pt height=11.232861749999998pt/></p> and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/83ff68299814eab9602cad34b564ae2a.svg?invert_in_darkmode" align=middle width=13.2934098pt height=11.232861749999998pt/></p> are minimal such that <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/f5d9bc6bea154888ee11852636a25d75.svg?invert_in_darkmode" align=middle width=80.17692539999999pt height=16.438356pt/></p>.

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
as above with <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/2b887f4560f00371798ab9ddb7083700.svg?invert_in_darkmode" align=middle width=38.06492745pt height=13.789957499999998pt/></p> for <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/b1e3f30ddcc18985ddbb231609cab84d.svg?invert_in_darkmode" align=middle width=118.12580505pt height=13.650669449999999pt/></p> using <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/81648d2a487c8cb1a45da834721178a1.svg?invert_in_darkmode" align=middle width=55.8849027pt height=11.4155283pt/></p> threads.
Or alternatively,
```python
python3 bulkRational.py start stop base ASet BSet threads
```
which prints
```
p q A B
```
for <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/b1e3f30ddcc18985ddbb231609cab84d.svg?invert_in_darkmode" align=middle width=118.12580505pt height=13.650669449999999pt/></p>, <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/e49ece15ceea1599ae1d023c38b34183.svg?invert_in_darkmode" align=middle width=68.2531245pt height=13.789957499999998pt/></p>, and <p align="center"><img src="https://rawgit.com/josephmeleshko/Palindrome-Ratio-Set-Automata-Generator/main/svgs/17269597a171151611862d395e0d9db4.svg?invert_in_darkmode" align=middle width=91.0843956pt height=16.438356pt/></p>.

The bulk processing scripts use python's multiprocessing for multithreading and tqdm for ongoing progress information but the main automata generator only uses basic python.
Pypy seems to significantly speed up processing but isn't necessary.
