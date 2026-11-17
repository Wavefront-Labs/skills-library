---
id: computing-software.systems-network-administration.netbird.troubleshoot-resource-access
name: troubleshoot-resource-access
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, resource-access, routing-peer-checks, route-table, access-control-check]
level: practitioner
status: docs-checked
description: "Step through a NetBird peer that is connected but cannot reach a network resource: test from the routing peer, forwarding, config, policy and client routes per OS."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/help/troubleshooting-client.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Symptom: the peer is Connected but a service behind a routing peer is unreachable.

1. Test from the routing peer itself: `curl -v "http://<resource-ip>"`, `nc -nvz -w 2 <resource-ip> 80`, or `ping --numeric --count=1 --timeout=2 <resource-ip>`.
2. Forwarding: `sysctl net.ipv4.ip_forward` should return `1`.
3. Network routing config: confirm resource address, routing peer group and distribution group.
4. Access control: a policy must allow the source group to the destination group on the needed protocol and port.
5. Client routes on the connecting peer:
- `netbird status -d` (Networks section) and `netbird networks ls`.
- Select missing ones: `netbird networks select <ID>` or `netbird networks select all`.
- Windows (admin PowerShell): `Get-NetRoute`.
- macOS: `netstat -nr`, look for a `utun` interface.
- Linux: `ip route` and `ip route show table 7120`.

Also verify packet handling with `netbird debug trace`, which simulates a packet through the firewall rules without sending real traffic.

## Checked

2026-11-04. Confirmed against the NetBird troubleshooting client page, section Debugging access to network resources: the test commands, `net.ipv4.ip_forward`, Networks and Routes configuration, access control policy, `netbird status -d`, `netbird networks ls` and select, Windows, macOS and Linux route checks including table 7120, `debug trace`. Removed the claim that a failing routing-peer test rules out NetBird policy, the ICMP policy reminder and the routing-peer-itself policy line, none of which the page states.
Method: documentation only; no commands were run.
