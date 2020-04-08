from workflow.render.dependency import validate_dependencies


def validate_job_names_unique(workflow_template):
    job_names = set()
    for job_template in workflow_template['jobs']:
        if job_template['name'] in job_names:
            raise ValueError('job names are not unique found duplicate job="{job_template["name"]}"')
        job_names.add(job_template['name'])


def validate_schema(workflow_template):
    validate_job_names_unique(workflow_template)
    validate_dependencies(workflow_template)
    return True
