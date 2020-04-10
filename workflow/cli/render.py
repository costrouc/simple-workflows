import pathlib

import yaml

from workflow.render.format import render_formatted


def create_render_subcommand(parser):
    subparser = parser.add_subparsers(help="Initialize QHub repository")
    subparser = subparser.add_parser("render")
    subparser.add_argument(
        "--format",
        default="yaml",
        choices=["yaml", "bash", "json", "airflow", "systemd"],
        help="format to output workflow",
    )
    subparser.add_argument("workflow", help="workflow configuration")
    subparser.set_defaults(func=handle_render)


def handle_render(args):
    filename = pathlib.Path(args.workflow)
    if not filename.is_file():
        raise ValueError(f'specified filename="{filename}" is not a file')

    with filename.open() as f:
        workflow_template = yaml.safe_load(f)

    print(render_formatted(workflow_template, args.format))
