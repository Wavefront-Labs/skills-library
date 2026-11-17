---
id: computing-software.data-engineering.apache-airflow.sharing-code-with-plugins-and-include
name: sharing-code-with-plugins-and-include
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-plugins, include-folder, shared-code, pythonpath]
level: practitioner
status: docs-checked
description: "Share helper code across Airflow DAGs via the dags-folder package layout, an installable internal package, or plugins, and know what plugins are still for in Airflow 3."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/plugins.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing code between DAGs: packages, include folders, plugins

**Goal:** reuse hooks, callbacks and helper functions across DAGs without import errors on schedulers/workers and without slowing DAG parsing.

## What Airflow puts on sys.path
The `dags/`, `plugins/` and `config/` folders are added to `sys.path`. So `dags/common/alerts.py` is importable as `from common.alerts import on_failure`.

## Options, in order of preference
1. **Internal Python package** (`pip install my-company-airflow-utils==1.4.2` baked into the image). Versioned, testable, same code on every component. Best for anything non-trivial.
2. **Package inside the dags folder** with an `__init__.py`:
   ```
   dags/
     common/__init__.py
     common/alerts.py
     sales/daily_orders.py      # from common.alerts import on_failure
   ```
   Add `common/` to `.airflowignore` so the DAG processor does not parse helpers looking for DAGs:
   ```
   common/
   ```
3. **Plugins** only for things that must be registered with Airflow: custom macros, timetables, listeners, UI extensions (Airflow 3: FastAPI apps, external views/React apps; Airflow 2: Flask blueprints/views), operator extra links.

## Do not put operators/hooks in plugins
Operators and hooks are plain Python imports, so put them in a package rather than registering them through a plugin.

## Plugin skeleton
```python
# plugins/company_plugin.py
from airflow.plugins_manager import AirflowPlugin
from company.timetables import BusinessDaysTimetable

class CompanyPlugin(AirflowPlugin):
    name = "company"
    timetables = [BusinessDaysTimetable]
    macros = []
```
- `airflow plugins` lists what loaded; import failures show there and in the UI.
- Plugins are loaded lazily by default (`[core] lazy_load_plugins = True`); changing plugin code needs a restart of the components that use it.

## Gotchas
- Name collisions: a top-level `dags/utils.py` or `dags/airflow.py` shadows real modules. Use a unique top-level package name.
- Heavy imports at module level of a shared helper slow every DAG that imports it: import inside functions.
- Timetables used by DAGs must be registered as plugins, or the scheduler cannot deserialize the DAG.

## Verify
`python -c "import common.alerts"` from inside the scheduler container, and `airflow dags list-import-errors` is empty.

## Checked

2026-10-28. Confirmed: lazy_load_plugins default behaviour (set to False to load at process start) on the plugins page. Removed: an unconfirmed removal claim.

Method: documentation only; no commands were run.
