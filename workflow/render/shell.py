import textwrap

from workflow.render.configuration import render_configuration

INDENT = "  "
EMPTY_LINE = "\n"


def format_runs(runs):
    if isinstance(runs, list):
        return "\n".join(runs)
    return runs


def render_bash(rendered_template):
    bash_script = ["#!/usr/bin/env bash"]

    for job in rendered_template["jobs"]:
        bash_script.append(f"\n# Job: {job['name']}")

        if "config" in job:
            for config in job["config"]:
                bash_script.append(f'cat >{config["filename"]} <<EOL')

                format = config.get("format", config["filename"].split(".")[-1])
                config_content = render_configuration(config["data"], format)
                bash_script.append(config_content)

                bash_script.append("EOL\n")

        if "strategy" in job and "cache" in job["strategy"]:
            bash_script.append(f'if [ ! -f "{job["strategy"]["cache"]}" ]; then')
            bash_script.append(
                textwrap.indent(format_runs(job["runs"]).strip(), INDENT)
            )
            bash_script.append("else")
            bash_script.append(
                INDENT + f'echo "skipping job={job["name"]} using cache"'
            )
            bash_script.append("fi")
        else:
            bash_script.append(format_runs(job["runs"]).strip())

    return "\n".join(bash_script).strip()
