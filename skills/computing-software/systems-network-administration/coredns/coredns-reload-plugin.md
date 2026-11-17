---
id: computing-software.systems-network-administration.coredns.coredns-reload-plugin
name: coredns-reload-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, reload, corefile, sighup, configuration]
level: practitioner
status: docs-checked
description: "Automatically reload a changed Corefile by checksum polling, with interval and jitter defaults and limits."
sources:
  - https://coredns.io/plugins/reload/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply Corefile edits without sending SIGHUP or SIGUSR1.

Syntax: `reload [INTERVAL] [JITTER]`, both Go durations.

How it works:
- The plugin periodically reads the Corefile and computes its SHA512 checksum. If it changed, CoreDNS reloads with the new file.
- Reloads are graceful, so no loss of service is expected. If the new Corefile contains an error, CoreDNS keeps running the old configuration and prints an error to the log.
- Defaults: INTERVAL 30s, JITTER 15s. The minimum INTERVAL is 2s and the minimum JITTER is 1s. If JITTER is more than half of INTERVAL it is set to half. For example `reload 10s` gives an automatic jitter of 5s.
- Jitter spreads reloads across many instances that started together and share a Corefile, as in Kubernetes. It can be disabled by setting jitter to `0s`. It is recalculated on every reload.
- This plugin can only be used once per server block.

To reload zone file changes, use the auto plugin. Changes to imported files are detected from CoreDNS v1.7.0; v1.6.0 and earlier do not see them. Reload can fail partway: if a new listener (for example the health or prometheus port) cannot start, the old process keeps running but the closed listener stays broken, so be careful when changing ports.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/reload/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the claims about the file plugin reload option and the bind plugin (not on the reload page); added the page's import and port-change notes.

Method: documentation only; no commands were run.
