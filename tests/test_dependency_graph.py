import unittest

from algorithms import dependency_graph
from util import parse_statement


class TestDependencyGraph(unittest.TestCase):
    def test_dependency_graph(self):
        rule1 = parse_statement("omit(X,Y) :- not path(X,Y), edge(X,Y).")
        rule2 = parse_statement("path(X,Y) :- not omit(X,Y), edge(X,Y).")
        rule3 = parse_statement(":- path(X,Y), path(X',Y), X < X'.")
        rule4 = parse_statement(":- path(X,Y), path(X,Y'), Y < Y'.")
        rule5 = parse_statement("on_path(Y) :- path(X,Y), path(Y,Z).")
        rule6 = parse_statement(":- node(X), not on_path(X).")
        rule7 = parse_statement("reach(X) :- start(X).")
        rule8 = parse_statement("reach(Y) :- reach(X), path(X,Y).")
        rule9 = parse_statement(":- node(X), not reach(X).")
        program = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
        graph = dependency_graph(program)[0]
        vertice_rules = [vertex.name for vertex in graph._vertices]
        self.assertCountEqual(vertice_rules, program)
        self.maxDiff = None
        for rule in program:
            self.assertTrue(rule in graph._names)
        edges = {
            rule1: [rule2],
            rule2: [rule1, rule3, rule4, rule5, rule8],
            rule3: [],
            rule4: [],
            rule5: [rule6],
            rule6: [],
            rule7: [rule8, rule9],
            rule8: [rule8, rule9],
            rule9: [],
        }
        for vertex in graph._vertices:
            vertex_dependecies = [graph._names[rule] for rule in edges[vertex.name]]
            self.assertCountEqual(
                vertex.edges, vertex_dependecies, msg="Vertex: {}".format(vertex.name)
            )
