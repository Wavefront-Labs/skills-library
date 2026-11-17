---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.debug-mode-hooks
name: debug-mode-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, debug-mode, hook-conf, dynamic-debug, tracing, troubleshooting]
level: advanced
status: docs-checked
description: "Use APISIX advanced debug hooks in debug.yaml: hook_conf settings, the hook_phase module list, the #END marker and per-request tracing with X-APISIX-Dynamic-Debug."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/debug-mode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced debug hooks

`hook_conf` keys in `conf/debug.yaml`:
- `enable`: false; turns hook tracing on.
- `name`: the module list to hook.
- `log_level`: `warn`.
- `is_print_input_args`: true; `is_print_return_value`: true.

```yaml
hook_conf:
  enable: true
  name: hook_phase
  log_level: warn
  is_print_input_args: true
  is_print_return_value: true

hook_phase:
  apisix:
    - http_access_phase
    - http_header_filter_phase
    - http_body_filter_phase
    - http_log_phase
#END
```

`#END` tells the checker to stop reading. The file is re-read only when its modification time changes.

Per-request tracing: set `http_filter.enable: true` and `enable_header_name: X-APISIX-Dynamic-Debug` in `debug.yaml`. Only requests carrying that header are traced, for example `curl 127.0.0.1:9090/hello --header 'X-APISIX-Dynamic-Debug: foo'`. `apisix.http_access_phase` cannot be hooked this way.

## Checked

2026-11-04: read the Debug Mode page (advanced section); hook_conf keys and defaults, the hook_phase example, the #END and modification-time note, http_filter with enable_header_name, and the access-phase limitation match. Nothing removed.

Method: documentation only; no commands were run.
