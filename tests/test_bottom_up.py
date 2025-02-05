import os
import unittest

from algorithms import BottomUpGrounder
from clingo.symbol import Function, Number
from util import parse_program


class TestGroundBottomUp(unittest.TestCase):
    def test_fact(self):
        grounder = BottomUpGrounder()
        self.assertEqual(
            str(grounder._grounding_algorithm(parse_program("node(a)."))[0][0]),
            "node(a).",
        )
        self.assertEqual(
            str(grounder._grounding_algorithm(parse_program("edge(a,b)."))[0][0]),
            "edge(a,b).",
        )

    def test_rules_basic(self):
        grounder = BottomUpGrounder()
        atoms = [
            Function("b", [Number(1)]),
            Function("b", [Number(2)]),
            Function("b", [Number(3)]),
            Function("a", [Number(1)]),
        ]
        self.assertCountEqual(
            [
                str(rule)
                for rule in grounder._grounding_algorithm(
                    parse_program("a(X) :- b(X)."), atoms
                )[0]
            ],
            ["a(3) :- b(3).", "a(2) :- b(2).", "a(1) :- b(1)."],
        )
        self.assertCountEqual(
            [
                str(rule)
                for rule in grounder._grounding_algorithm(
                    parse_program("b(X) :- a(X)."), atoms
                )[0]
            ],
            ["b(1) :- a(1)."],
        )

    def test_rules_and_facts(self):
        grounder = BottomUpGrounder()
        self.assertCountEqual(
            [
                str(rule)
                for rule in grounder._grounding_algorithm(
                    parse_program("a(X) :- b(X). b(1). b(2). b(3).")
                )[0]
            ],
            [
                "a(3) :- b(3).",
                "a(2) :- b(2).",
                "a(1) :- b(1).",
                "b(1).",
                "b(2).",
                "b(3).",
            ],
        )

        self.assertCountEqual(
            [
                str(rule)
                for rule in grounder._grounding_algorithm(
                    parse_program("a(X) :- b(X). b(1). b(2). b(3). a(1).")
                )[0]
            ],
            [
                "a(3) :- b(3).",
                "a(2) :- b(2).",
                "a(1) :- b(1).",
                "b(1).",
                "b(2).",
                "b(3).",
                "a(1).",
            ],
        )

        self.assertCountEqual(
            [
                str(rule)
                for rule in grounder._grounding_algorithm(
                    parse_program("b(X) :- a(X). b(1). b(2). b(3). a(1).")
                )[0]
            ],
            ["b(1) :- a(1).", "b(1).", "b(2).", "b(3).", "a(1)."],
        )


