---
id: computing-software.data-science-and-analytics.apache-superset.jinja-template-security
name: jinja-template-security
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [jinja, template-injection, url-param, untrusted-input, sql-injection]
level: advanced
status: docs-checked
description: "Avoid injection in Superset Jinja templates: SSTI trust model, url_param allowlists, where_in and quote escaping, guest attribute escaping."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/sql-templating.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep templated SQL from becoming an injection path.

Facts from the templating docs:
- Templates execute code on the server. Within Superset's security model this is intended: users with permission to edit charts and virtual datasets are trusted users.
- Granting those permissions to untrusted users can turn the feature into a Server-Side Template Injection (SSTI) vulnerability. `ENABLE_TEMPLATE_PROCESSING` defaults to False; enable it only if you need it and every user with dataset or chart edit access is an administrator or fully trusted.

Practices:
1. Treat `url_param()` values as untrusted. Escaping varies by context and configuration, so restrict values to an explicit allowlist:

```sql
{% set cc = url_param('countrycode') %}
{% if cc not in ('US', 'ES', 'FR') %}{% set cc = 'US' %}{% endif %}
WHERE country_code = '{{ cc }}'
```

2. `filter.get('val')` returns the raw filter value without escaping. For multi-value filters use `|where_in`; for single values such as `LIKE`, double single quotes: `{{ filter.get('val') | replace("'", "''") }}`.
3. `get_guest_user_attribute()` escapes string values by default through the database dialect's literal rendering. If you pass `escape_result=False`, or interpolate numbers or booleans, you must validate or allowlist them. Use `escape_result=False` before `|where_in` or `|tojson`, which quote on their own; escaping twice corrupts values such as `O'Brien`. Interpolating a whole array or object renders Python's string form, which is not valid SQL.
4. Do not enable template processing on deployments where untrusted users can edit datasets or charts.

## Checked

2026-11-08: read sql-templating.mdx in full. Removed claims not on the page: minimum-privilege database user, permission names such as `can_sql_json`, hostile-input testing and row level security advice, and `cache_key_wrapper` wrapping advice.
Method: documentation only; no commands were run.
