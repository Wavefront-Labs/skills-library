---
id: computing-software.networking-hardware-and-wireless.envoy.command-line-options
name: command-line-options
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, cli, concurrency, base-id, service-cluster, service-node, log-level, config-yaml, mode, validate]
level: practitioner
status: docs-checked
description: "Use the key Envoy CLI flags (-c, --mode validate, --concurrency, --base-id, --service-cluster/node, log level and path, drain times)."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/operations/cli.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# command line options
Common options from the CLI reference:
- `-c, --config-path <path>` bootstrap file, and `--config-yaml <yaml>` for an inline override merged on top.
- `--mode <string>`: `serve` (default) or `validate` (validate the configuration and exit: prints OK with exit code 0, or the errors with exit code 1; no network traffic and no hot restart).
- `--concurrency <int>` worker threads; if unset, it defaults to the minimum of the hardware thread count and the CPU affinity (cpuset) size.
- `-l, --log-level`, `--component-log-level upstream:debug,connection:trace`, `--log-path`, `--log-format`.
- `--base-id`, `--use-dynamic-base-id`, `--base-id-path`, `--restart-epoch`, `--disable-hot-restart`, `--parent-shutdown-time-s`, `--drain-time-s`, `--drain-strategy` for hot restart and draining.
- `--service-cluster`, `--service-node`, `--service-zone` identify the instance to the management server and zone aware routing.
- `--admin-address-path`, `--local-address-ip-version`, `--file-flush-interval-msec`, `--disable-extensions`, `--allow-unknown-fields` and `--reject-unknown-dynamic-fields` for config strictness.

```
envoy --mode validate -c /etc/envoy/envoy.yaml
envoy -c /etc/envoy/envoy.yaml --concurrency 4 --service-cluster edge --service-node edge-1 \
  --component-log-level upstream:debug,http:info
```
Gotchas: two Envoys on one host need distinct `--base-id` values or the shared-memory region collides; `--mode validate` generates no network traffic and skips hot restart, so it does not disturb other Envoy processes on the machine. Verify by checking the exit status of validate in CI.

## Checked

2026-11-03. Confirmed against: operations/cli.rst (flags, --mode serve|validate behaviour, --concurrency default, --base-id). Removed or corrected: the init_only mode, the 'matching hardware threads' recommendation and the claim that validate checks reachability.

Method: documentation only; no commands were run.
