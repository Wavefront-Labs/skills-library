---
id: computing-software.cybersecurity-defensive.system-hardening.listening-ports-audit
name: listening-ports-audit
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [listening-ports, ss, get-nettcpconnection, attack-surface, host-hardening, port-audit]
level: practitioner
status: docs-checked
description: "Audit listening ports: enumerate with ss and Get-NetTCPConnection, tie each socket to a process, classify bind addresses and compare with an external nmap view."
sources: ["https://man7.org/linux/man-pages/man8/ss.8.html", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-nettcpconnection", "https://learn.microsoft.com/en-us/powershell/module/nettcpip/get-netudpendpoint", "https://nmap.org/book/man-briefoptions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listening ports audit

**Goal:** know every listening socket, which process owns it, and that only intended ones are reachable from intended networks.

## Linux
```
ss -tulpnH                         # TCP and UDP, listening only, with processes, numeric, no header
ss -tlpn 'sport = :5432'           # filter by source port
```
Options per ss(8): `-t` TCP, `-u` UDP, `-l` listening sockets only, `-p` show processes, `-n` no name resolution, `-H` suppress the header. Classify each listener: loopback (`127.0.0.1`, `::1`), a specific internal address, or all interfaces (`0.0.0.0`, `[::]`, `*`).

## Windows
```powershell
Get-NetTCPConnection -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess | Sort-Object LocalPort
Get-NetUDPEndpoint | Select-Object LocalAddress,LocalPort,OwningProcess
```
`-State` accepts `Listen`; `OwningProcess` is the PID of the owning process. Map each PID to a process or service with your usual tools.

## Fix
- Bind local-only services to loopback in their own configuration (look up the setting in each product's documentation).
- Remove or disable the owning service if it is not needed.
- Use a host firewall with default-deny inbound and explicit allows as a second layer.

## External confirmation
From another network segment, scan the host and compare with the host's own view. nmap options (Nmap Reference Guide): `-sS` TCP SYN scan, `-sU` UDP scan, `--open` show only open (or possibly open) ports, `-p1-65535` all TCP ports, `--top-ports <number>` the most common ports. Only scan hosts you are authorised to test. Differences between the two views indicate firewalls or NAT you should understand.

## Ongoing
Collect listeners centrally per host role and alert on new ports.

## Verify
- [ ] Every listener mapped to an approved service in the role baseline.
- [ ] Datastores and admin interfaces not reachable from user networks or the internet.

## Checked
2026-11-01. Confirmed: ss options `-t -u -l -p -n -H` and the `sport = :PORT` filter (ss(8)); `Get-NetTCPConnection -State Listen` and OwningProcess, `Get-NetUDPEndpoint` properties (Microsoft Learn); nmap `-sS`, `-sU`, `--open`, `-p1-65535`, `--top-ports <number>` (Nmap brief options).
Removed: lsof, tasklist service mapping, per-product bind settings (Redis, PostgreSQL, MySQL), the Docker and UFW claim, osquery query, and nmap `-p-` and `-T4` (not described on the page read).
Method: documentation only; no commands were run.
