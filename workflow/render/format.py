import yaml
import json

from workflow.render.base import render
from workflow.render.shell import render_bash
from workflow.render.airflow import render_airflow
from workflow.render.systemd import render_systemd


def render_formatted(workflow_template, format):
    rendered_template = render(workflow_template)

    if format == "yaml":
        return yaml.dump(rendered_template, default_flow_style=False, sort_keys=False)
    elif format == "json":
        return json.dumps(rendered_template, indent=4)
    elif format == "bash":
        return render_bash(rendered_template)
    elif format == "airflow":
        return render_airflow(rendered_template)
    elif format == "systemd":
        lines = []
        for key, value in render_systemd(rendered_template).items():
            lines.append(f"======== systemd {key} ========")
            lines.append(value)
        return "\n".join(lines)
    else:
        raise ValueError(
            f'format="{format}" not recognized output format for rendering'
        )
