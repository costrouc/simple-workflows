import copy

import pytest

from workflow.render.configuration import render_configuration


BASE_WORKFLOW_TEMPLATE = {
    "name": "configuration tests",
    "version": 1,
    "jobs": [
        {
            "name": "job1",
            "runs": "replace me",
            "config": [
                {
                    "filename": "replace me",
                    "format": "replace me",
                    "data": {"a1": {"key1": True, "key2": 1}, "a2": {"key1": 1.2,}},
                }
            ],
        }
    ],
}


EXPECTED = {
    "ini": """[a1]
key1 = True
key2 = 1

[a2]
key1 = 1.2
""",
    "toml": """[a1]
key1 = true
key2 = 1

[a2]
key1 = 1.2
""",
    "json": """{
    "a1": {
        "key1": true,
        "key2": 1
    },
    "a2": {
        "key1": 1.2
    }
}
""",
    "yaml": """a1:
  key1: true
  key2: 1
a2:
  key1: 1.2
""",
}


@pytest.mark.parametrize("format", ["ini", "yaml", "json", "toml"])
def test_configuration(format, tmp_path):
    directory = tmp_path / format
    directory.mkdir()

    workflow_template = copy.deepcopy(BASE_WORKFLOW_TEMPLATE)

    workflow_template["jobs"][0]["runs"] = f"cat {directory}/config.{format}"
    workflow_template["jobs"][0]["config"][0][
        "filename"
    ] = f"{directory}/config.{format}"
    workflow_template["jobs"][0]["config"][0]["format"] = format
    assert (
        render_configuration(workflow_template["jobs"][0]["config"][0]["data"], format)
        == EXPECTED[format]
    )
