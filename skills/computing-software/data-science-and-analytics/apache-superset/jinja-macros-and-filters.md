---
id: computing-software.data-science-and-analytics.apache-superset.jinja-macros-and-filters
name: jinja-macros-and-filters
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [jinja, macros, filter-values, where-in, cache-key-wrapper]
level: advanced
status: docs-checked
description: "Use Superset Jinja macros: current_username, url_param, filter_values, get_filters, get_time_filter, dataset, metric, cache_key_wrapper and where_in."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/sql-templating.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right built-in macro for a templated query. Requires `ENABLE_TEMPLATE_PROCESSING` (default False).

User macros: `current_username()`, `current_user_id()`, `current_user_email()` and `current_user_roles()` (an array), plus `current_user_rls_rules()` (RLS rules on the current dataset). With caching enabled, each value is included in the cache key by default; pass `add_to_cache_keys=False` to opt out. `{{ current_user_roles()|tojson }}` stringifies the array, and `IN {{ current_user_roles()|where_in }}` renders like `('admin', 'viewer')`.

- `url_param('name')`: reads a URL parameter. Treat as untrusted and allowlist it before use in SQL.
- `get_guest_user_attribute('name', default=..., escape_result=...)`: guest-token attribute for embedded dashboards; string values are escaped by default; use `escape_result=False` before `|where_in` or `|tojson`, which quote on their own.
- `filter_values('column')`: values of a filter as a list. Pair with `|where_in`.
- `get_filters('column', remove_filter=True)`: filters for a column including the operator; loop over it and branch on `filter.get('op')`. `filter.get('val')` is raw and unescaped, so use `|where_in` for lists and `| replace("'", "''")` for single values like `LIKE`.
- `get_time_filter(column, default, target_type, strftime, remove_filter)`: returns an object with `from_expr`, `to_expr` and `time_range`; use `from_expr` and `to_expr` directly in WHERE without quoting. `remove_filter=True` marks the filter processed so it is removed from the outer query. `default` is used when the filter is absent or is No filter.
- `dataset(id)`: query a physical or virtual dataset as a table, e.g. `SELECT * FROM {{ dataset(42) }}`; `include_metrics=True` adds metrics (grouped by non-metric columns, or by `columns=[...]`).
- `metric('metric_key', dataset_id)`: returns a metric's SQL; `dataset_id` is optional and defaults to the current dataset.
- `cache_key_wrapper(value)`: adds a value to the cache key; only needed for your own custom function return values (it already powers the user id and username caching).

Filters: `|where_in` converts a list to a SQL `IN` body, giving `('First', 'Second', 'Third')`; an empty value gives `()`, or None with `where_in(default_to_none=True)`. `|to_datetime(format=...)` loads a string as a datetime for date arithmetic. Standard Jinja2 builtin filters also work.

```sql
SELECT action, count(*) AS times
FROM logs
WHERE action IN {{ filter_values('action_type')|where_in }}
GROUP BY action
```

## Checked

2026-11-08: read sql-templating.mdx in full. Removed claims not on the page: wrapping `current_username()` in `cache_key_wrapper` (it is cached by default), the "provide a default" rule, and the owner-filter example.
Method: documentation only; no commands were run.
