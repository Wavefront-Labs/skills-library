---
id: computing-software.cloud-infrastructure-engineering.alertmanager.amtool-alert-queries
name: amtool-alert-queries
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, amtool, alert-query, output-extended]
level: practitioner
status: docs-checked
description: "amtool alert commands: list firing alerts, extended output with -o, and querying with equality and regex matchers."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# amtool alert and alert query

`amtool` is a command-line tool for interacting with the Alertmanager API, bundled with all Alertmanager releases. Alternatively install it with:

```
go install github.com/prometheus/alertmanager/cmd/amtool@latest
```

View all currently firing alerts:

```
amtool alert
```

Columns shown are Alertname, Starts At and Summary. Extended output adds labels, annotations, end time and generator URL:

```
amtool -o extended alert
```

Query with the Alertmanager matcher syntax:

```
amtool -o extended alert query alertname="Test_Alert"
amtool -o extended alert query instance=~".+1"
amtool -o extended alert query alertname=~"Test.*" instance=~".+1"
```

Multiple matchers are combined, so the third query returns only alerts satisfying both.

The server address comes from `--alertmanager.url` or from `alertmanager.url` in the amtool configuration file. The `-o` flag selects the output format; the configuration file can set a default through its `output` key (unset defaults to `simple`).

## Checked

2026-11-08. Confirmed against the Alertmanager README (amtool section): go install, amtool alert, -o extended, alert query examples and the amtool configuration keys.

Method: documentation only; no commands were run.
