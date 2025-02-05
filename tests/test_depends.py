import unittest

from algorithms import depends
from util import parse_statement


class TestDepends(unittest.TestCase):
    def test_depends_01(self):
        rule1 = parse_statement("omit(X,Y) :- not path(X,Y), edge(X,Y).")
        rule2 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        self.assertTrue(depends(rule1, rule2))
        self.assertTrue(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertFalse(depends(rule2, rule2))

    def test_depends_02(self):
        rule1 = parse_statement("omit(X,Y) :- not path(X,Y), edge(X,Y).")
        rule2 = parse_statement(":- path(X,Y), path(X',Y), X < X'.")
        self.assertFalse(depends(rule1, rule2))
        self.assertFalse(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertFalse(depends(rule2, rule2))

    def test_depends_03(self):
        rule1 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        rule2 = parse_statement(":- path(X,Y), path(X',Y), X < X'.")
        self.assertFalse(depends(rule1, rule2))
        self.assertTrue(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertFalse(depends(rule2, rule2))

    def test_depends_04(self):
        rule1 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        rule2 = parse_statement("on_path(Y) :- path(X,Y), path(Y,Z).")
        self.assertFalse(depends(rule1, rule2))
        self.assertTrue(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertFalse(depends(rule2, rule2))

    def test_depends_05(self):
        rule1 = parse_statement("edge(a,b).")
        rule2 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        self.assertFalse(depends(rule1, rule2))
        self.assertTrue(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertFalse(depends(rule2, rule2))

    def test_depends_06(self):
        rule1 = parse_statement("reach(X) :- start(X).")
        rule2 = parse_statement("reach(Y) :- reach(X), path(X,Y).")
        self.assertFalse(depends(rule1, rule2))
        self.assertTrue(depends(rule2, rule1))
        self.assertFalse(depends(rule1, rule1))
        self.assertTrue(depends(rule2, rule2))
