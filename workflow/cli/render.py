import pathlib
import yaml
import json

from workflow.render.base import render
from workflow.render.shell import render_bash


def create_render_subcommand(parser):
    subparser = parser.add_subparsers(help="Initialize QHub repository")
    subparser = subparser.add_parser("render")
    subparser.add_argument("--format", default='yaml', choices=['yaml', 'bash', 'json', 'airflow'], help="format to output workflow")
    subparser.add_argument('workflow', help='workflow configuration')
    subparser.set_defaults(func=handle_render)


def handle_render(args):
    filename = pathlib.Path(args.workflow)
    if not filename.is_file():
        raise ValueError(f'specified filename="{filename}" is not a file')

    with filename.open() as f:
        workflow_template = yaml.safe_load(f)

    rendered_template = render(workflow_template)

    if args.format == 'yaml':
        print(yaml.dump(rendered_template, default_flow_style=False, sort_keys=False))
    elif args.format == 'json':
        print(json.dumps(rendered_template))
    elif args.format == 'bash':
        print(render_bash(rendered_template))
    else:
        raise ValueError('format="{format}" not recognized output format for rendering')
