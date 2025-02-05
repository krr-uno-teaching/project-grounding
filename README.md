# Grounding Project
In this assignment, you will build a grounder form normal programs.

## Formalities.
You can work on the solution alone or in groups of two people. Different groups have to submit different solutions, in case of plagiarism all groups involved will fail the project.

Before you start create a file ```group.txt``` with the names and NUIDs of the components of the group. If you are working alone, the file should contain a single line with your name. If you are working in a group, the file should contain two lines with the names of the two members of the group. The file should be located in the root directory of the repository and it should have the following format:
```
Vladimir lifschitz NUID: 00000001
Michael Gelfond    NUID: 00000002
```
Do not write anything else in this file nor use any other format! Blank spaces do not matter for the format.

Your code will be autograded for technical correctness. However, the correctness of your implementation -- not the autograder's judgments -- will be the final judge of your score. If necessary, we will review and grade assignments individually to ensure that you receive due credit for your work.

The content of the **main** branch of your GitHub repository at the time of the deadline will be considered your submission. Any modifications after deadline will be ignored. So will be any previous code that you committed before. Note that the autograder will give you the evaluation of your last commit, so be sure that it is what you expected.

**Start as soon as possible to avoid running out of time.**

Do not modify the file ```autograder.py``` nor any of the content of the directories ```.git```, ```.github```, ```img```, ```questions``` and ```tests```. Modifying some of this directories may prevent your code to work or cause lost of your progress.

**Academic Dishonesty**: We will be checking your code against other submissions in the class for logical redundancy. If you copy someone else's code and submit it with minor changes, we will know. These cheat detectors are quite hard to fool, so please don't try. Modifying the behavior of the autograder in any way is also cheating. We trust you all to submit your own work only and to do it in honest way; please don't let us down. If you do, we will pursue the strongest consequences available to us.

## Framework

This project requires Python 3.9 or higher and the ```clingo``` Python package with a version 5.6.2. You can check your installation by running the following commands:
```bash
python --version
python -c "import clingo; print(clingo.__version__)"
```
If you are missing the ```clingo``` package, you can install it with ```pip```:
```bash
python -m pip install clingo==5.6.2
```
You will also need the ```clingox``` package , you can install it with ```pip```:
```bash
python -m pip install clingox==1.2.0
```

The framework is composed of the following files:
| file             | description           |
| ---------------- | ----------------------|
| algorithms.py    | The file where you will implement the algorithms. This is the only file that you need to modify |
| grounder.py      | This is the main application file that you will run |
| instantiator.py  | This file contains code that grounds a single rule and that you will use to help develop you grounding algorithms |
| rule.py          | Contains the class Rule to represent ground rules |
| tarjan.py        | Contains the class Graph and code that computes the strongly connected components of the graph |
| util.py          | Contains helpful function to simplify you code |
| autograder.py    | The autrograder |

The ```grounder.py``` program contains three main subcommands
The framework is composed of the following files:
| subcomand             | description           |
| ---------------- | ----------------------|
| ground    | Grounds a logic program |
| graph     | Computes and prints the dependency graph of a logic program |
| sccs      | Computes and prints the strongly connected components of a logic program |

