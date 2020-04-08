import configparser
import io
import json

import yaml


def render_configuration(config, format):
    if format == 'ini':
        return render_ini(config)
    elif format == 'yaml':
        return yaml.dump(config, default_flow_style=False, sort_keys=False)
    elif format == 'json':
        return json.dumps(config, indent=4)
    else:
        raise ValueError(f'configuration format={format} not supported')


def render_ini(config):
    parser = configparser.ConfigParser()
    parser.read_dict(config)

    content = io.StringIO()
    parser.write(content)
    content.seek(0)
    return content.read().strip()
