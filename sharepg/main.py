#!/usr/bin/env python3
from sharepg.disassemble import extract_bubbles, disassemble_graph, get_intervals
from argparse import ArgumentParser
from sys import argv
from os.path import exists
from json import load
from rich import print
from rich.traceback import install
from gfagraphs import Graph

install(show_locals=True)

parser: ArgumentParser = ArgumentParser(
    description='GFA manipulation tools.', add_help=True)
subparsers = parser.add_subparsers(
    help='Available subcommands', dest="subcommands")

parser._positionals.title = 'Subcommands'
parser._optionals.title = 'Global Arguments'

###

parser_disbubbles: ArgumentParser = subparsers.add_parser(
    'disbubbles', help='Extracts bubbles shared by genomes.'
)
parser_disbubbles.add_argument(
    "graph", type=str, help='Path to a .gfa graph'
)
parser_disbubbles.add_argument(
    '-a', '--set_a', type=str, help='A first set of paths', nargs='+'
)
parser_disbubbles.add_argument(
    '-b', '--set_b', type=str, help='A second set of paths', nargs='+'
)
parser_disbubbles.add_argument(
    '-r', '--reference', type=str, help='A reference name. Must be in one of the sets.'
)
parser_disbubbles.add_argument(
    '-t', '--threshold', type=float, help='A threshold (proprortion of graphs that shall go through).', default=1.
)

###

parser_disnodes: ArgumentParser = subparsers.add_parser(
    'disnodes', help='Extracts nodes shared by genomes.'
)
parser_disnodes.add_argument(
    "graph", type=str, help='Path to a .gfa graph'
)
parser_disnodes.add_argument(
    '-a', '--set_a', type=str, help='A first set of paths', nargs='+'
)
parser_disnodes.add_argument(
    '-b', '--set_b', type=str, help='A second set of paths', nargs='+'
)
parser_disnodes.add_argument(
    '-r', '--reference', type=str, help='A reference name. Must be in one of the sets.'
)
parser_disnodes.add_argument(
    '-t', '--threshold', type=float, help='A threshold (proprortion of graphs that shall go through).', default=1.
)


###

parser_disintervals: ArgumentParser = subparsers.add_parser(
    'disintervals', help='Extracts intervals shared by genomes.'
)
parser_disintervals.add_argument(
    "graph", type=str, help='Path to a .gfa graph'
)
parser_disintervals.add_argument(
    '-a', '--set_a', type=str, help='A first set of paths', nargs='+'
)
parser_disintervals.add_argument(
    '-b', '--set_b', type=str, help='A second set of paths', nargs='+'
)
parser_disintervals.add_argument(
    '-r', '--reference', type=str, help='A reference name. Must be in one of the sets.'
)
parser_disintervals.add_argument(
    '-t', '--threshold_upper', type=float, help='A threshold (proprortion of graphs that shall go through).', default=1.
)
parser_disintervals.add_argument(
    '-l', '--threshold_lower', type=float, help='B threshold (proprortion of graphs that shall not go through).', default=1.
)


#######################################

args = parser.parse_args()


def main() -> None:
    "Main call for subprograms"
    if len(argv) == 1:
        print(
            "[dark_orange]You need to provide a command and its arguments for the program to work.\n"
            "Try to use -h or --help to get list of available commands."
        )
        exit()

    for identifier, syspath in [(key, path) for key, path in args.__dict__.items() if key in ['graph',]]:
        if not exists(syspath):
            raise RuntimeError(
                f"Specified path '{syspath}' for argument '{identifier}' does not exists."
            )
    if args.reference not in args.set_a + args.set_b:
        raise RuntimeError(
            f"Reference {args.reference} is not in one of the populations {args.set_a + args.set_b} we want to study."
        )

    ##############################################################################
    #                                    COMMANDS                                #
    ##############################################################################

    if args.subcommands == 'disbubbles':
        "Extract bubbles that are shared by a set of paths"
        # Loading the graph within a context manager
        with Graph(
            args.graph,
            with_sequence=False,
            low_memory=True,
            with_reverse_edges=False,
            regexp='.*'
        ) as gfa_graph:
            # Computing sequence offsets and paths that are going through each node
            gfa_graph.sequence_offsets()
            bubbles = extract_bubbles(
                graph=args.graph,
                gfa_graph=gfa_graph,
                reference=args.reference,
                node_result=disassemble_graph(
                    gfa_graph=gfa_graph,
                    path_a=set(args.set_a),
                    path_b=set(args.set_b),
                    reference=args.reference,
                    threshold_upper=args.threshold_upper,
                    threshold_lower=args.threshold_lower,
                ),
            )
            for items in bubbles:
                print(
                    '\t'.join(items)
                )

    elif args.subcommands == 'disnodes':
        "Extract nodes that are shared by a set of paths"
        # Loading the graph within a context manager
        with Graph(
            args.graph,
            with_sequence=False,
            low_memory=True,
            with_reverse_edges=False,
            regexp='.*'
        ) as gfa_graph:
            # Computing sequence offsets and paths that are going through each node
            gfa_graph.sequence_offsets()
            nodes: dict[str, bool] = disassemble_graph(
                gfa_graph=gfa_graph,
                path_a=set(args.set_a),
                path_b=set(args.set_b),
                reference=args.reference,
                threshold_upper=args.threshold_upper,
                threshold_lower=args.threshold_lower,
            )
            for node_name, status in nodes.items():
                print(f'{node_name}\t{int(status)}')
    elif args.subcommands == 'disintervals':
        "Extract intervals that are shared by a set of paths"
        # Loading the graph within a context manager
        with Graph(
            args.graph,
            with_sequence=False,
            low_memory=True,
            with_reverse_edges=False,
            regexp='.*'
        ) as gfa_graph:
            # Computing sequence offsets and paths that are going through each node
            gfa_graph.sequence_offsets()
            intervals = get_intervals(
                gfa_graph=gfa_graph,
                node_result=disassemble_graph(
                    gfa_graph=gfa_graph,
                    path_a=set(args.set_a),
                    path_b=set(args.set_b),
                    reference=args.reference,
                    threshold_upper=args.threshold_upper,
                    threshold_lower=args.threshold_lower,
                ),
                paths_a=set(args.set_a),
            )
            for path_name, interval in intervals.items():
                print(
                    f"{path_name}\t{','.join([str(intr) for intr in interval.intervals])}")

    else:
        print(
            "[dark_orange]Unknown command. Please use the help to see available commands."
        )
        exit(1)
