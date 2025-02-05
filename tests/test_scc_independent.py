import unittest

from algorithms import strongly_connected_components
from clingo import ast
from util import parse_statement


def occurs_before(
    sccs: list[list[ast.AST]], scc1: list[ast.AST], scc2: list[ast.AST]
) -> bool:
    """
    Check if scc1 occurs before scc2 in the list of strongly connected components sccs.
    """
    sccs = [sorted(scc) for scc in sccs]
    scc1_index = sccs.index(sorted(scc1))
    scc2_index = sccs.index(sorted(scc2))
    return scc1_index < scc2_index


class TestSCCs(unittest.TestCase):
    def test_scc(self):
        rule0 = parse_statement("edge(1,2).")
        rule1 = parse_statement("omit(X,Y) :- not path(X,Y), edge(X,Y).")
        rule2 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        rule3 = parse_statement(":- path(X,Y), path(X',Y), X < X'.")
        rule4 = parse_statement(":- path(X,Y), path(X,Y'), Y < Y'.")
        rule5 = parse_statement("on_path(Y) :- path(X,Y), path(Y,Z).")
        rule6 = parse_statement(":- node(X), not on_path(X).")
        rule7 = parse_statement("reach(X) :- start(X).")
        rule8 = parse_statement("reach(Y) :- reach(X), path(X,Y).")
        rule9 = parse_statement(":- node(X), not reach(X).")
        rule10 = parse_statement("a.")
        program = [
            rule0,
            rule1,
            rule2,
            rule3,
            rule4,
            rule5,
            rule6,
            rule7,
            rule8,
            rule9,
            rule10,
        ]
        sccs = strongly_connected_components(program)
        sccs = [sorted(scc) for scc in sccs]
        self.assertIn([rule0], sccs)
        self.assertIn([rule1, rule2], sccs)
        self.assertIn([rule3], sccs)
        self.assertIn([rule4], sccs)
        self.assertIn([rule5], sccs)
        self.assertIn([rule6], sccs)
        self.assertIn([rule7], sccs)
        self.assertIn([rule8], sccs)
        self.assertIn([rule9], sccs)
        self.assertIn([rule10], sccs)
        self.assertCountEqual(
            sccs,
            [
                [rule0],
                [rule1, rule2],
                [rule3],
                [rule4],
                [rule5],
                [rule6],
                [rule7],
                [rule8],
                [rule9],
                [rule10],
            ],
        )
        self.assertTrue(occurs_before(sccs, [rule0], [rule1, rule2]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule3]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule4]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule5]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule6]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule8]))
        self.assertTrue(occurs_before(sccs, [rule0], [rule9]))

        self.assertTrue(occurs_before(sccs, [rule1, rule2], [rule3]))
        self.assertTrue(occurs_before(sccs, [rule1, rule2], [rule4]))
        self.assertTrue(occurs_before(sccs, [rule1, rule2], [rule5]))
        self.assertTrue(occurs_before(sccs, [rule1, rule2], [rule8]))
        self.assertTrue(occurs_before(sccs, [rule1, rule2], [rule9]))

        self.assertTrue(occurs_before(sccs, [rule5], [rule6]))

        self.assertTrue(occurs_before(sccs, [rule7], [rule8]))
        self.assertTrue(occurs_before(sccs, [rule7], [rule9]))

        self.assertTrue(occurs_before(sccs, [rule8], [rule9]))

    def test_independend_scss(self):
        rule0 = parse_statement("a.")
        rule1 = parse_statement("b.")
        program = [rule0, rule1]
        sccs = strongly_connected_components(program)
        self.assertIn([rule0], sccs)
        self.assertIn([rule1], sccs)
