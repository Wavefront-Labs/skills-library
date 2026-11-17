---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-config-files-and-directories
name: crowdsec-config-files-and-directories
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [config-yaml, yaml-local, environment-variables, config-directory, acquis-d, profiles-yaml]
level: practitioner
status: docs-checked
description: "Where CrowdSec keeps its configuration, how environment variables and .yaml.local overrides work, and the log and pipeline directives in config.yaml."
sources: ["https://docs.crowdsec.net/docs/configuration/crowdsec_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The main file is `/etc/crowdsec/config.yaml` for both the Log Processor and the Local API. Related paths under `/etc/crowdsec/`:

- `acquis.yaml` and `acquis.d/`: datasource definitions
- `bouncers/*.yaml`: per-bouncer configuration
- `collections/`, `parsers/`, `scenarios/`: installed content
- `contexts/*.yaml`: alert context
- `hub/`: local Hub mirror; never put custom items here
- `local_api_credentials.yaml` and `online_api_credentials.yaml`: credentials for the Local API and Central API
- `profiles.yaml`: alert-to-decision rules
- `notifications/*.yaml`: notification plugin configs
- `appsec-configs/` and `appsec-rules/`: WAF configuration and rules
- `simulation.yaml`: scenarios in simulation mode

## Environment variables

Values can reference environment variables, for example a database password. From 1.5.0 an undefined variable leaves the original string untouched so literal `$` characters in passwords survive; older versions substituted an empty string.

## Local overrides

Instead of editing `config.yaml` (which a package upgrade may offer to replace), write local settings to a `.yaml.local` file next to it. Mappings are merged and sequences are replaced. `profiles.yaml` is the exception: its local file is read as a whole, as if appended.

## Common directives

Under `common`: `log_media` (`stdout`, `file` or `syslog`), `log_level` (`error`, `info`, `debug`, `trace`), `log_dir`, `log_max_size` (MB, default 500), `log_max_age`, `log_max_files` (default 3 old files), `compress_logs` and `log_format` (`text` or `json`).

`crowdsec_service.pipeline` sizes the stages with `parser.routines`, `bucket.routines` and `output.routines` (each default 1) and `output.queue_size` (default 256). When the output queue overflows because a postoverflow such as a reverse DNS lookup is slow, overflows are dropped deliberately rather than pushed without whitelist checks.

## Checked

2026-11-03. Confirmed against the CrowdSec configuration page: directory and file list, environment-variable substitution and the 1.5.0 behaviour, .yaml.local merge rules and the profiles.yaml exception, common log directives and defaults (500 MB, 3 old files), and pipeline routines, queue_size 256 and the deliberate drop on a full postoverflow queue. Removed: nothing.

Method: documentation only; no commands were run.
