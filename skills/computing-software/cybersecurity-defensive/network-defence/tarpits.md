---
id: computing-software.cybersecurity-defensive.network-defence.tarpits
name: tarpits
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [tarpit, labrea, endlessh, ssh-tarpit, smtp-tarpit, deception, attacker-slowdown]
level: practitioner
status: docs-checked
description: "Use tarpits to slow scanners and brute-forcers: the endlessh SSH tarpit, internal tarpits on unused space as detection, and the risks and monitoring value."
sources: ["https://github.com/skeeto/endlessh", "https://d3fend.mitre.org/tactic/d3f:Deceive/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tarpits

A tarpit accepts connections and responds extremely slowly, wasting attacker time and resources while
producing high-signal logs (nothing legitimate should talk to it).

## Types
| Tarpit | How | Use |
|---|---|---|
| endlessh (SSH) | Very slowly sends an endless, random SSH banner, one line per delay interval (10 s by default) | Internet-facing hosts where real SSH moved to another port |
| Other tarpits (LaBrea-style TCP, SMTP, HTTP) | Not covered here; check each project's own documentation | Unused internal address space, spam bots, web scanners |

## endlessh
The README describes it as a tarpit that keeps SSH clients locked up for hours or even days; the intended use
is to put your real SSH server on another port and let scanners get stuck in the tarpit. It is a
single-threaded C program using poll(), and the tarpit sits in the banner before any cryptographic exchange.
```
# /etc/endlessh/config  (the -f option sets and loads the config file)
Port 22
Delay 10000
MaxLineLength 32
MaxClients 4096
```
`Delay` is milliseconds between banner lines; `MaxLineLength` is the maximum banner line length (3-255,
default 32); the example config in the README sets `Port 2222`, so set `Port` explicitly. Move the real sshd
to another port and restrict it (VPN/bastion source only).

## Internal tarpit as detection
Run on unused IPs per VLAN; any connection is an alert (scanning, worm, misconfiguration). Feed to SIEM
with source host for immediate triage. MITRE D3FEND lists Decoy Environment (honeypot) and Decoy Object
techniques under its Deceive tactic.

## Gotchas
- Tarpits consume your sockets/file descriptors too; set client limits (`MaxClients`).
- Hiding the real service on a non-standard port is not security by itself - it reduces noise only.
- Do not tarpit on addresses partners or monitoring systems scan legitimately.

## Verify
- [ ] Connection to the tarpit appears in SIEM with source; scanner sessions observed hanging.

## Checked
Checked 2026-11-09 against the endlessh README (description, options -f and -l, example config values Port
2222, Delay 10000, MaxLineLength 32, MaxClients 4096) and the D3FEND Deceive tactic page. Removed: Postfix
parameter names and the LaBrea mechanics (the LaBrea page was a stub and the Postfix page failed to load, so
neither was read) and the HTTP path example.
Method: docs-checked 2026-11-09 against the endlessh README and the D3FEND Deceive tactic page.
