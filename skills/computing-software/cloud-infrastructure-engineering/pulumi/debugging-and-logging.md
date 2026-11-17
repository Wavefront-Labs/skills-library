---
id: computing-software.cloud-infrastructure-engineering.pulumi.debugging-and-logging
name: debugging-and-logging
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, logtostderr, pulumi-debug, verbose-logging, pulumi-v9]
level: practitioner
status: docs-checked
description: "Debug Pulumi CLI runs with --logtostderr, --logflow, -v verbose levels, --debug, --diff and --tracing file output, and take care sharing logs."
sources:
  - https://www.pulumi.com/docs/iac/support/troubleshooting/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_up/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging and verbose logging

Global CLI flags (listed on every command page such as `pulumi up`):

| Flag | Meaning |
|---|---|
| `-v, --verbose int` | Enable verbose logging (for example `-v=3`); anything above 3 is very verbose |
| `--logtostderr` | Log to stderr instead of to files |
| `--logflow` | Flow log settings to child processes (like plugins) |
| `--tracing file:` | Emit tracing to the endpoint; use the `file:` scheme to write tracing data to a local file |
| `--otel-traces` | Export OpenTelemetry traces to an endpoint (`file://` for local JSON, `grpc://` or `https://`) |
| `--profiling` | Emit CPU and memory profiles and an execution trace to `[filename].[pid].{cpu,mem,trace}` |
| `-d, --debug` | (`up`) print detailed debugging output during resource operations |
| `--diff` | (`up`, `preview`, `refresh`) display the operation as a rich diff |

```bash
pulumi up --logtostderr --logflow -v=9 2> pulumi.log
pulumi up --tracing=file:./up.trace
```
The troubleshooting page groups the tools as automatic logging, CLI verbose logging, and program logging for diagnostics.

## Gotchas
- Very verbose output can include request details and configuration; review and redact secrets and tokens before attaching logs to an issue.
- `--logflow` is what passes log settings on to provider plugins.
- `--diff` is a lighter first look than verbose logging when asking why a resource changes.

## Checked
2026-11-03. Confirmed flag names and descriptions on the `pulumi up` CLI page and the troubleshooting landing page. Removed: `PULUMI_DEBUG_GRPC`, `PULUMI_DEBUG_COMMANDS`, `TF_LOG`, `pulumi logs --follow`, `pulumi about`, `pulumi.log.debug`, `OpenTracing` format claims, the hang advice and grep Verify, none on pages read.
Method: documentation only; no commands were run.
