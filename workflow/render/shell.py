import textwrap

INDENT = '  '


def format_runs(runs):
    if isinstance(runs, list):
        return "\n".join(runs)
    return runs


def render_bash(rendered_template):
    bash_script = ""

    for job in rendered_template['jobs']:
        run_block = format_runs(job['runs']).strip()

        if 'strategy' in job and 'cache' in job['strategy']:
            run_block = textwrap.indent(run_block, INDENT)

            run_block = (
                f'if [ ! -f "{job["strategy"]["cache"]}" ]; then\n'
                f'{run_block}\n'
                f'fi'
            )

        bash_script = bash_script + (
            f"\n# Job: {job['name']}\n"
            f"{run_block}\n"
        )

    return bash_script
