---
id: computing-software.cloud-infrastructure-engineering.alertmanager.matcher-composition
name: matcher-composition
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, matchers, composition, promql-style]
level: practitioner
status: docs-checked
description: "Composing several Alertmanager matchers: YAML list versus brace expression, optional braces, trailing comma, whitespace rules."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Composing matchers

When matchers are composed, all of them must match for the whole expression to match. `{alertname="Watchdog", severity=~"warning|critical"}` matches an alert named Watchdog whose severity is warning or critical.

Two equivalent forms:

```yaml
matchers:
  - alertname = Watchdog
  - severity =~ "warning|critical"
```

or a PromQL-inspired string with comma-separated matchers:

```
{alertname="Watchdog", severity=~"warning|critical"}
```

Rules:
- A single trailing comma is permitted.
- The open `{` and close `}` braces are optional, but both must be present or both omitted. A lone open or close brace is an error, as are duplicated braces such as `{{...}}`.
- Whitespace (spaces, tabs, newlines) is permitted outside double quotes and has no effect.

More examples:

```yaml
matchers: [ foo = bar, dings != bums ]
matchers: [ '{foo="bar", dings!="bums"}' ]
```

In the short form, prefer double quotes around entries to avoid problems with commas; single quotes work best for the PromQL-like string.

The same matcher syntax applies to routes, silences and inhibition rules.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: how matchers combine. Removed: nothing.

Method: documentation only; no commands were run.
