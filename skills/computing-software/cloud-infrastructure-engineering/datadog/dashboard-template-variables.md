---
id: computing-software.cloud-infrastructure-engineering.datadog.dashboard-template-variables
name: dashboard-template-variables
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, template-variables, dashboard-variables, saved-views, scoped-queries]
level: practitioner
status: docs-checked
description: "Add template variables so one dashboard can be filtered by env, service or host with saved views."
sources: ["https://docs.datadoghq.com/dashboards/template_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template variables and saved views
Goal: reuse one dashboard for many scopes.

Create a variable from the dashboard's template variable controls: pick the tag (the `<KEY>` of a `<KEY>:<VALUE>` tag) or an attribute, a name, a default value and the available values.

Widget query using variables:

```
avg:system.cpu.user{$env,$service} by {host}
```

- A variable is named after the selected tag by default. Default Value defaults to `*`; Available Values defaults to `(all)` and always includes `*`.
- A widget is filtered only if its query uses the variable (`$name` in the `from` field, or a group-by variable after `by`). You can apply or remove a variable on selected widgets, including Select All and Deselect All.
- Append `.value` to put the selected value into a query (`env:staging-$service.value`); in text widgets `$env.key` and `$env.value` display the key and value.
- Saved views store template variable selections. The Default view can be edited only by changing the variables' default values.
- Changing a value updates the URL parameter `&tpl_var_<NAME>=<VALUE>`, for example `&tpl_var_env=prod`, which you can share.
- Only a subset of variables shows in the header; click `+ N` or Expand template variables to see the rest.

Gotcha: widgets whose queries do not reference the variable ignore it, so a dashboard can look filtered while part of it is not. Review each widget. For event overlays the variable must be a metric tag, not an event tag.

## Verify
- Change a variable (for example env to staging) and confirm every widget's query value changes.

## Checked
2026-11-09. Confirmed against the Datadog template variables page: tag/attribute selection, name, Default Value `*`, Available Values `(all)`, apply to selected widgets, `$name.value` and `.key`, saved views and Default view rule, `tpl_var_` URL parameter, header `+ N`, metric-tag requirement for event overlays. Removed: the JSON `prefix`/`default` snippet (an API shape not on this page), the advice to keep variable names short and aligned with tag keys, and the per-team saved-view recommendation.
Method: documentation only; no commands were run.
