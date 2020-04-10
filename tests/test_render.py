import pytest
import yaml

from workflow.render.format import render_formatted


@pytest.mark.parametrize(
    "output_format", ["bash", "yaml", "json", "airflow", "systemd"]
)
def test_render(output_format):
    filename = "tests/assets/simple.yaml"
    with open(filename) as f:
        workflow_template = yaml.safe_load(f)

    render_formatted(workflow_template, output_format)
