import argparse
import sys

if sys.version_info < (3, 9):
    raise SystemExit("Sorry, this code need Python 3.9 or higher")

import algorithms
import util
from algorithms import BottomUpGrounder, Grounder, GrounderWithDependencies


def command_ground(args: argparse.Namespace) -> None:
    grounder: Grounder
    if args.algorithm == "dependencies":
        grounder = GrounderWithDependencies()
    else:
        grounder = BottomUpGrounder()
    grounder.add_files([f.name for f in args.files])
    ground_program = grounder.ground()
    if args.all_computed_rules:
        print("\n".join(str(rule) for rule in grounder.instantiator.grounded_rules))
    else:
        print("\n".join(str(rule) for rule in ground_program))


def command_graph(args: argparse.Namespace) -> None:
    program = util.parse_files([f.name for f in args.files])
    graph, _ = algorithms.dependency_graph(program)
    print(graph)


def command_sccs(args: argparse.Namespace) -> None:
    program = util.parse_files([f.name for f in args.files])
    sccs = algorithms.strongly_connected_components(program)
    print(algorithms.sccs_to_str(sccs))


parser = argparse.ArgumentParser(description="Grodunds a logic program.")
subparsers = parser.add_subparsers(help="available sub-commands", required=True)

# create the parser for the "ground" command
parser_ground = subparsers.add_parser("ground", help="grounds a logic program")
parser_ground.add_argument(
    "files",
    help="Files to be grounded",
    type=argparse.FileType("r"),
    nargs="+",
)
parser_ground.add_argument(
    "--all-computed-rules",
    help="Prints all computed rules instead of the final outcome",
    action="store_true",
)
parser_ground.add_argument(
    "--algorithm",
    help="Algorithm to be used for grounding",
    type=str,
    choices=["bottom-up", "dependencies"],
    default="bottom-up",
)
parser_ground.set_defaults(func=command_ground)

# create the parser for the "graph" command
parser_graph = subparsers.add_parser(
    "graph",
    help="shows the dependency graph of a logic program",
)
parser_graph.add_argument(
    "files",
    help="Files that contain the program",
    type=argparse.FileType("r"),
    nargs="+",
)
parser_graph.set_defaults(func=command_graph)

# create the parser for the "sccs" command
parser_sccs = subparsers.add_parser(
    "sccs", help="shows the dependency sccs of a logic program"
)
parser_sccs.add_argument(
    "files",
    help="Files that contain the program",
    type=argparse.FileType("r"),
    nargs="+",
)
parser_sccs.set_defaults(func=command_sccs)

args = parser.parse_args()
args.func(args)
