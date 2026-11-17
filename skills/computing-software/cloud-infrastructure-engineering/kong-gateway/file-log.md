---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.file-log
name: file-log
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, file-log, log-file, reopen, plugins, logging]
level: intro
status: docs-checked
description: "file-log plugin: the path option (created if missing, special characters rejected), reopen default false for log rotation, and custom_fields_by_lua."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/file-log/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# file-log

Config:
- `path` (required): output log file. The plugin creates it if it does not exist. The value is rejected if it has leading or trailing whitespace or contains `*`, `&`, `%`, a backtick or a backslash ("not a valid filename").
- `reopen` (default `false`): when `true`, the file is closed and reopened on every request.
- `custom_fields_by_lua` (optional): map of log field names to Lua code whose return value sets or replaces that field.

`reopen: true` costs a close and open of the file on every request.

## Checked

2026-11-04. Confirmed against the file-log schema.lua: path required with the filename match pattern and "not a valid filename" error, created if missing, reopen default false, custom_fields_by_lua.

Method: documentation only; no commands were run.
