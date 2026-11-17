---
id: computing-software.cloud-infrastructure-engineering.alertmanager.template-functions
name: template-functions
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, templating, template-functions, tojson, tz]
level: advanced
status: docs-checked
description: "Alertmanager template functions beyond Go defaults: append, date, dict, join, match, reReplaceAll, routeLabels, since, toJson, tz, title and more."
sources: ["https://prometheus.io/docs/alerting/latest/notifications/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Template functions

Alertmanager adds these functions to the standard Go template functions.

- `append slice args...`: new slice with args appended.
- `base64decode text` / `base64encode text`: URL-safe base64 (`URLEncoding`).
- `date format time`: text representation of a time; formats follow Go's `time` package.
- `dict values...`: map of string to any; an even number of arguments, keys must be strings.
- `humanizeDuration`: human-readable duration from a number or string.
- `join sep s`: `strings.Join` with the separator first, for easy pipelining.
- `list ...`: arguments as a slice of interfaces. `stringSlice ...`: strings as a slice of strings.
- `match pattern string`: regexp match.
- `now`: current local time. `since time`: duration since the given time.
- `reReplaceAll pattern replacement text`: unanchored regexp substitution.
- `routeLabels name`: value of the named route label for this group, or `""`.
- `safeHtml text` / `safeUrl text`: mark a string as HTML or URL not needing auto-escaping.
- `title`: capitalise the first character of each word. `toLower`, `toUpper`, `trimSpace`.
- `toJson`: JSON encoding of a value.
- `tz zone time`: time in a zone such as `Europe/Paris`.
- `urlUnescape text`: `url.QueryUnescape`.

```
{{ .StartsAt | tz "Europe/Paris" | date "2006-01-02 15:04" }}
{{ reReplaceAll "(.*):[0-9]+" "$1" .Labels.instance }}
```

## Checked

2026-11-03. Confirmed against the Notification template reference: function table.

Method: documentation only; no commands were run.
