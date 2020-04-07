import argparse
import sys

from workflow.cli.render import create_render_subcommand


def cli(args):
    parser = argparse.ArgumentParser(description="Workflow command line")
    parser.set_defaults(func=None)
    create_render_subcommand(parser)
    args = parser.parse_args(args)

    if args.func is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args.func(args)
