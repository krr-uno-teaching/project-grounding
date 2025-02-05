from abc import ABC, abstractmethod
from typing import AbstractSet, Optional, Sequence

from clingo.ast import AST, ASTType, parse_files
from clingo.symbol import Symbol
from instantiator import Instantiator
from rule import Rule
from tarjan import Graph
from util import body_symbolic_atoms, head_symbolic_atoms


def sccs_to_str(sccs: list[list[AST]]) -> str:
    """
    Convert a list of strongly connected components to a string.
    """
    return ("\n" + "-" * 60 + "\n").join(
        "\n".join(str(rule) for rule in scc) for scc in sccs
    )


class Grounder(ABC):
    def __init__(self, instantiator: Optional[Instantiator] = None) -> None:
        self._program: list[AST] = []
        if not instantiator:
            instantiator = Instantiator()
        self.instantiator = instantiator

    def __append_rule_to_program_ast(self, stm: AST) -> None:
        if stm.ast_type == ASTType.Rule:
            self._program.append(stm)

    def add_files(self, files: Sequence[str]):
        parse_files(files, self.__append_rule_to_program_ast)

    def ground(self) -> list[Rule]:
        return self._grounding_algorithm(self._program)[0]

    @abstractmethod
    def _grounding_algorithm(
        self, program: list[AST], atoms: AbstractSet[Symbol] = frozenset()
    ) -> tuple[list[Rule], set[Symbol]]:
        pass


class BottomUpGrounder(Grounder):
    def _grounding_algorithm(
        self, program: list[AST], atoms: AbstractSet[Symbol] = frozenset()
    ) -> tuple[list[Rule], set[Symbol]]:
        """
        Grounds a program bottom up.
        """
        # YOUR CODE HERE
        raise NotImplementedError


def depends(rule2: AST, rule1: AST) -> bool:
    """
    Check if rule2 depends on rule1. This is the case if the there is an atom in the body of rule2
    with the same name and number of arguments as an atom in the head of rule1.
    """
    assert rule2.ast_type == ASTType.Rule
    assert rule1.ast_type == ASTType.Rule
    # YOUR CODE HERE
    raise NotImplementedError


def dependency_graph(program: Sequence[AST]) -> tuple[Graph[AST], list[AST]]:
    """
    Compute the dependency graph of a program using the depends function defined above.
    It returs such a graph and a list of rules that have no dependencies with any other rules.
    """
    # YOUR CODE HERE
    raise NotImplementedError


def strongly_connected_components(program: Sequence[AST]) -> list[list[AST]]:
    """
    Compute the strongly connected components of a program. The strongly connected components are
    returned in topological order.
    """
    # YOUR CODE HERE
    raise NotImplementedError


class GrounderWithDependencies(Grounder):
    def __init__(self, instantiator: Optional[Instantiator] = None) -> None:
        super().__init__(instantiator)
        self.bootom_up_grounder = BottomUpGrounder(self.instantiator)

    def _grounding_algorithm(
        self, program: list[AST], atoms: AbstractSet[Symbol] = frozenset()
    ) -> tuple[list[Rule], set[Symbol]]:
        """
        Ground a program bottom up using the dependency graph.
        """
        # YOUR CODE HERE
        raise NotImplementedError
