---
id: computing-software.cloud-infrastructure-engineering.fluentd.system-directive-settings
name: system-directive-settings
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, system, workers, root-dir, log-level, umask, enable-jit, config-include-dir]
level: practitioner
status: docs-checked
description: "Reference for the Fluentd system directive: workers, root_dir, log_level, permissions, umask, strict_config_value, config_include_dir, JIT and metrics flags."
sources:
  - https://docs.fluentd.org/deployment/system-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd system directive
Key `<system>` parameters (version shown where the page gives it):
- `workers` (default 1); `restart_worker_interval` (1.15.0, default 0 = restart stopped workers immediately).
- `root_dir`: base for buffers, storage, backup and evacuated chunks when plugins have `@id`.
- `log_level` (default `info`), `suppress_repeated_stacktrace`, `emit_error_log_interval`, `ignore_repeated_log_interval` (1.10.2), `ignore_same_log_interval` (1.11.3), `suppress_config_dump`, `log_event_verbose`.
- `without_source`; `with_source_only` (1.18.0, not on Windows; see `source-only-mode`).
- `rpc_endpoint`, `enable_get_dump`, `process_name`.
- `file_permission`, `dir_permission`, `umask` (1.20.0; the `--umask` flag wins; applied to workers only with `--no-supervisor` or `--daemon`).
- `strict_config_value` (1.8.0): bad numeric or boolean values raise errors instead of becoming `0` or `true`.
- `disable_shared_socket` (1.12.1): shared socket lets workers listen on one port.
- `config_include_dir` (1.19.0, default `/etc/fluent/conf.d`): files there load without `@include`; set `""` to disable.
- `enable_jit` (default true; since v1.20.0): YJIT raises per-worker memory; no effect on Windows.
- `enable_input_metrics` (default true since v1.19.0), `enable_size_metrics`.
- `enable_msgpack_time_support` (1.9.0, default false).
- `<source_only_buffer>`: temporary buffer for source-only mode (`flush_interval` 10, `chunk_limit_size` 256MB, `total_limit_size` 64GB, `overflow_action` `drop_oldest_chunk`, `path`).

For the `<log>` subsection see `logging-output-and-rotation`.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/system-config and confirmed: parameter names, versions, defaults, umask rules, source_only_buffer defaults. Removed or reworded: nothing.

Method: documentation only; no commands were run.
