import getpass


def render_systemd(workflow_template):
    pass


def render_systemd_timer(name, timer):
    return f"""[Unit]
Description=Workflow Timer {name}

[Timer]
OnCalendar={timer}

[Install]
WantedBy=timers.target
"""


def render_systemd_service(name, command, user=None, group='nobody'):
    user = user or getpass.getuser()

    return f"""[Unit]
Description=Workflow Service {name}

[Service]
Type=oneshot
ExecStart={command}
User={user}
Group={group}
"""
