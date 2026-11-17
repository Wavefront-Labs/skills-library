---
id: computing-software.cybersecurity-defensive.system-hardening.ntp-time-synchronisation
name: ntp-time-synchronisation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [audit-log-management, ntp-time-sync, chrony, w32time, nts, time-hierarchy, log-correlation]
level: practitioner
status: docs-checked
description: "Keep clocks accurate for logs and auth: design an NTP hierarchy, configure chrony with NTS and Windows w32time via the AD domain hierarchy, and monitor offset."
sources: ["https://github.com/mlichvar/chrony/blob/master/doc/chrony.conf.adoc", "https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/WindowsServerDocs/networking/windows-time-service/Windows-Time-Service-Tools-and-Settings.md", "https://github.com/MicrosoftDocs/windowsserverdocs/blob/main/WindowsServerDocs/networking/windows-time-service/How-the-Windows-Time-Service-Works.md", "https://www.rfc-editor.org/rfc/rfc8915"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time synchronisation (NTP)

**Goal:** every system's clock is close enough to UTC that logs correlate, Kerberos works and certificates validate; set the tolerance you need per system class.

## Hierarchy
External trusted sources (national labs, NTS-capable pools, GPS appliances) -> 2-4 internal NTP servers -> all hosts. Domain-joined Windows uses the AD hierarchy with the PDC emulator of the forest root syncing externally.

## Linux: chrony
`/etc/chrony.conf` on clients:
```
server ntp1.corp.example iburst
server ntp2.corp.example iburst
server ntp3.corp.example iburst
makestep 1.0 3
rtcsync
```
On internal servers with external sources and NTS:
```
server nts1.example.net iburst nts
server nts2.example.net iburst nts
allow 10.0.0.0/8
```
With `nts`, the host named in `server` is an NTS-KE server (RFC 8915; the key-establishment step uses TLS). Check: `chronyc tracking`, `chronyc sources -v`, `chronyc authdata` (NTS status).

## Windows
- PDC emulator (forest root): `w32tm /config /manualpeerlist:"ntp1.corp.example,0x8 ntp2.corp.example,0x8" /syncfromflags:manual /reliable:yes /update` then `net stop w32time && net start w32time`.
- Other DCs and members: `w32tm /config /syncfromflags:domhier /update` (default).
- Check: `w32tm /query /status`, `w32tm /stripchart /computer:ntp1.corp.example /samples:5`.

## Network devices
Point routers, switches and firewalls at the internal NTP servers with authentication where the platform supports it (vendor-specific; not covered here); set the timezone consistently.

## Monitoring
Alert when the offset exceeds the tolerance you chose for the system class or when sources are unreachable; compare event timestamps with ingest time in the SIEM.

## Verify
- [ ] Fleet offset dashboard within tolerance.
- [ ] Only internal NTP servers are allowed outbound UDP 123 at the firewall.

## Checked
Checked 2026-10-25 against the chrony.conf manual (`doc/chrony.conf.adoc`, mlichvar/chrony, last commit 2026-10-05), the Microsoft Learn Windows Time documents (Windows-Time-Service-Tools-and-Settings and How-the-Windows-Time-Service-Works in MicrosoftDocs/windowsserverdocs, last commit 2026-10-23) and RFC 8915 (NTS). Confirmed: chrony `server ... iburst nts`, `makestep`, `rtcsync`, `allow`, `chronyc authdata`; `w32tm /config /manualpeerlist /syncfromflags:manual /reliable:yes /update`, `/syncfromflags:domhier`, `/query /status`, `/stripchart /computer /samples`, `NtpServer` flags (0x8 Client, 0x2 UseAsFallbackOnly) and the PDC emulator and domain hierarchy behaviour. Removed unconfirmed: the Kerberos 5-minute figure, named public NTS servers, cloud provider time addresses, PDC role transfer and hypervisor time sync advice, router NTP commands, the Prometheus metric name and alert thresholds.

Method: documentation only; no commands were run.
