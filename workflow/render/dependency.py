def validate_dependencies(workflow_template):
    topological_sort(workflow_template["jobs"])


def topological_sort(jobs):
    dependencies = {job["name"]: job for job in jobs}
    edges = {
        job["name"]: set(job.get("depends_on", []))
        for job in jobs
        if len(job.get("depends_on", [])) != 0
    }
    empty_edges = set(
        job["name"] for job in jobs if len(job.get("depends_on", [])) == 0
    )
    sorted_jobs = []

    while empty_edges:
        job_name = empty_edges.pop()
        sorted_jobs.append(dependencies[job_name])

        new_edges = {}
        for _job_name, depends_on in edges.items():
            depends_on.discard(job_name)
            if len(depends_on) == 0:
                empty_edges.add(_job_name)
            else:
                new_edges[_job_name] = depends_on
        edges = new_edges

    if len(edges) != 0:
        raise ValueError(
            f"cycle detected in jobs remaining unsatisfiable edges={edges}"
        )

    return sorted_jobs
