import unittest

from clingo.symbol import Function, Number
from instantiator import Instantiator, _encode_rule
from util import parse_statement


class TestCase(unittest.TestCase):
    def test_fact(self):
        instantiator = Instantiator()
        self.assertEqual(
            str(instantiator._ground_rule(parse_statement("node(a)."))[0]), "node(a)."
        )
        self.assertEqual(
            str(instantiator._ground_rule(parse_statement("edge(a,b)."))[0]),
            "edge(a,b).",
        )
        self.assertEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            [],
        )

    def test_fact2(self):
        instantiator = Instantiator()
        self.assertEqual(
            str(instantiator.ground_rule(parse_statement("node(a)."))[0]), "node(a)."
        )
        self.assertEqual(
            str(instantiator.ground_rule(parse_statement("edge(a,b)."))[0]),
            "edge(a,b).",
        )
        self.assertEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            ["node(a).", "edge(a,b)."],
        )

    def test_rules_(self):
        instantiator = Instantiator()
        atoms = [
            Function("b", [Number(1)]),
            Function("b", [Number(2)]),
            Function("b", [Number(3)]),
            Function("a", [Number(1)]),
        ]
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator._ground_rule(
                    parse_statement("a(X) :- b(X)."), atoms
                )
            ],
            ["a(3) :- b(3).", "a(2) :- b(2).", "a(1) :- b(1)."],
        )
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator._ground_rule(
                    parse_statement("b(X) :- a(X)."), atoms
                )
            ],
            ["b(1) :- a(1)."],
        )
        self.assertEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            [],
        )

    def test_rules(self):
        instantiator = Instantiator()
        atoms = [
            Function("b", [Number(1)]),
            Function("b", [Number(2)]),
            Function("b", [Number(3)]),
            Function("a", [Number(1)]),
        ]
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator.ground_rule(
                    parse_statement("a(X) :- b(X)."), atoms
                )
            ],
            ["a(3) :- b(3).", "a(2) :- b(2).", "a(1) :- b(1)."],
        )
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator.ground_rule(
                    parse_statement("b(X) :- a(X)."), atoms
                )
            ],
            ["b(1) :- a(1)."],
        )
        self.assertEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            ["a(3) :- b(3).", "a(2) :- b(2).", "a(1) :- b(1).", "b(1) :- a(1)."],
        )

    def test_encode_rule(self):
        rule = _encode_rule(parse_statement("a(X) :- b(X), not c(X), not d(X)."))
        self.assertEqual(str(rule), "bc(X); bd(X); ha(X) :- b(X).")

    def test_negation(self):
        instantiator = Instantiator()
        atoms = [
            Function("b", [Number(1)]),
            Function("b", [Number(2)]),
            Function("b", [Number(3)]),
            Function("a", [Number(1)]),
        ]
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator.ground_rule(
                    parse_statement("a(X) :- b(X), not c(X), not d(X)."), atoms
                )
            ],
            [
                "a(3) :- b(3), not c(3), not d(3).",
                "a(2) :- b(2), not c(2), not d(2).",
                "a(1) :- b(1), not c(1), not d(1).",
            ],
        )
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator.ground_rule(
                    parse_statement("b(X) :- a(X)."), atoms
                )
            ],
            ["b(1) :- a(1)."],
        )
        self.assertCountEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            [
                "a(3) :- b(3), not c(3), not d(3).",
                "a(2) :- b(2), not c(2), not d(2).",
                "a(1) :- b(1), not c(1), not d(1).",
                "b(1) :- a(1).",
            ],
        )
        self.assertCountEqual(
            [
                str(rule)
                for rule in instantiator.ground_rule(
                    parse_statement("a1(X), a2(X) :- b(X)."), atoms
                )
            ],
            ["a1(3); a2(3) :- b(3).", "a1(2); a2(2) :- b(2).", "a1(1); a2(1) :- b(1)."],
        )
        self.assertCountEqual(
            [str(rule) for rule in instantiator.grounded_rules],
            [
                "a(3) :- b(3), not c(3), not d(3).",
                "a(2) :- b(2), not c(2), not d(2).",
                "a(1) :- b(1), not c(1), not d(1).",
                "b(1) :- a(1).",
                "a1(3); a2(3) :- b(3).",
                "a1(2); a2(2) :- b(2).",
                "a1(1); a2(1) :- b(1).",
            ],
        )
