from typing import AbstractSet, Optional

from clingo import ast
from clingo.ast import AST, ASTType
from clingo.control import Control
from clingo.symbol import Function, Symbol
from clingox.program import Program, ProgramObserver
from rule import Rule, program_rules
from util import head_as_disjunction


def _encode_literal(literal: AST, prefix: str, sign: Optional[ast.Sign] = None) -> AST:
    new_lit = ast.Literal(
        literal.location,
        sign if sign is not None else literal.sign,
        ast.SymbolicAtom(
            ast.Function(
                literal.atom.symbol.location,
                f"{prefix}{literal.atom.symbol.name}",
                literal.atom.symbol.arguments,
                literal.atom.symbol.external,
            )
        ),
    )
    return new_lit


def _encode_rule(rule: AST) -> AST:
    pos_body = []
    neg_body = []
    for lit in rule.body:
        if lit.sign == ast.Sign.Negation and lit.atom.ast_type == ASTType.SymbolicAtom:
            new_lit = _encode_literal(lit, "b", ast.Sign.NoSign)
            neg_body.append(new_lit)
        else:
            pos_body.append(lit)
    new_head = head_as_disjunction(rule.head)
    for clit in new_head.elements:
        lit = clit.literal
        if lit.atom.ast_type == ASTType.SymbolicAtom:
            new_lit = _encode_literal(lit, "h")
        else:
            new_lit = lit
        neg_body.append(new_lit)
    new_head.elements = neg_body
    return ast.Rule(rule.location, new_head, pos_body)


def _decode_symbol(symbol: Symbol) -> tuple[bool, Symbol]:
    is_head = symbol.name[0] == "h"
    new_symbol = Function(symbol.name[1:], symbol.arguments, symbol.positive)
    return (is_head, new_symbol)


def _dencode_rule(rule: Rule) -> Rule:
    head = []
    neg_body = []
    for lit in rule.head:
        is_head, new_symbol = _decode_symbol(lit)
        if is_head:
            head.append(new_symbol)
        else:
            neg_body.append(new_symbol)
    return Rule(rule.choice, head, rule.pos_body, neg_body)


class Instantiator:
    def __init__(self):
        self.grounded_rules = []

    def _ground_rule(
        self, rule: AST, atoms: AbstractSet[Symbol] = frozenset()
    ) -> list[Rule]:
        prg = Program()
        ctl = Control(message_limit=0)
        ctl.register_observer(ProgramObserver(prg))
        externals = " ".join(f"#external {str(a)}." for a in atoms)
        program_to_ground = str(rule) + "\n" + externals
        ctl.add("base", [], program_to_ground)
        ctl.ground([("base", [])])
        rules = program_rules(prg)
        return rules

    def ground_rule(
        self, rule: AST, atoms: AbstractSet[Symbol] = frozenset()
    ) -> list[Rule]:
        encoded_rule = _encode_rule(rule)
        encoded_ground_rules = self._ground_rule(encoded_rule, atoms)
        rules = [_dencode_rule(rule) for rule in encoded_ground_rules]
        self.grounded_rules.extend(rules)
        return rules