class TestGrounder_GroundBottomUp(unittest.TestCase):
    def test_grounder_hc(self):
        grounder = BottomUpGrounder()
        path = os.path.dirname(__file__)
        path = os.path.join(path, "ex", "hc")
        encoding = os.path.join(path, "encoding.lp")
        instance = os.path.join(path, "instance01.lp")
        grounder.add_files([encoding, instance])
        expected_result = """
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            path(d,a) :- edge(d,a), not omit(d,a).
            path(a,c) :- edge(a,c), not omit(a,c).
            path(a,b) :- edge(a,b), not omit(a,b).
            path(c,a) :- edge(c,a), not omit(c,a).
            path(c,d) :- edge(c,d), not omit(c,d).
            path(b,d) :- edge(b,d), not omit(b,d).
            path(b,c) :- edge(b,c), not omit(b,c).
            omit(d,a) :- edge(d,a), not path(d,a).
            omit(a,c) :- edge(a,c), not path(a,c).
            omit(a,b) :- edge(a,b), not path(a,b).
            omit(c,a) :- edge(c,a), not path(c,a).
            omit(c,d) :- edge(c,d), not path(c,d).
            omit(b,d) :- edge(b,d), not path(b,d).
            omit(b,c) :- edge(b,c), not path(b,c).
            :- path(c,d), path(b,d).
            :- path(b,c), path(a,c).
            :- path(d,a), path(c,a).
            :- path(a,c), path(a,b).
            :- path(b,d), path(b,c).
            :- path(c,d), path(c,a).
            on_path(a) :- path(a,c), path(c,a).
            on_path(a) :- path(a,c), path(d,a).
            on_path(b) :- path(b,d), path(a,b).
            on_path(c) :- path(c,d), path(a,c).
            on_path(c) :- path(c,d), path(b,c).
            on_path(b) :- path(b,c), path(a,b).
            on_path(c) :- path(c,a), path(a,c).
            on_path(c) :- path(c,a), path(b,c).
            on_path(d) :- path(d,a), path(b,d).
            on_path(d) :- path(d,a), path(c,d).
            on_path(a) :- path(a,b), path(c,a).
            on_path(a) :- path(a,b), path(d,a).
            :- node(a), not on_path(a).
            :- node(c), not on_path(c).
            :- node(d), not on_path(d).
            :- node(b), not on_path(b).
            reach(a) :- start(a).
            reach(d) :- path(c,d), reach(c).
            reach(a) :- path(c,a), reach(c).
            reach(a) :- path(d,a), reach(d).
            reach(c) :- path(a,c), reach(a).
            reach(b) :- path(a,b), reach(a).
            reach(d) :- path(b,d), reach(b).
            reach(c) :- path(b,c), reach(b).
            :- node(a), not reach(a).
            :- node(c), not reach(c).
            :- node(d), not reach(d).
            :- node(b), not reach(b).
            """
        expected_result = [s.strip() for s in expected_result.strip().split("\n")]
        self.assertCountEqual(
            [str(rule) for rule in grounder.ground()], expected_result
        )
        expected_grodunded_rules = """
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            path(d,a) :- edge(d,a), not omit(d,a).
            path(c,d) :- edge(c,d), not omit(c,d).
            path(a,b) :- edge(a,b), not omit(a,b).
            path(c,a) :- edge(c,a), not omit(c,a).
            path(b,d) :- edge(b,d), not omit(b,d).
            path(b,c) :- edge(b,c), not omit(b,c).
            path(a,c) :- edge(a,c), not omit(a,c).
            omit(d,a) :- edge(d,a), not path(d,a).
            omit(c,d) :- edge(c,d), not path(c,d).
            omit(a,b) :- edge(a,b), not path(a,b).
            omit(c,a) :- edge(c,a), not path(c,a).
            omit(b,d) :- edge(b,d), not path(b,d).
            omit(b,c) :- edge(b,c), not path(b,c).
            omit(a,c) :- edge(a,c), not path(a,c).
            :- node(b), not on_path(b).
            :- node(a), not on_path(a).
            :- node(c), not on_path(c).
            :- node(d), not on_path(d).
            reach(a) :- start(a).
            :- node(b), not reach(b).
            :- node(a), not reach(a).
            :- node(c), not reach(c).
            :- node(d), not reach(d).
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            path(b,c) :- edge(b,c), not omit(b,c).
            path(c,d) :- edge(c,d), not omit(c,d).
            path(a,c) :- edge(a,c), not omit(a,c).
            path(a,b) :- edge(a,b), not omit(a,b).
            path(c,a) :- edge(c,a), not omit(c,a).
            path(d,a) :- edge(d,a), not omit(d,a).
            path(b,d) :- edge(b,d), not omit(b,d).
            omit(b,c) :- edge(b,c), not path(b,c).
            omit(c,d) :- edge(c,d), not path(c,d).
            omit(a,c) :- edge(a,c), not path(a,c).
            omit(a,b) :- edge(a,b), not path(a,b).
            omit(c,a) :- edge(c,a), not path(c,a).
            omit(d,a) :- edge(d,a), not path(d,a).
            omit(b,d) :- edge(b,d), not path(b,d).
            :- path(c,d), path(b,d).
            :- path(b,c), path(a,c).
            :- path(d,a), path(c,a).
            :- path(a,c), path(a,b).
            :- path(b,d), path(b,c).
            :- path(c,d), path(c,a).
            on_path(a) :- path(a,c), path(c,a).
            on_path(a) :- path(a,c), path(d,a).
            on_path(b) :- path(b,d), path(a,b).
            on_path(c) :- path(c,d), path(a,c).
            on_path(c) :- path(c,d), path(b,c).
            on_path(c) :- path(c,a), path(a,c).
            on_path(c) :- path(c,a), path(b,c).
            on_path(a) :- path(a,b), path(c,a).
            on_path(a) :- path(a,b), path(d,a).
            on_path(b) :- path(b,c), path(a,b).
            on_path(d) :- path(d,a), path(b,d).
            on_path(d) :- path(d,a), path(c,d).
            :- node(a), not on_path(a).
            :- node(c), not on_path(c).
            :- node(d), not on_path(d).
            :- node(b), not on_path(b).
            reach(a) :- start(a).
            reach(c) :- path(a,c), reach(a).
            reach(b) :- path(a,b), reach(a).
            :- node(a), not reach(a).
            :- node(c), not reach(c).
            :- node(d), not reach(d).
            :- node(b), not reach(b).
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            path(b,c) :- edge(b,c), not omit(b,c).
            path(c,d) :- edge(c,d), not omit(c,d).
            path(a,c) :- edge(a,c), not omit(a,c).
            path(a,b) :- edge(a,b), not omit(a,b).
            path(c,a) :- edge(c,a), not omit(c,a).
            path(d,a) :- edge(d,a), not omit(d,a).
            path(b,d) :- edge(b,d), not omit(b,d).
            omit(b,c) :- edge(b,c), not path(b,c).
            omit(c,d) :- edge(c,d), not path(c,d).
            omit(a,c) :- edge(a,c), not path(a,c).
            omit(a,b) :- edge(a,b), not path(a,b).
            omit(c,a) :- edge(c,a), not path(c,a).
            omit(d,a) :- edge(d,a), not path(d,a).
            omit(b,d) :- edge(b,d), not path(b,d).
            :- path(c,d), path(b,d).
            :- path(d,a), path(c,a).
            :- path(b,c), path(a,c).
            :- path(b,d), path(b,c).
            :- path(a,c), path(a,b).
            :- path(c,d), path(c,a).
            on_path(b) :- path(b,d), path(a,b).
            on_path(a) :- path(a,c), path(c,a).
            on_path(a) :- path(a,c), path(d,a).
            on_path(c) :- path(c,d), path(a,c).
            on_path(c) :- path(c,d), path(b,c).
            on_path(c) :- path(c,a), path(a,c).
            on_path(c) :- path(c,a), path(b,c).
            on_path(a) :- path(a,b), path(c,a).
            on_path(a) :- path(a,b), path(d,a).
            on_path(d) :- path(d,a), path(b,d).
            on_path(d) :- path(d,a), path(c,d).
            on_path(b) :- path(b,c), path(a,b).
            :- node(a), not on_path(a).
            :- node(c), not on_path(c).
            :- node(d), not on_path(d).
            :- node(b), not on_path(b).
            reach(a) :- start(a).
            reach(d) :- path(b,d), reach(b).
            reach(c) :- path(b,c), reach(b).
            reach(c) :- path(a,c), reach(a).
            reach(b) :- path(a,b), reach(a).
            reach(d) :- path(c,d), reach(c).
            reach(a) :- path(c,a), reach(c).
            :- node(a), not reach(a).
            :- node(c), not reach(c).
            :- node(d), not reach(d).
            :- node(b), not reach(b).
            node(a).
            node(b).
            node(c).
            node(d).
            edge(a,b).
            edge(a,c).
            edge(b,c).
            edge(b,d).
            edge(c,a).
            edge(c,d).
            edge(d,a).
            start(a).
            path(b,c) :- edge(b,c), not omit(b,c).
            path(c,d) :- edge(c,d), not omit(c,d).
            path(a,c) :- edge(a,c), not omit(a,c).
            path(a,b) :- edge(a,b), not omit(a,b).
            path(c,a) :- edge(c,a), not omit(c,a).
            path(d,a) :- edge(d,a), not omit(d,a).
            path(b,d) :- edge(b,d), not omit(b,d).
            omit(b,c) :- edge(b,c), not path(b,c).
            omit(c,d) :- edge(c,d), not path(c,d).
            omit(a,c) :- edge(a,c), not path(a,c).
            omit(a,b) :- edge(a,b), not path(a,b).
            omit(c,a) :- edge(c,a), not path(c,a).
            omit(d,a) :- edge(d,a), not path(d,a).
            omit(b,d) :- edge(b,d), not path(b,d).
            :- path(c,d), path(b,d).
            :- path(d,a), path(c,a).
            :- path(b,c), path(a,c).
            :- path(b,d), path(b,c).
            :- path(a,c), path(a,b).
            :- path(c,d), path(c,a).
            on_path(b) :- path(b,d), path(a,b).
            on_path(a) :- path(a,c), path(c,a).
            on_path(a) :- path(a,c), path(d,a).
            on_path(c) :- path(c,d), path(a,c).
            on_path(c) :- path(c,d), path(b,c).
            on_path(c) :- path(c,a), path(a,c).
            on_path(c) :- path(c,a), path(b,c).
            on_path(a) :- path(a,b), path(c,a).
            on_path(a) :- path(a,b), path(d,a).
            on_path(d) :- path(d,a), path(b,d).
            on_path(d) :- path(d,a), path(c,d).
            on_path(b) :- path(b,c), path(a,b).
            :- node(a), not on_path(a).
            :- node(c), not on_path(c).
            :- node(d), not on_path(d).
            :- node(b), not on_path(b).
            reach(a) :- start(a).
            reach(d) :- path(b,d), reach(b).
            reach(c) :- path(a,c), reach(a).
            reach(d) :- path(c,d), reach(c).
            reach(a) :- path(c,a), reach(c).
            reach(b) :- path(a,b), reach(a).
            reach(a) :- path(d,a), reach(d).
            reach(c) :- path(b,c), reach(b).
            :- node(a), not reach(a).
            :- node(c), not reach(c).
            :- node(d), not reach(d).
            :- node(b), not reach(b).
            """
        expected_grodunded_rules = [
            s.strip() for s in expected_grodunded_rules.strip().split("\n")
        ]
        self.assertCountEqual(
            [str(rule) for rule in grounder.instantiator.grounded_rules],
            expected_grodunded_rules,
        )
        self.assertEqual(set(expected_result), set(expected_grodunded_rules))
