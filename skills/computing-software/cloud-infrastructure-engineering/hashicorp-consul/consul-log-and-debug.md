---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-log-and-debug
name: consul-log-and-debug
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-monitor, consul-debug, log-level]
level: practitioner
status: docs-checked
description: "Use consul monitor, log levels and consul debug to diagnose agent problems, and handle sensitive data in captures."
sources: ["https://developer.hashicorp.com/consul/commands/reload", "https://developer.hashicorp.com/consul/docs/agent/telemetry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with live logs, then escalate to a bundle.

```sh
consul monitor -log-level=debug
consul debug -duration=2m -interval=20s -capture=metrics -capture=logs -output=/var/tmp/consul-debug
```

`consul debug` records agent, host, members, metrics, logs and optional pprof data into an archive. `consul monitor` follows a running agent's logs and can show a more verbose level than the agent is configured with (trace, debug, info, warn, error; `-log-json` streams JSON).

Gotchas: with ACLs enabled `consul debug` needs an `operator:read` token. ACL tokens and private keys are sanitized, but other information about the environment is plain text in the archive, so review it before sharing. `-duration` must be longer than `-interval` and longer than 10 seconds (default 5 minutes); `-interval` must be longer than 5 seconds (default 30 seconds). The `pprof` target is only retrieved when `enable_debug` is true on the agent or ACLs are enabled and a token with `operator:read` is used.

Verify: the compressed archive is written under the `-output` path (the current directory by default).

## Checked

2026-11-03. Confirmed against the consul debug and consul monitor command pages (capture targets, flags and limits, operator:read, sanitization, pprof condition, monitor log levels and -log-json). Removed: the runtime config-reload claim, the disk-fill warning, the index.json check and the bundle retention advice, which the pages do not state.

Method: documentation only; no commands were run.
