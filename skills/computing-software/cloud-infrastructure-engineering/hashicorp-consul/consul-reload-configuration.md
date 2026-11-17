---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-reload-configuration
name: consul-reload-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-reload, sighup, reloadable-config]
level: practitioner
status: docs-checked
description: "Apply reloadable Consul config changes with consul reload or SIGHUP, check logs for errors, and know which settings are reloadable."
sources: ["https://developer.hashicorp.com/consul/commands/reload", "https://developer.hashicorp.com/consul/commands/validate", "https://developer.hashicorp.com/consul/docs/fundamentals/agent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul reload` triggers a reload of the agent's configuration files, the same as `SIGHUP`. It does not wait for the reload to finish, and any error appears in the agent logs, not in the command output. It needs the `agent:write` ACL.

```sh
consul validate /etc/consul.d && consul reload
```

`consul validate FILE_OR_DIRECTORY...` tests that config files are valid, so run it before the reload.

Reloadable at runtime (per the agent page): ACL tokens, bootstrapped configuration entries, health check definitions, `discard_check_output`, HTTP client address, log level, metric `prefix_filter`, node metadata, some Raft options (`raft_snapshot_threshold`, `raft_snapshot_interval`, `raft_trailing_logs`), RPC rate limits, reporting, `http_max_conns_per_client`, service definitions, and TLS configuration.

Gotchas:
- Anything not on that list is not reloadable; restart the agent. Gossip settings are one example: `consul reload` and `SIGHUP` do not change gossip encryption configuration.
- TLS reload is limited to a configuration that is already TLS enabled; you cannot enable or disable TLS by reloading.
- Because errors only show in the agent log, read the log after each reload.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/reload, commands/validate, fundamentals/agent (reloadable list, TLS limit), secure/encryption/gossip/enable/existing (reload does not change gossip). Removed: the journalctl pipe, the specific claims that `bind_addr`, `data_dir`, `server` and ports need a restart, the claim that a failed reload keeps the old configuration, and the Verify step.
Method: documentation only; no commands were run.
