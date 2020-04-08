import itertools

AIRFLOW_HEADER = '''
from airflow import DAG
from airflow.operators.bash import BashOperator
'''

job_counter = itertools.count()


def render_airflow(rendered_template):
    airflow_script = [AIRFLOW_HEADER]

    airflow_script.append(f'dag = DAG(dag_id="{rendered_template["name"]}")')

    for job in rendered_template['jobs']:
        job_id = str(next(job_counter))
        airflow_script.append(f'task_{job_id} = BashOperator(task_id="{job["name"]}", bash_command="", dag=dag)')

    return '\n'.join(airflow_script).strip()
