---
id: computing-software.data-engineering.apache-airflow.custom-operators-and-hooks
name: custom-operators-and-hooks
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, custom-operator, airflow-hooks, baseoperator, basehook, template-fields, get-connection, provider-package, plugins]
level: advanced
status: docs-checked
description: "Write custom Airflow operators and hooks: BaseHook with connections, BaseOperator.execute, template_fields, no work in __init__, packaging as an internal provider, and testing."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html
  - https://airflow.apache.org/docs/apache-airflow-providers/howto/create-custom-providers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom operators and hooks

**Goal:** wrap an internal system (API, warehouse, tool) once, so DAG authors use a tested, templated operator instead of copy-pasted Python.

## Hook: owns the connection
```python
from airflow.sdk import BaseHook                  # Airflow 3 (airflow.hooks.base in 2.x)
import requests

class AcmeApiHook(BaseHook):
    def __init__(self, acme_conn_id: str = "acme_default"):
        super().__init__()
        self.acme_conn_id = acme_conn_id

    def get_session(self):
        c = self.get_connection(self.acme_conn_id)      # host, login, password, extra
        s = requests.Session()
        s.headers["Authorization"] = f"Bearer {c.password}"
        s.base_url = f"https://{c.host}"
        return s
```

## Operator: does one job
```python
from airflow.sdk import BaseOperator               # airflow.models.BaseOperator in 2.x

class AcmeExportOperator(BaseOperator):
    template_fields = ("report", "dest_path")       # rendered with Jinja ({{ ds }}, params)

    def __init__(self, *, report: str, dest_path: str, acme_conn_id: str = "acme_default", **kwargs):
        super().__init__(**kwargs)
        self.report, self.dest_path, self.acme_conn_id = report, dest_path, acme_conn_id   # store only

    def execute(self, context):
        s = AcmeApiHook(self.acme_conn_id).get_session()
        r = s.get(f"{s.base_url}/reports/{self.report}", timeout=60)
        r.raise_for_status()
        write_to_storage(self.dest_path, r.content)
        return self.dest_path                         # pushed to XCom
```

## Rules
- **No I/O in `__init__`** or at module level: operators are instantiated on every DAG parse (at least every `min_file_process_interval` seconds per file). Connections, API calls, and heavy imports go in `execute`.
- Put templated attributes in `template_fields`; add `template_ext = (".sql",)` to render file contents.
- Make `execute` idempotent (retries rerun it).
- Raise `AirflowSkipException` to skip, `AirflowFailException` to fail without retries.
- Long waits: implement a deferrable version (see the deferring docs) instead of sleeping in a worker slot.

## Packaging
Ship as an internal Python package (`acme-airflow-provider` is a placeholder name) installed into the Airflow image, with a `get_provider_info` entry point as in the custom-providers page. Avoid the `plugins/` folder for operators: plain imports from an installed package version cleanly.

## Testing
```python
def test_export(mocker):
    mocker.patch.object(AcmeApiHook, "get_session", return_value=fake_session)
    op = AcmeExportOperator(task_id="t", report="sales", dest_path="/tmp/x")
    assert op.execute(context={}) == "/tmp/x"
```

## Verify
- [ ] DAG file parse time unaffected (`airflow dags report` shows low duration).
- [ ] Templated fields render correctly (`airflow tasks render <dag> <task> <date>`).
- [ ] Unit tests mock the hook; one integration test hits a sandbox.

## Checked

2026-10-28. Confirmed against: custom-operator page (execute-time hooks, template_ext, AirflowSkipException/AirflowFailException, min_file_process_interval), CLI reference (airflow tasks render, dags report), custom providers page (get_provider_info), airflow.sdk BaseOperator/BaseHook import mapping. Removed (not confirmable in the fetched pages): hook class attributes, ui_color, defer call signature, 30 s figure, UI claim for connection type.

Method: documentation only; no commands were run.
