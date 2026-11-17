---
id: computing-software.systems-network-administration.netbird.cli-status-and-health
name: cli-status-and-health
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, netbird-status, health-check, json-output, peer-filtering]
level: practitioner
status: docs-checked
description: "Use netbird status for per-peer detail, table, JSON or YAML output, address-only output, filters, and live/ready/startup health probes with exit codes."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/bootstrap-via-config-file.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`netbird status` shows peer state. Flags:
- `-d, --detail`: per-peer details (public key, ICE candidates, relay address, handshake, networks).
- `-t, --table`: compact table, one row per peer (v0.82.0+); cannot be combined with `--detail`, `--json`, `--yaml`, `--ipv4` or `--ipv6`.
- `-j, --json` / `-y, --yaml`: machine-readable output.
- `-4` / `-6`: print only this peer's NetBird IPv4 or IPv6 address.
- `-C, --check`: health probe with value `live`, `ready` or `startup`; success prints nothing and exits 0, failure exits 1.
- `-S`, `-T`, `-I`, `-N`: filter detailed output by status (idle|connecting|connected), connection type (P2P|Relayed), IPs or peer names.
- `-A, --anonymize` (global flag): anonymize IPs and non-netbird.io domains in status output.

Probes:
- `live`: the daemon responds.
- `ready`: daemon status is Idle, Connecting or Connected; NeedsLogin, LoginFailed and SessionExpired fail it.
- `startup`: management and signal are connected and, if any NetBird relays are configured, at least one relay is available.

Scripting examples:
```
netbird status --check startup && echo registered
netbird status --json | jq '.management.connected'
netbird status -4
```

The `Lazy connection` line of the status output shows whether lazy connections are on for that peer.

## Checked

2026-11-04: read the CLI page (status section) and the bootstrap-via-config-file page (check and jq examples), plus the lazy-connection page for the status line. Confirmed flags, version gate, probe semantics and exit codes. Corrected the startup description, which omitted that a relay is only required when relays are configured.

Method: documentation only; no commands were run.
