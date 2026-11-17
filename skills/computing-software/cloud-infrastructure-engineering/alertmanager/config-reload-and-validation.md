---
id: computing-software.cloud-infrastructure-engineering.alertmanager.config-reload-and-validation
name: config-reload-and-validation
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, config-reload, sighup, check-config]
level: intro
status: docs-checked
description: "How Alertmanager loads alertmanager.yml, reloads it at runtime via SIGHUP or POST /-/reload, and validates it with amtool check-config."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loading, reloading and validating configuration

Alertmanager is configured with command-line flags and a configuration file. Flags set immutable system parameters; the file defines inhibition rules, routing and receivers. Run `alertmanager -h` to list all flags.

Load a file with `--config.file`:

```
./alertmanager --config.file=alertmanager.yml
```

Runtime reload: Alertmanager can reload its configuration without restarting. A reload is triggered by sending `SIGHUP` to the process or by an HTTP `POST` to `/-/reload`. If the new configuration is not well-formed, the changes are not applied and an error is logged.

Validate before deploying with amtool; no running server is needed:

```
amtool check-config config.yml
Checking 'config.yml'  SUCCESS
Found:
 - global config
 - route
 - 2 inhibit rules
 - 2 receivers
 - 0 templates
```

The same command can be run with `--enable-feature="utf8-strict-mode"` to confirm matchers are compatible with the strict parser; a failure prints `FAILED` and amtool exits with `failed to validate 1 file(s)`.

The file is YAML. Brackets in the reference mark optional parameters; for non-list parameters the value is set to the stated default. A visual editor for routing trees is linked from the configuration page.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): --config.file, SIGHUP and /-/reload reload, amtool check-config output.

Method: documentation only; no commands were run.
