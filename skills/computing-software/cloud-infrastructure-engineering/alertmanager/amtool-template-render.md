---
id: computing-software.cloud-infrastructure-engineering.alertmanager.amtool-template-render
name: amtool-template-render
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, amtool, template-render, template-glob]
level: advanced
status: docs-checked
description: "Previewing Alertmanager notification templates offline with amtool template render, using --template.glob and --template.text."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# amtool template render

amtool can preview how a template renders. Suppose the configuration lists template files:

```yaml
templates:
  - '/path/to/templates/*.tmpl'
```

Then render a named template with example data:

```
amtool template render --template.glob='/path/to/templates/*.tmpl' --template.text='{{ template "slack.default.markdown.v1" . }}'
```

Flags:
- `--template.glob`: which template files to load; the glob mirrors the entries under `templates`.
- `--template.text`: the template text to evaluate; here it calls a named template with the root data `.`.

The data structure real notifications receive is documented as `Receiver`, `Status`, `Alerts`, `GroupLabels`, `CommonLabels`, `CommonAnnotations`, `RouteLabels` and `ExternalURL`.

Related: the notification template documentation lists available functions, and the configuration page notes that the last component of a `templates` path may use a wildcard such as `templates/*.tmpl`.

## Checked

2026-11-03. Confirmed against the Alertmanager README (amtool template render example) and the Notification template reference. Removed: the generic 'use it to test' advice naming functions.

Method: documentation only; no commands were run.
