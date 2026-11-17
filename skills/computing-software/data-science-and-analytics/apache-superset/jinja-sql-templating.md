---
id: computing-software.data-science-and-analytics.apache-superset.jinja-sql-templating
name: jinja-sql-templating
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [jinja, sql-templating, template-processing, jinja-context, template-processors]
level: practitioner
status: docs-checked
description: "Enable Jinja templating in Superset SQL: ENABLE_TEMPLATE_PROCESSING, default context variables, JINJA_CONTEXT_ADDONS and CUSTOM_TEMPLATE_PROCESSORS."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/sql-templating.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make SQL Lab queries and virtual datasets dynamic.

SQL Lab and Explore support Jinja in queries when the `ENABLE_TEMPLATE_PROCESSING` feature flag is on in `superset_config.py` (default False). Python code can then be embedded in virtual datasets and in Custom SQL in filter and metric controls.

```python
FEATURE_FLAGS = {"ENABLE_TEMPLATE_PROCESSING": True}
```

Default context variables: `columns`, `filter`, `groupby` (deprecated), `metrics`, `row_limit`, `row_offset`, `table_columns`, `time_column` (None if undefined), `time_grain` (None if undefined). Some, like `filter`, are only populated when a chart or dashboard supplies them (Explore time range filters, dashboard native filters, filter components).

Syntax: parameters use double braces in the query and single-brace blocks for logic, for example:

```sql
{% set tf = get_time_filter("dttm_col") %}
SELECT * FROM tbl
WHERE dttm_col > {{ tf.from_expr }} AND dttm_col <= {{ tf.to_expr }}
```

Extension points in `superset_config.py`:
- `JINJA_CONTEXT_ADDONS`: dict of objects made available wherever the Jinja context is, e.g. `{'my_crazy_macro': lambda x: x*2}`.
- `CUSTOM_TEMPLATE_PROCESSORS`: dict mapping an engine to a processor class (a subclass such as `PrestoTemplateProcessor` overriding `process_template`); it overwrites the default Jinja processor for that engine, so templates on that database use the custom one (the docs' example uses `$` macros instead of `{{ }}`).

SQL Lab parameters: the Parameters menu takes JSON such as `{"my_table": "foo"}`, usable as `{{ my_table }}` and stored with the dataset as TEMPLATE PARAMETERS. The special `_filters` parameter tests filter macros in the SQL Lab UI only and is not stored.

Live query validation is separate: `SQL_VALIDATORS_BY_ENGINE` under `FEATURE_FLAGS` maps an engine to a validator such as `PrestoDBSQLValidator`.

Security: templates execute on the server. Users who can edit charts and virtual datasets are treated as trusted; granting that to untrusted users can allow server-side template injection (see the Jinja security skill).

## Checked

2026-11-08: read sql-templating.mdx in full. Removed claims not on the page: the `from_dttm` variable and `current_username()` as a region filter example, "test in SQL Lab first" and "keep logic small" advice.
Method: documentation only; no commands were run.
