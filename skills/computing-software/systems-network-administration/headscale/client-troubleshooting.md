---
id: computing-software.systems-network-administration.headscale.client-troubleshooting
name: client-troubleshooting
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, netcheck, derp-map, netmap, troubleshooting, tailscale-debug]
level: practitioner
status: docs-checked
description: "Tailscale client commands that diagnose Headscale problems: netcheck, status JSON, DNS status, daemon logs, netmap, DERP tests."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/debug.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/derp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client-side troubleshooting

Many of these show differences between Headscale and Tailscale SaaS.

```
tailscale netcheck
tailscale status --json
tailscale dns status --all
tailscale debug daemon-logs
tailscale debug netmap
tailscale debug derp-map
tailscale debug derp headscale
tailscale debug --help
```

- `netcheck`: check local network conditions.
- `status --json`: get the client status.
- `dns status --all`: get DNS status.
- `debug daemon-logs`: client logs.
- `debug netmap`: the client netmap.
- `debug derp-map` and `debug derp headscale`: display the DERP map and check connectivity with the embedded DERP (assumes the default region code).

## Server side

Pair with server logs at debug level (logging-config) and the debug endpoint (debug-endpoint). `headscale nodes list` shows whether Headscale sees the node online.

## Gotcha

Tailscale's own Troubleshooting guide covers common issues.

## Checked

2026-11-04. Confirmed against the Headscale debugging and DERP pages: every command listed, the remark about differences with Tailscale SaaS, and the derp commands. Removed unsourced explanations and a Windows reset remark.
Method: documentation only; no commands were run.
