---
id: computing-software.cloud-infrastructure-engineering.alertmanager.amtool-config-routes
name: amtool-config-routes
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, amtool, route-testing, verify-receivers]
level: practitioner
status: docs-checked
description: "amtool config routes: print the routing tree and test which receivers a label set matches, with --verify.receivers for CI exit codes."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing routes with amtool

`amtool config routes` visualizes the routing tree of a configuration as a text tree. `amtool config routes test` takes a label set and prints every receiver the alert would match, ordered and separated by `,`.

View the routing tree of a running Alertmanager:

```
amtool config routes --alertmanager.url=http://localhost:9093
```

Test a label set against a local file and compare with an expected receiver:

```
amtool config routes test --config.file=doc/examples/simple.yml --tree --verify.receivers=team-X-pager service=database owner=team-X
```

Flags and behaviour:
- `--config.file` points at a local configuration file, as in the README example.
- `--tree` prints the result in tree form.
- `--verify.receivers=<name>` makes amtool return error code 1 on mismatch, so it can gate a CI job.
- The trailing arguments are label pairs such as `service=database owner=team-X`.

The README says the test prints all receivers the alert would match, so the list may contain several names.

## Checked

2026-11-08. Confirmed against the Alertmanager README (amtool Routes section): tree view, routes test, --tree, --verify.receivers exit code 1 and the example commands. Removed: the continue: true remark and the amtool check-config pairing, which the README does not state.

Method: documentation only; no commands were run.
