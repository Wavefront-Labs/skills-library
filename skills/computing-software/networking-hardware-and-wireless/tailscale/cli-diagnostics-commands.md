---
id: computing-software.networking-hardware-and-wireless.tailscale.cli-diagnostics-commands
name: cli-diagnostics-commands
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-status, tailscale-ping, netcheck]
level: practitioner
status: docs-checked
description: "Use status, ping, netcheck and whois to find out why a path is slow or relayed."
sources: ["https://tailscale.com/kb/1080", "https://tailscale.com/kb/1338"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CLI diagnostics

Goal: debug connections and policy from the shell.

- `tailscale status` shows a table with each peer's address, name, user, OS and state, such as `active; direct <ip-port>`, `active; relay <relay-server>` or `idle`.
- `tailscale ping <hostname-or-ip>` pings only over Tailscale and reports connection details. Flags: `--c` (max pings, default 10), `--icmp`, `--peerapi`, `--size`, and `--tsmp`.
- `tailscale netcheck` reports physical network conditions: UDP, IPv4, IPv6, MappingVariesByDestIP and more.
- `tailscale whois ip[:port]` returns the machine and user for a Tailscale IP.

**Policy debugging with ping**

- `tailscale ping --tsmp` tests whether two devices can establish a connection but stops before the access control check.
- `tailscale ping --icmp` (or regular `ping`) tests end to end including access policies.
- If TSMP succeeds but ICMP fails, access policies are likely blocking the connection.

**Preview rules.** In Access controls, the Preview rules tab shows, for a selected user, accessible destinations, the defining rule line number, and other users with that access. Access control `tests` guard against accidental changes.

**Other commands:** `tailscale down` disconnects; `tailscale switch <account>` changes account (`--list` lists them); `tailscale file cp` and `file get` handle Taildrop.

**Checklist**

1. Check direct versus relay in `status`.
2. Compare TSMP and ICMP pings.
3. Run `netcheck` for NAT issues.

## Checked

2026-11-03. Read CLI reference (kb/1080) and Debug policies (kb/1338) and confirmed status, ping flags (`--c` default 10), netcheck, whois and the TSMP versus ICMP test. Nothing else was removed.

Method: documentation only; no commands were run.