None of these commands will work when you first download the framework. You will need to implement the algorithms in ```algorithms.py``` to make them work. Once you have completed an algorithm, you can test it by running ```grounder.py``` with the corresponding subcommand. For instance, you can use the command
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}
```
To ground the program ```tests/ex/hc/encoding.lp``` with the instance ```tests/ex/hc/instance01.lp```. The output of the command will be the grounded program. This is the example saw in class.


Do not modify any file besides ```algorithms.py```. Modifying other files may cause the autograder to fail. You can add new files if you want.

We recommend that you create new commits frequently when doing the rest of this project. If at some point you realize you did a mistake, you can revert to a previous commit. Pushing to the GitHub repository may also help you in case that you accidentally lose your local copy. If you have doubts about Git or Github, or you can learn more about it, you can read the tutorial in following link:

https://github.com/Advanced-Concepts-Programming-Languages/github-starter-course

When submitting questions to the instructors be sure that your most recent code has been commited and pushed to GitHub. Send the link to your repository. Feedback may be added to your code in GitHub.

## Question 1: Bottom-up grounding (30 points)
To begin with, you will be implemented the **bottom-up grounding** algorithm saw in class.
The ```algorithms.py``` file contains an abstract class ```Grounder``` and a subclass called ```BottomUpGrounder```.

The ```Grounder``` class contains attribute ```instantiator``` which has the method
```python
def ground_rule(self, rule: AST, atoms: set[Symbol] = frozenset()) -> list[Rule]:
```
This method allows us to ground a single rule with respect to a set of atoms. For instance, if ```rule``` is an ```AST``` object representing rule
```
a(X) :- b(X), not c(X).
```
and ```atoms``` is a set of symbols ```a(1), b(1), b(2), b(3)```, then the call
```python
self.instantiator.ground_rule(rule, atoms)
```
returns a list containing a ```Rule``` object representing the following rules:
```
a(1) :- b(1), not c(1).
a(2) :- b(2), not c(2).
a(3) :- b(3), not c(3).
```
You can access the head of any ```Rule``` object by accessing the attribute ```head```.
For instance, if ```rule``` is a ```Rule``` object representing rule ```a(1) :- b(1), not c(1)```, then ```rule.head``` will return a list of size one containing the symbol ```a(1)```.
Note that ```rule.head``` may be an empty list in the case that ```rule``` is a constraint.

This class also has an abstract method ```_grounding_algorithm()``` that will be instantiated by its subclasses.
```python
def _grounding_algorithm(
    self, program: list[AST], atoms: set[Symbol] = frozenset()
) -> tuple[list[Rule], set[Symbol]]:
```
**You should not modify class ```Grounder```.**
The class that you should modify to implement the bottom-up algorithm is the ```BottomUpGrounder```. In particular, you should write you code in the method ```_grounding_algorithm()```.
This method receives a list of ```AST``` objects representing the ```program``` and a set of ```Symbol``` objects that represent the current set of relevant atoms.
It should return a pair.
The first component of this pair is the list of ground rules resulting for ground ```program``` with respect to ```atoms```.
The second component of this pair is the set of head atoms occurring in the head of all rules in ```program```.

You can see the result of your algorithm by running
```sh
python grounder.py ground tests/ex/pr01.lp
```
The result should look like
```
a(1).
b(1).
b(2).
b(3).
a(1) :- b(1), not c(1).
a(2) :- b(2), not c(2).
a(3) :- b(3), not c(3).
```
The order in which rules appear does not matter. You also can test the class example
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}
```
This should print 60 rules. You can count the number of rules with the commands
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp} | wc -l
```
You can finally check your code using the autograder by running command
```sh
python autograder.py --question=1
```

## Question 2: Strongly connected components (40 points)
In this question, you will implement the dependency graph of a program and obtain the strongly connected components of this graph in topological order. For this project, we will use only the dependency graph of the program, not the positively dependency graph. As a result, our algorithm will be slightly simpler than the one saw in class, though also slightlty less efficient.


### Question 2a: Rule dependencies (10 points)

As a first step to implement the dependency graph, you will add the code when a rule depends on another rule to the function
```python
def depends(rule1: AST, rule2: AST) -> bool:
```
in the ```algorithms.py``` file. This function receives two ```AST``` objects representing two rules and returns ```True``` if ```rule1``` depends on ```rule2```. Otherwise, it returns ```False```.

Recall from class that ```rule1``` **depends** on ```rule2``` if if there is an atom ```b``` in the body of ```rule1``` and an atom ```h``` in the head of ```rule2``` such that ```h``` **unifies** with ```b```. **For this project we will use a relaxation of this condition**. We will say that ```rule1``` **depends** on ```rule2``` if there is an atom ```b``` in the body of ```rule1``` and an atom ```h``` in the head of ```rule2``` such that ```a``` and ```b``` have the same name and the same arity (number of arguments). For instance, if ```rule1``` is the rule
```
on_path(Y) :- path(X,Y), path(Y,Z).
```
and ```rule2``` is the rule
```
path(X,Y) :- not omit(X,Y), edge(X,Y).
```
we say that ```rule1``` depends on ```rule2``` because ```path(X,Y)``` and ```path(Y,Z)``` (or ```path(X,Y)```) have the same name and the same arity. The call ```depends(rule1, rule2)``` returns ```True```. On the other hand,
the call ```depends(rule2, rule1)``` returns ```False```. To see the difference with the unification-based definition, consider the following example.
Let ```rule3``` be the rule
```
holds(path,X,Y) :- not holds(omit,X,Y), holds(edge,X,Y).
```
Under the definition used in this project ```rule3``` depends on itself. However, under the unification-based definition, ```rule3``` does not, becase ```holds(path,X,Y)``` does unify neither with ```holds(omit,X,Y)``` nor with ```holds(edge,X,Y)``` .

To help you in the implementation of this function, file ```utils.py``` contains functions
```python
def head_symbolic_atoms(rule: AST) -> List[AST]:
def body_symbolic_atoms(rule: AST) -> List[AST]:
```
These two rules receive as argument an ```AST``` object representing a rule and return a list of ```AST``` objects representing the head and body atoms, respectively. For instance, if ```rule``` is the rule
```
on_path(Y) :- path(X,Y), path(Y,Z).
```
the first function will return a list with a unique ```AST``` object representing the atom ```path(Y)```. The second function will return a list with two ```AST``` objects representing the atoms ```path(X,Y)``` and ```path(Y,Z)```.
You can access the name of each atom with the attribute ```name``` and the list of arguments with the attribute ```arguments```. For instance, if ```atom``` is the ```AST``` object representing the atom ```path(X,Y)```, then ```atom.name``` is the string ```"path"``` and ```atom.arguments``` is a list of two ```AST``` objects representing variables ```X``` and ```Y```.

You can check your code using the autograder by running command
```sh
python autograder.py --question=2a
```

### Question 2b: Dependency graph (20 points)

In this question, you will implement the dependency graph of a program in the function
```python
def dependency_graph(program: Sequence[AST]) -> tuple[Graph[Rule], list[Rule]]:
```
in the ```algorithms.py``` file. This function receives a list of ```AST``` objects representing a program and returns a pair. The first component of this pair is a ```Graph``` object representing the dependency graph of the program. The second component of this pair is a list of ```Rule``` objects representing the rules in the program that neither depend on any other rule nor any other rule depends on them. You can ignore this second component for this question, for instance by simply returning the empty list. We will pick it up in [Question 2d](#question-2d-taking-care-of-rules-without-dependencies-5-points).

The ```tarjan.py``` file contains the class ```Graph``` that you should use for building the returned dependency graph. You can create a new graph simply by calling the constructor without arguments ```Graph()```. The class ```Graph``` has the method:
```python
def add_edge(self, rule1: Rule, rule2: Rule) -> None:
```
This method adds an edge from vertex ```rule1``` to vertex ```rule2```. If the vertices ```rule1``` and ```rule2``` do not exist in the graph, they are created. This is the only method from this class that you need to use to build the dependency graph. You can obtain a string representation of a ```graph``` by calling the method ```str(graph)```. For instance, for the Hamiltonian cycle example saw in class, you should obtain the following string representation:
```
"path(X,Y) :- not omit(X,Y); edge(X,Y)."        ==>      "omit(X,Y) :- not path(X,Y); edge(X,Y)."
"path(X,Y) :- not omit(X,Y); edge(X,Y)."        ==>      "#false :- path(X,Y); path(X',Y); X < X'."
"path(X,Y) :- not omit(X,Y); edge(X,Y)."        ==>      "#false :- path(X,Y); path(X,Y'); Y < Y'."
"path(X,Y) :- not omit(X,Y); edge(X,Y)."        ==>      "on_path(Y) :- path(X,Y); path(Y,Z)."
"path(X,Y) :- not omit(X,Y); edge(X,Y)."        ==>      "reach(Y) :- reach(X); path(X,Y)."
"omit(X,Y) :- not path(X,Y); edge(X,Y)."        ==>      "path(X,Y) :- not omit(X,Y); edge(X,Y)."
"on_path(Y) :- path(X,Y); path(Y,Z)."           ==>      "#false :- node(X); not on_path(X)."
"reach(Y) :- reach(X); path(X,Y)."              ==>      "reach(Y) :- reach(X); path(X,Y)."
"reach(Y) :- reach(X); path(X,Y)."              ==>      "#false :- node(X); not reach(X)."
"reach(X) :- start(X)."                         ==>      "reach(Y) :- reach(X); path(X,Y)."
"reach(X) :- start(X)."                         ==>      "#false :- node(X); not reach(X)."
```
Each line represents an edge in the graph. The origin vertex is the one on the left of the arrow and the destination vertex is the one on its right. You also can see the result of your algorithm by running
```sh
python grounder.py graph tests/ex/hc/encoding.lp
```
The result should be the one shown above.

You can check your code using the autograder by running command
```sh
python autograder.py --question=2b
```

### Question 2c: Strongly connected components (5 points)

For this question, you implement the code for obtaining the strongly connected components in topological order in the function
```python
def strongly_connected_components(program: Sequence[AST]) -> list[list[AST]]:
```
in the ```algorithms.py``` file. This function receives a list of ```AST``` objects representing a program and returns a list of lists of ```AST``` objects representing the strongly connected components of the program in topological order. Each list of ```AST``` objects represents a strongly connected component. The first list of ```AST``` objects represents the strongly connected component that does not depend on any other strongly connected component. The second list of ```AST``` objects represents the strongly connected component that does not depend on any other strongly connected component except the first one. And so on.

For instance, for the Hamiltonian cycle example saw in class, you should obtain something like the following.
```
reach(X) :- start(X).
------------------------------------------------------------
path(X,Y) :- not omit(X,Y); edge(X,Y).
omit(X,Y) :- not path(X,Y); edge(X,Y).
------------------------------------------------------------
reach(Y) :- reach(X); path(X,Y).
------------------------------------------------------------
#false :- node(X); not reach(X).
------------------------------------------------------------
on_path(Y) :- path(X,Y); path(Y,Z).
------------------------------------------------------------
#false :- node(X); not on_path(X).
------------------------------------------------------------
#false :- path(X,Y); path(X,Y'); Y < Y'.
------------------------------------------------------------
#false :- path(X,Y); path(X',Y); X < X'.
```
Each line separates different strongly connected componnents and these componnents are printed in topological order. Once you complete this question, you can print the result of your algorithm in this example by running
```sh
python grounder.py sccs tests/ex/hc/encoding.lp
```
Note that you may obtain the same strongly connected components in a slightly different order, as the topological order is not unique. Note also that rules
```
omit(X,Y) :- not path(X,Y); edge(X,Y).
path(X,Y) :- not omit(X,Y); edge(X,Y).
```
are in the same strongly connected component. You may noitice that this is different from what we saw in class. This difference is due to the fact that we are not using the positive dependency graph to further split the strongly connected components.


To obtain this list, you can use the function ```dependency_graph()``` you implemented in [Question 2b](#question-2b-dependency-graph-20-points) and the function
```python
def sccs(self) -> list[list[T]]:
```
from the ```Graph``` class in file ```tarjan.py```. You can check your code using the autograder by running command
```sh
python grounder.py sccs tests/ex/hc/encoding.lp
```
The result should be the one shown above.

You can check your code using the autograder by running command
```sh
python autograder.py --question=2c
```

### Question 2d: Taking care of rules without dependencies (5 points)

In this question, you will revisit the code in the previous questions and ensure that rules that neither depend on any other rule nor any other rule depends on them are also included in the strongly connected components. To do so, you will modify the function ```dependency_graph()``` and ensure that the second component of the pair returned by the function is the list of these rules. You may also need to modify the function ```strongly_connected_components()``` to ensure that the list of strongly connected components returned by the previous function is handled correctly.

You can check your code using the autograder by running command
```sh
python autograder.py --question=2d
```

## Question 3: Grounding using dependencies (30 points)

You will implement now the grounding algorithm that takes into account the dependencies between rules. The algorithm is described in the lecture slides. You will implement the code in the function ```_grounding_algorithm()``` of the ```GrounderWithDependencies``` class. The code for this class is also in the file ```algorithms.py```.

To implement this algorithm you will need to use your implementation of the bottom up grounder from [Question 1](#question-1-bottom-up-grounding-30-points). The class ```GrounderWithDependencies``` already has an attribute ```bootom_up_grounder``` that contains an instance of the ```BottomUpGrounder``` class.
You should use this instance to ground rules when you need o call the bottom up grounder. Do not create a new instance of the ```BottomUpGrounder``` class. Doing so will cause the autograder to fail!



You can see the result of you algorithm by running
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp} --algorithm=dependencies
```
This should print 60 rules.
 You can count the number of rules with the commands
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp} --algorithm=dependencies | wc -l
```
These are the same 60 rules that are obtained with the bottom up algorithm. To see the difference between the two algorithms, you need to look at the number of rules that are computed during the process, instead of the final result. You can do this by running commands
```sh
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}  --all-computed-rules --algorithm=bottom-up
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}  --all-computed-rules --algorithm=dependencies
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}  --all-computed-rules --algorithm=bottom-up | wc -l
python grounder.py ground tests/ex/hc/{encoding.lp,instance01.lp}  --all-computed-rules --algorithm=dependencies | wc -l
```
You can finally check your code using the autograder by running command
```sh
python autograder.py --question=3
```


**Be sure you have committed your changes, pushed them to the GitHub repository and see the grade you expected to receive in the Actions tab in GitHub.**
