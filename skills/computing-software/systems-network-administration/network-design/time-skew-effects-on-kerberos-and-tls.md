---
id: computing-software.systems-network-administration.network-design.time-skew-effects-on-kerberos-and-tls
name: time-skew-effects-on-kerberos-and-tls
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-services-troubleshooting, time-skew, kerberos, tls-certificates, totp, ntp, log-correlation]
level: practitioner
status: draft
description: "Recognise faults caused by wrong clocks: Kerberos skew, TLS not-yet-valid certs, MFA codes, DNSSEC and log correlation, and how to find and fix the drifting host."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/windows-time-service/how-the-windows-time-service-works
  - https://www.rfc-editor.org/rfc/rfc4120#section-1.6
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time skew effects

Many "network" faults are clocks. Check time early when authentication or TLS fails selectively.

## Symptoms by service
| Service | Tolerance | Symptom |
|---|---|---|
| Kerberos (AD) | 5 minutes default | `KRB_AP_ERR_SKEW`, "The time difference between client and server is too great", domain logon or SMB access fails, falls back to NTLM if allowed |
| TLS | certificate validity window | `certificate is not yet valid` (clock behind) or `expired` (clock ahead); browsers show NET::ERR_CERT_DATE_INVALID |
| TOTP MFA | ~30-90 s | codes always rejected |
| DNSSEC validation | signature inception/expiry | SERVFAIL for signed zones on the resolver with the wrong clock |
| Cluster/DB replication | varies | split-brain detection, lease issues |
| Logs/SIEM | n/a | events out of order, correlation fails |

## Find the bad clock
```
w32tm /stripchart /computer:dc01.example.net /samples:5 /dataonly    # Windows offset to a DC
w32tm /query /status
chronyc tracking                                                     # Linux
timedatectl
show clock detail / show ntp status                                  # Cisco
```
Compare the failing host, the server and the DC/NTP source. In AD, the PDC emulator of the forest
root must sync to a reliable external source; everyone else follows the domain hierarchy
(`w32tm /query /source` should show a DC, not `Local CMOS Clock` or `VM IC Time Synchronization
Provider`).

## Common causes
- VM hypervisor time sync fighting NTP (disable one).
- Dead CMOS battery on appliances that boot without network time.
- NTP blocked by a new firewall rule (UDP 123).
- Wrong time zone rather than wrong time: UTC correct but displayed offset wrong (check UTC first).

## Fix
Re-point to the proper source, step the clock once if far off (`w32tm /resync /force`,
`chronyc makestep`), then let it slew. Restart services that cached failures (Kerberos tickets:
`klist purge`).

## Verify
- [ ] Offset under 1 s on the affected hosts and the failing authentication/TLS operation succeeds.
