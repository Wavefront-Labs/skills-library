---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.watch-config-live-reload
name: watch-config-live-reload
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [watch-config, reload, configuration, restart-cost, persistence-directory]
level: advanced
status: docs-checked
description: "Decide when to use opa run --watch-config, what a reload costs (listeners, bundle redownload, buffered decisions) and when a config change is rejected or not applied."
sources:
  - https://www.openpolicyagent.org/docs/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply configuration changes without exiting the OPA process, only where nothing else can replace it. Server mode only.

```
opa run -s -c opa-config.yaml --watch-config
```

This is separate from `-w`/`--watch`: `--watch` reloads policy and data into the store in place, while `--watch-config` restarts the server and everything the configuration drives, keeping only the store.

When to use it: on Kubernetes prefer rolling the pods after a ConfigMap update. Use `--watch-config` for an embedded non-orchestrated host, a sidecar whose restart would take the application down, or development.


Cost of a reload:
- Listeners are re-bound: in-flight requests drain first, then there is a brief window where the port is not accepting connections.
- Bundles download again, unless `persistence_directory` is set, in which case the persisted copy activates first. Until first activation `/health?bundles` reports not ready.
- Buffered decisions are flushed when the decision log plugin has a `service`; decisions buffered for a console or plugin sink are lost.

When a change is not applied:
- invalid config (parse or schema failure, or a `bundles` entry naming a missing service) is rejected before teardown, logged, and the running config keeps serving
- a failed restart (such as a port that no longer binds) falls back to the previous config
- the file is not watched when discovery is enabled or the caller supplied a custom router

Check: introduce a typo in a service name referenced by `bundles` and confirm the error is logged while decisions keep being served.

## Checked

The flag, the reload cost items and the rejected or unapplied change cases were confirmed in the Reloading Configuration section of the Configuration page.

Method: docs-checked 2026-11-09 against the OPA docs configuration page (docs/docs/configuration.md in the OPA repository, the Reloading Configuration section read; persistence_directory entry located by search).
