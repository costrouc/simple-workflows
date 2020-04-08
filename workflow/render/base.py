import json
import re

import yaml

from workflow.render.schema import validate_schema

PARAMETER_REGEX = r"\s*{{\s*param\.([A-Za-z0-9_\.]+)\s*}}\s*"


def get_attribute(path, node):
    _node = node
    for attr in path.split('.'):
        if re.fullmatch('\d+', attr):
            _node = _node[int(attr)]
        else:
            _node = _node[attr]
    return _node


def nested_chain_map(path, dicts):
    for d in dicts:
        try:
            return get_attribute(path, d)
        except:
            pass
    raise ValueError(f'Could not locate attribute path={path}')


def replace_string(node, parameters):
    match = re.fullmatch(PARAMETER_REGEX, node)
    if match:
        return nested_chain_map(match.group(1), parameters)

    matches = list(re.finditer(PARAMETER_REGEX, node))
    for match in matches[::-1]:
        value = nested_chain_map(match.group(1), parameters)
        if not isinstance(value, (int, str, float)):
            raise ValueError(f'Cannot partially replace string="{node}" with non simple type (e.g. dict, list)')
        node = node[:match.start()] + str(value) + node[match.end():]
    return node


def replace_node(node, parameters):
    if isinstance(node, dict):
        return {key: replace_node(value, parameters) for key, value in node.items()}
    elif isinstance(node, list):
        return [replace_node(value, parameters) for value in node]
    elif isinstance(node, str):
        return replace_string(node, parameters)
    return node


def render_jobs(workflow_template):
    global_parameters = workflow_template.get("parameters", {})

    jobs = []
    for job_template in workflow_template['jobs']:
        if 'strategy' in job_template and 'matrix' in job_template['strategy']:
            for job_parameters in job_template['strategy']['matrix']:
                job_parameters = replace_node(job_parameters, [global_parameters])
                rendered_job = replace_node(job_template, [global_parameters, job_parameters])
                rendered_job['strategy'].pop('matrix')
                jobs.append(rendered_job)
        else:
            job_parameters = replace_node(job_template.get('parameters', {}), [global_parameters])
            rendered_job = replace_node(job_template, [global_parameters, job_parameters])
            rendered_job.pop('parameters', None)
            jobs.append(rendered_job)
    return jobs


def render(filename, format='yaml'):
    with open(filename) as f:
        workflow_template = yaml.safe_load(f)

    validate_schema(workflow_template)

    rendered_template = {
        'name': workflow_template['name'],
        'version': workflow_template['version'],
        'jobs': render_jobs(workflow_template)
    }

    if format == 'yaml':
        return yaml.dump(rendered_template, default_flow_style=False, sort_keys=False)
    elif format == 'json':
        return json.dumps(rendered_template)
    else:
        raise ValueError('format="{format}" not recognized output format for rendering')
