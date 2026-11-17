---
id: computing-software.cloud-infrastructure-engineering.alertmanager.config-value-types
name: config-value-types
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, placeholders, duration-syntax, regex-anchoring]
level: intro
status: docs-checked
description: "Placeholder types used in the Alertmanager config reference: duration, labelname, regex anchoring, tmpl_string, secret and filepath."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Value types in the configuration reference

The configuration reference uses generic placeholders. Knowing their exact meaning avoids silent mistakes.

- `<duration>` matches `((([0-9]+)y)?(([0-9]+)w)?(([0-9]+)d)?(([0-9]+)h)?(([0-9]+)m)?(([0-9]+)s)?(([0-9]+)ms)?|0)`, for example `1d`, `1h30m`, `5m`, `10s`.
- `<labelname>` matches `[a-zA-Z_][a-zA-Z0-9_]*`.
- `<labelvalue>` is a string of Unicode characters.
- `<regex>` is any valid RE2 regular expression. The regex is anchored on both ends; to un-anchor it, use `.*<regex>.*`.
- `<tmpl_string>` is a string that is template-expanded before use; `<tmpl_secret>` is the same for a secret.
- `<secret>` is a regular string that is a secret, such as a password.
- `<filepath>` is a valid path in the current working directory.
- `<boolean>` takes `true` or `false`; `<int>` is an integer.

Example of the anchoring rule: a matcher `service=~"mysql|cassandra"` must match the whole label value. A value like `mysql-primary` is not matched unless the regex is written `mysql.*`.

Fields documented as `<tmpl_string>` (such as Slack `title` or PagerDuty `description`) are evaluated with Go templates, so they can reference the notification data structure.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference (generic placeholders list): the duration regex, labelname regex, labelvalue, filepath, boolean, string, secret, tmpl_string, tmpl_secret, int, and the RE2 regex anchored on both ends with the .*<regex>.* un-anchoring tip; Slack title and PagerDuty description are tmpl_string fields. The mysql-primary illustration follows from the anchoring rule.

Method: documentation only; no commands were run.
