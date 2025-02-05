#!/bin/python3

import argparse
import io
import os
import shutil
import sys
import unittest
from abc import ABC, abstractmethod
from typing import Optional

if sys.version_info < (3, 9):
    raise SystemExit("Sorry, this code need Python 3.9 or higher")


GITHUB_AUTOGRADE_DIR = os.path.join(".github", "classroom")
GITHUB_AUTOGRADE_FILE = os.path.join(GITHUB_AUTOGRADE_DIR, "autograding.json")
GITHUB_AUTOGRADE_BACK = os.path.join("github", "autograding.json")
try:
    if os.path.exists(".git"):
        os.makedirs(GITHUB_AUTOGRADE_DIR, exist_ok=True)
        shutil.copy(GITHUB_AUTOGRADE_BACK, GITHUB_AUTOGRADE_FILE)
        os.system(f"git add {GITHUB_AUTOGRADE_FILE}")
except Exception as e:
    pass


class Question(ABC):
    @abstractmethod
    def eval(self):
        pass


class QuestionALL(Question):
    def __init__(self, name: str, questions: list[Question], max_points: int):
        self.name = name
        self._questions = questions

    def eval(self):
        success = True
        failing_tests = []
        for question in self._questions:
            s, ft = question.eval()
            success = success & s
            failing_tests.extend(ft)
        return success, failing_tests


class QuestionUnitTestAll(Question):
    def __init__(self, name, tests: dict[str, Optional[list[str]]], max_points: int):
        self.name = name
        self.tests = tests
        self.max_points = max_points

    def eval(self):
        sys.stdout.write(f"evaluating {self.name}...")
        success = True
        failing_tests = []
        for test in self.tests:
            test_out = io.StringIO()
            runner = unittest.TextTestRunner(test_out)
            itersuite = unittest.TestLoader().loadTestsFromName(test)
            test_result = runner.run(itersuite)
            if not test_result.wasSuccessful():
                success = False
                failing_tests.extend(test_result.failures)
                failing_tests.extend(test_result.errors)
        sys.stdout.write(" done\n")
        return success, failing_tests


question1 = QuestionUnitTestAll(
    name="question 1",
    tests={
        "tests.test_bottom_up": None,
    },
    max_points=10,
)

question2a = QuestionUnitTestAll(
    name="question 2a",
    tests={
        "tests.test_depends": None,
    },
    max_points=10,
)

question2b = QuestionUnitTestAll(
    name="question 2b",
    tests={
        "tests.test_dependency_graph": None,
    },
    max_points=10,
)

question2c = QuestionUnitTestAll(
    name="question 2c",
    tests={
        "tests.test_scc": None,
    },
    max_points=10,
)

question2d = QuestionUnitTestAll(
    name="question 2d",
    tests={
        "tests.test_scc_independent": None,
    },
    max_points=10,
)

question2 = QuestionALL(
    name="question 2",
    questions=[question2a, question2b, question2c, question2d],
    max_points=10,
)


question3 = QuestionUnitTestAll(
    name="question 3",
    tests={
        "tests.test_grounding_with_dependencies": None,
    },
    max_points=10,
)

questionALL = QuestionALL(
    name="All questions",
    questions=[question1, question2, question3],
    max_points=10,
)

questions = {
    "question1": question1,
    "question2": question2,
    "question2a": question2a,
    "question2b": question2b,
    "question2c": question2c,
    "question2d": question2d,
    "question3": question3,
    "questionALL": questionALL,
}


def dispatch_question(args):
    question_name = f"question{args.question}"
    if question_name in questions:
        return questions[question_name]
    else:
        raise Exception("Question not found", args.question)


def parse():
    parser = argparse.ArgumentParser(description="Test Grounder")
    parser.add_argument(
        "--question",
        metavar="N",
        help="Question number.",
        required=False,
        default=None,
        choices=["1", "2", "2a", "2b", "2c", "2d", "3", "ALL"],
    )

    parser.add_argument(
        "--timeout",
        "-t",
        metavar="N",
        type=int,
        help="Time allocated to each instance.",
        required=False,
        default=180,
    )

    parser.add_argument(
        "--generate-solutions",
        metavar="<dir>",
        help="Path to a directory to write solutions. If does not exist, it will be created.",
        required=False,
        default=None,
    )
    args = parser.parse_args()

    if args.question is None:
        args.question = "ALL"

    return args


def main():
    try:
        args = parse()
        if args.question:
            question = dispatch_question(args)
            success, failing_tests = question.eval()
            if success:
                sys.stdout.write("SUCCESS\n")
                return 0
            else:
                sys.stdout.write("FAILURE\n")
                sys.stdout.write("The following tests failed:\n")
                for error in failing_tests:
                    sys.stdout.write(f"   {str(error[0].id())}\n")
                sys.stdout.write(
                    "\nYou can get more information by running the test directly using the command:\n"
                )
                sys.stdout.write("   python -m unittest <name-of-failing-test>\n")
                return 1

    except Exception as e:
        if len(e.args) >= 1:
            if e.args[0] == "Question not found":
                sys.stderr.write(f"ERROR: {e.args[0]} {e.args[1]}\n")
                return 1
        raise e


if __name__ == "__main__":
    sys.exit(main())
