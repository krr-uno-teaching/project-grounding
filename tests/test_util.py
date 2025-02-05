import unittest

from clingo import ast
from clingo.ast import Location, Position
from util import body_symbolic_atoms, head_symbolic_atoms, parse_statement


class TestCase(unittest.TestCase):
    def test_rule_head(self):
        head = head_symbolic_atoms(
            parse_statement("a(X) :- b(X), c(X), not d(X), not e(X).")
        )
        expected_head = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "a",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        self.assertEqual(head, [expected_head])

        head = head_symbolic_atoms(
            parse_statement("a1(X), a2(X) :- b(X), c(X), not d(X), not e(X).")
        )
        expected_head1 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "a1",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        expected_head2 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "a2",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        self.assertEqual(head, [expected_head1, expected_head2])

    def test_rule_body(self):
        body = body_symbolic_atoms(
            parse_statement("a(X) :- b(X), c(X), not d(X), not e(X).")
        )
        expected_body1 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "b",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        expected_body2 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "c",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        expected_body3 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "d",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        expected_body4 = ast.Function(
            Location(
                begin=Position(filename="<string>", line=1, column=1),
                end=Position(filename="<string>", line=1, column=5),
            ),
            "e",
            [
                ast.Variable(
                    Location(
                        begin=Position(filename="<string>", line=1, column=3),
                        end=Position(filename="<string>", line=1, column=4),
                    ),
                    "X",
                )
            ],
            0,
        )
        self.assertCountEqual(
            body, [expected_body1, expected_body2, expected_body3, expected_body4]
        )
