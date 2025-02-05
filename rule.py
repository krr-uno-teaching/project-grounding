from dataclasses import dataclass
from itertools import chain
from typing import Sequence

from clingo.symbol import Symbol
from clingox.program import OutputTable, Program
from clingox.program import Rule as XRule


@dataclass
class Rule:
    """
    Ground representation of disjunctive and choice rules.
    """

    choice: bool
    head: Sequence[Symbol]
    pos_body: Sequence[Symbol] = tuple()
    neg_body: Sequence[Symbol] = tuple()

    def __str__(self) -> str:
        """
        Pretty print a rule.
        """
        head = self._str_rule_head()
        body = ", ".join(
            chain(
                (str(lit) for lit in self.pos_body),
                (f"not {str(lit)}" for lit in self.neg_body),
            )
        )

        return f"{head}{body}."

    def _str_rule_head(self) -> str:
        """
        Pretty print the head of a rule including the implication symbol if
        necessary.
        """
        ret = ""

        if self.choice:
            ret += "{"
        ret += "; ".join(str(lit) for lit in self.head)
        if self.choice:
            ret += "}"

        if not self.head and not self.choice:
            ret += ":- "
        elif self.pos_body or self.neg_body:
            ret += " :- "

        return ret


def get_rule(rule: XRule, output_table: OutputTable) -> Rule:
    choice = rule.choice
    head = tuple(output_table[i] for i in rule.head)
    pos_body = tuple(output_table[i] for i in rule.body if i >= 0)
    neg_body = tuple(output_table[-i] for i in rule.body if i < 0)
    return Rule(choice, head, pos_body, neg_body)


def is_fact(rule: XRule) -> bool:
    return not rule.choice and len(rule.head) == 1 and not rule.body


def program_rules(program: Program) -> list[Rule]:
    rules = [
        get_rule(rule, program.output_atoms)
        for rule in program.rules
        if not is_fact(rule)
    ]
    for fact in program.facts:
        rules.append(Rule(choice=False, head=[fact.symbol]))
    return rules
