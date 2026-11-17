---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.debug-mode-basic
name: debug-mode-basic
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, debug-mode, debug-yaml, apisix-plugins-header, troubleshooting]
level: practitioner
status: docs-checked
description: "Turn on APISIX basic debug mode in conf/debug.yaml to see plugin execution order in the Apisix-Plugins response header, and know its inference limits."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/debug-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic debug mode

Set `basic.enable: true` in `conf/debug.yaml`. APISIX checks the file every second and applies changes automatically. (Before v2.10 the switch was `apisix.enable_debug = true` in `conf/config.yaml`.)

Effect: responses carry an `Apisix-Plugins` header listing `plugin-name#phase` entries in execution order, for example `limit-conn#access, limit-count#access, limit-conn#log`.

Limits:
- Phases after the response header is generated (`body_filter`, `log`) are inferred, not traced, so the header may not match real execution. A plugin skipped by its `_meta.filter` still appears.
- Phases that cannot be traced or inferred, such as global-rule plugins running after the header is sent, are written to the error log at `warn` level.

## Checked

2026-11-04: read the Debug Mode page (basic section); basic.enable, the 1-second file check, the pre-v2.10 switch, the Apisix-Plugins header example and both limitation paragraphs match. Nothing removed.

Method: documentation only; no commands were run.
