---
id: computing-software.systems-network-administration.netbird.client-troubleshooting
name: client-troubleshooting
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, client-troubleshooting, client-logs, foreground-debug, login-failures]
level: practitioner
status: docs-checked
description: "Troubleshoot a NetBird client: read status fields, collect debug bundles, locate and rotate logs, run foreground debug modes, fix login failures and Linux firewall fallback."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/help/troubleshooting-client.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start: `netbird status -d`, then `netbird debug bundle --anonymize --system-info` (`-A -S`; omit anonymize if tunnel detail is needed).

Status fields: Connection type (`P2P` or `Relayed`); ICE candidates (`host/host`, `srflx`, `-/-` normal when relayed); Last WireGuard handshake (about every 2 minutes; empty means none completed); Quantum resistance must match on both peers.

Logs: `/var/log/netbird/client.log` (macOS/Linux). Built-in rotation is on, limit `NB_LOG_MAX_SIZE_MB` (default 15). A logrotate config mentioning netbird disables built-in rotation; use `copytruncate`. macOS newsyslog needs `NB_LOG_DISABLE_ROTATION=true`.

Bundles: `netbird debug for 5m --system-info`; `netbird debug bundle --system-info --upload-bundle` returns an upload key (local ZIP kept); desktop Settings > Troubleshoot; or Run Remote Job > Debug Bundle from the dashboard (keys expire after 30 days).

Levels: `netbird debug log level debug` (reset on restart). Foreground: `sudo netbird service stop`, then `sudo netbird up -F`. Variants: `NB_WG_KERNEL_DISABLED=true`, `GRPC_GO_LOG_VERBOSITY_LEVEL=99 GRPC_GO_LOG_SEVERITY_LEVEL=info`, `PIONS_LOG_DEBUG=all NB_LOG_LEVEL=debug`. Packet sim: `netbird debug trace in 100.64.1.1 self -p tcp --dport 80`.

Login failures (`PermissionDenied`, "invalid user", "peer login has expired"): machine registered earlier to another user or key. Delete the peer in the dashboard, or `netbird service stop`, remove `/var/lib/netbird/default.json`, `netbird service start`.

Linux firewall fallback: missing modules (e.g. `xt_mark`) push filtering to userspace; try loading the module, `NB_SKIP_NFTABLES_CHECK` or `NB_USE_LEGACY_ROUTING`. `--disable-firewall` stops access-control enforcement here. Routing hosts need `net.ipv4.ip_forward=1` and `net.ipv6.conf.all.forwarding=1`.

## Checked

2026-11-04: read the client troubleshooting page in full. Confirmed the status fields, log location and rotation rules, debug bundle commands and upload behaviour, remote job path and 30 day key expiry, log level and foreground modes, environment variable variants, login failure cause and fix, and the Linux firewall fallback and forwarding settings. Nothing removed.

Method: documentation only; no commands were run.
