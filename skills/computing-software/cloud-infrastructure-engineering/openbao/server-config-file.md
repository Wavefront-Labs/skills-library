---
id: computing-software.cloud-infrastructure-engineering.openbao.server-config-file
name: server-config-file
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, configuration, hcl, sighup, default-lease-ttl]
level: practitioner
status: docs-checked
description: "OpenBao server config file: HCL/JSON and directories, key top-level parameters with defaults, env vars, SIGHUP reload and risky options."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server configuration file

HCL or JSON, or a directory of `.hcl`/`.json` files loaded alphabetically. Duplicate scalar options: last wins; lists such as `listener` append. Start with `bao server -config ...`.

## Required and key parameters

- `storage` (required), `listener` (required), optional `ha_storage`, `seal`, `telemetry`, `user_lockout`, `audit`, `initialize`
- `default_lease_ttl` and `max_lease_ttl`: `"768h"`
- `default_max_request_duration`: `"90s"` (overridable per listener)
- `cache_size`: `"131072"` entries; `disable_cache` (false) hurts performance badly
- `ui` false; `raw_storage_endpoint` false (enables `sys/raw`, highly privileged); `introspection_endpoint` false
- `api_addr`, `cluster_addr`, `disable_clustering` (cannot be `true` with raft)
- `disable_ssct_tokens` true; `disable_standby_reads` false

## Environment variables

`BAO_UI`, `BAO_LOG_LEVEL`, `BAO_API_ADDR`, `BAO_CLUSTER_ADDR`, `BAO_ENABLE_FILE_PERMISSIONS_CHECK`.

## SIGHUP

Applies a valid `log_level` (overriding flag and env var) and can toggle `unsafe_allow_api_audit_creation`. Secrets and auth plugins keep their existing log level.

## Gotchas

- `detect_deadlocks` tracks every lock attempt and can hurt performance.
- Plugins: `plugin_directory`, `plugin_auto_download` (false), `plugin_auto_register` (true), `plugin_download_behavior` ("fail").

## Checked

2026-11-04. Read the OpenBao configuration overview page in full. Confirmed: HCL, JSON and directory loading rules, `-config`, every parameter and default listed, the environment variables, the SIGHUP behaviour and plugin options. Removed: nothing.
Method: documentation only; no commands were run.
