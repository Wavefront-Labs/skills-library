---
id: computing-software.systems-network-administration.netbird.troubleshoot-relayed-connections
name: troubleshoot-relayed-connections
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, relayed-connections, symmetric-nat, hole-punching, stun-blocked]
level: practitioner
status: docs-checked
description: "Diagnose why NetBird peers use relay instead of P2P: confirm connection type, triage CGNAT and symmetric NAT, check STUN and firewalls, read ICE logs, rollout advice."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/help/troubleshooting-relayed-connections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Confirm: `netbird status -d` on each peer, field Connection type. `Relayed` with `ICE candidate (Local/Remote): -/-` is normal. If it is P2P but slow, the cause is path quality, MTU or load. Relay is the safety net after failed hole punching: more latency and shared bandwidth, still WireGuard end-to-end encrypted.

Triage: relay is expected with carrier CGNAT, cloud NAT gateways without public IPs, or strict enterprise firewalls with symmetric NAT. If only one side is affected keep troubleshooting; one predictable side is often enough.

Checks on both peers:
1. Outbound TCP/443 to the Management API and `signal.netbird.io`.
2. STUN: any `Unavailable` entry under `Relays:` in `netbird status -d` means that transport is blocked, usually egress UDP filtering. STUN uses UDP 80, 443, 3478, 5555.
3. Host firewalls: UFW, firewalld, Windows Firewall, endpoint security.

Debug logs: `srflx` candidates present but ICE cycling Checking to Failed means the direct path is blocked; no `srflx` means STUN or UDP is blocked. If all else checks out, suspect symmetric NAT: adjust NAT settings if you control it, else accept relay.

Avoid forwarding UDP ports to force P2P or opening inbound ports; fixes here are outbound rules or a `wt0` allowance.

Fleet rollout: allow outbound UDP to STUN and relay endpoints, permit `*.relay.netbird.io` on TCP/443, monitor `Relays:`, add `wt0` to firewall baselines, document sites that accept relay.

## Checked

2026-11-04. Confirmed against the NetBird troubleshooting relayed connections page: connection type check, relay as safety net, triage environments, control plane and STUN checks with ports, host firewalls, srflx and Checking to Failed log reading, symmetric NAT conclusion, outbound-only fixes, rollout checklist. Nothing removed.
Method: documentation only; no commands were run.
