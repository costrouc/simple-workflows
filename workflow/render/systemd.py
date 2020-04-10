import getpass

from workflow.render.shell import render_bash


def render_systemd(workflow_template):
    return {
        "service": render_systemd_service(workflow_template["name"], "fake command"),
        "timer": render_systemd_timer(
            workflow_template["name"], workflow_template["trigger"]["systemd"]["timer"]
        ),
        "script": render_bash(workflow_template),
    }


def render_systemd_timer(name, timer):
    return f"""[Unit]
Description=Workflow Timer {name}

[Timer]
OnCalendar={timer}

[Install]
WantedBy=timers.target
"""


def render_systemd_service(name, command, user=None, group="nobody"):
    user = user or getpass.getuser()

    return f"""[Unit]
Description=Workflow Service {name}

[Service]
Type=oneshot
ExecStart={command}
User={user}
Group={group}
"""
