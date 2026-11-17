---
id: computing-software.cybersecurity-defensive.network-defence.ssh-tunnelling-control
name: ssh-tunnelling-control
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ssh-tunnelling, ssh-port-forwarding, allowtcpforwarding, reverse-tunnel-detection, egress-control, vpn-remote-access]
level: practitioner
status: docs-checked
description: "Control SSH tunnelling: disable or restrict forwarding in sshd_config, PermitOpen and per-key limits, egress blocking of outbound SSH, and detecting reverse tunnels."
sources: ["https://man.openbsd.org/sshd_config", "https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT", "https://attack.mitre.org/techniques/T1572/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH tunnelling control

SSH port forwarding turns any SSH access into a VPN (`-L`, `-R`, `-D` SOCKS) that bypasses firewalls -
used by attackers for C2 and pivoting (ATT&CK T1572 Protocol Tunneling).

## Server-side (sshd_config)
```
AllowTcpForwarding no          # or 'local' for bastions that need -L only
AllowStreamLocalForwarding no
GatewayPorts no
PermitTunnel no
X11Forwarding no
AllowAgentForwarding no
# Bastion exception for a group, limited destinations:
Match Group bastion-users
    AllowTcpForwarding local
    PermitOpen db01.internal:5432 app01.internal:443
```
Per key in `authorized_keys`: `restrict,port-forwarding,permitopen="db01:5432" ssh-ed25519 AAAA...`
(`restrict` disables port, agent and X11 forwarding, PTY allocation and `~/.ssh/rc`; `port-forwarding` re-enables forwarding and `permitopen` limits `-L` to literal host:port values, with no pattern matching or name lookup).

sshd_config values: `AllowTcpForwarding` and `AllowStreamLocalForwarding` accept `yes` or `all`, `no`, `local` (client-side `-L`) or `remote`. The man page warns that disabling forwarding does not improve security unless users are also denied shell access, as they can install their own forwarders.

`sshd -T | grep -i forward` shows the effective settings.

## Network-side
- Block outbound TCP 22 from servers and workstations to the internet except named jump hosts/Git hosts; SSH to arbitrary internet hosts is a strong exfil/C2 signal.
- Look at session duration and byte-count heuristics in your network sensors.

## Detection
- Long-lived outbound SSH sessions with steady small packets (interactive C2) or large asymmetric transfers.
- Process telemetry: `ssh` launched on servers with forwarding options (see ssh(1) for the option list).

## Gotchas
- Disabling forwarding does not stop a user with a shell running their own forwarding tools (socat, chisel); it removes the trivial path - combine with egress control.
- Git over SSH to GitHub needs outbound 22 for developers; allow to those destinations only (or use 443 / HTTPS).

## Verify
- [ ] `ssh -L 9999:internal:80 server` is refused by the server.
- [ ] Outbound SSH to an arbitrary internet host is blocked and logged.

## Checked
Checked 2026-11-09 against the OpenBSD sshd_config(5) man page (AllowTcpForwarding, AllowStreamLocalForwarding, AllowAgentForwarding, GatewayPorts, PermitTunnel, X11Forwarding, PermitOpen, Match), the sshd(8) AUTHORIZED_KEYS FILE FORMAT section (restrict, port-forwarding, permitopen) and MITRE ATT&CK T1572 (SSH tunneling named as a Protocol Tunneling method). Removed: the PAN-OS App-ID claim, plink and ssh option lists, the remote-listener remark, and the exact error string, none of which these pages confirm.
Method: docs-checked 2026-11-09 against the sshd_config man page, the sshd man page and ATT&CK T1572.
