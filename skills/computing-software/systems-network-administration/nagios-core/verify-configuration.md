---
id: computing-software.systems-network-administration.nagios-core.verify-configuration
name: verify-configuration
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, verify-config, nagios-v, preflight, config-check, syntax-check]
level: intro
status: docs-checked
description: "Check a Nagios Core configuration with nagios -v before every restart, how to read errors versus warnings, and why a bad config stops the daemon."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/verifyconfig.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verify the configuration before restarting

Command:

```
/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
```

## Rules
- Run it after every configuration change and before any restart or reload: Nagios shuts down if the config has errors.
- Errors usually name the file and line. Verification often stops at the first error, so fix it and rerun until clean.
- Warnings are recommendations; the docs say they can generally be ignored. Errors cannot.
- Restart only after a clean run (see `computing-software.systems-network-administration.nagios-core.start-stop-reload`).

## Related
- `nagios -pv` also writes the precached object file (see `computing-software.systems-network-administration.nagios-core.fast-startup-precache`).
- `-s` prints per-stage startup timings.

## Checked

2026-11-04. Confirmed against the Verifying Your Configuration page (nagios -v command, shutdown on errors, first error often ends the check, warnings can generally be ignored) and the Fast Startup page for -pv and -s. Removed an unconfirmed self-check about an error total.

Method: documentation only; no commands were run.
