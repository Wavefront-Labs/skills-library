---
id: computing-software.software-engineering.deno.env-vars-special-deno-variables
name: env-vars-special-deno-variables
category: computing-software
field: software-engineering
product: deno
tags: [environment-variables, deno-dir, proxy, certificates, deno-no-prompt, deno-install-root]
level: advanced
status: docs-checked
description: "Environment variables that change Deno's behaviour: cache dir, certificates, proxies, prompts, install root, test jobs, permission audit and tracing."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/env_variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Paths and caches: `DENO_DIR` sets the cache directory. `DENO_INSTALL_ROOT` sets the `deno install` root (executables go in its `bin`, default `$HOME/.deno`). `DENO_INSTALL` picks where the shell install script puts `$DENO_INSTALL/bin/deno`. `DENO_REPL_HISTORY` sets the history file (empty disables).

TLS: `DENO_TLS_CA_STORE` is a comma-separated, ordered list of `system`, `mozilla` (default `mozilla`). `DENO_CERT` loads a PEM file (same as `--cert`). `NODE_EXTRA_CA_CERTS` adds CAs for `fetch()`, `Deno.connectTls()` and Node APIs (Deno 2.8+); a bad file warns rather than fails.

Network: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` (comma-separated hosts), `NPM_CONFIG_REGISTRY`, `DENO_AUTH_TOKENS`.

Behaviour: `DENO_NO_PROMPT` disables permission prompts (alternative to `--no-prompt`). `DENO_NO_UPDATE_CHECK`, `DENO_NO_PACKAGE_JSON`, `NO_COLOR`, `DENO_V8_FLAGS`, `DENO_CONDITIONS` (same as `--conditions`), `DENO_UNSTABLE_TSGO=1` (native tsgo type-check).

Testing: `DENO_COVERAGE_DIR` (only `deno test`); `DENO_JOBS` workers for `--parallel`, default CPU count.

Security: `DENO_AUDIT_PERMISSIONS` takes a file path for JSONL, or `otel` for OpenTelemetry log records. `DENO_TRACE_PERMISSIONS=1` adds stack traces to prompts (costs performance).

Other: `DENO_KV_ACCESS_TOKEN`, `DENO_WEBGPU_TRACE`, `DENO_WEBGPU_BACKEND` (`vulkan`, `dx12`, `metal`, `opengl`).

## Checked

2026-11-04. Confirmed against docs runtime/reference/env_variables.md: each listed variable against the special-variables table, including defaults, Deno 2.8 gate for NODE_EXTRA_CA_CERTS and WebGPU backend values.

Method: documentation only; no commands were run.
