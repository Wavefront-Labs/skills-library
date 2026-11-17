---
id: computing-software.digital-forensics-incident-response.log-analysis.vpn-and-edge-appliance-log-analysis
name: vpn-and-edge-appliance-log-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [vpn-logs, edge-appliance, ivanti, fortigate, dfir]
level: advanced
status: draft
description: "Investigate VPN and edge appliance logs (FortiGate, Ivanti, Palo Alto GlobalProtect, Cisco ASA): session logs, exploitation signs, integrity tools and log gaps."
sources: ["https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-060b", "https://docs.fortinet.com/document/fortigate/7.4.0/fortios-log-message-reference", "https://docs.paloaltonetworks.com/globalprotect"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VPN and edge appliance logs

Edge devices are a top initial access vector and often lack EDR. Logs may live only on the device (small ring buffer) unless forwarded to syslog/SIEM.

## Collect first
- Export logs and config immediately (and run the vendor integrity checker) before rebooting or patching; many appliances keep logs in RAM.
- Pull from the SIEM/syslog for history beyond the on-box buffer.

## Normal session evidence
| Product | Useful logs |
|---|---|
| FortiGate SSL-VPN | `type=event subtype=vpn` `action=tunnel-up/ssl-login-fail`, `user`, `remip`, `tunnelip` |
| Palo Alto GlobalProtect | GlobalProtect logs: `portal-auth`, `gateway-connected`, client version, host ID, public/private IP |
| Cisco ASA / FTD | 113039 (AnyConnect session start), 722022/722023, 113005 (auth reject), 716001/716002 (WebVPN) |
| Ivanti Connect Secure | User Access log (login, roles), Events log, Admin Access log |

Hunt for: logins from new countries/ASNs/VPS providers, impossible travel, the same account from two IPs concurrently, unknown client versions/host IDs, success after spraying.

## Exploitation signs
- Ivanti: Integrity Checker Tool (ICT) failures, unexpected files in web dirs, `/api/v1/totp/user-backup-code` / `/api/v1/license/keys-status` exploit URIs in web logs (CVE-2023-46805/2024-21887).
- FortiOS: crash logs (`sslvpnd` crashes), unknown admin accounts, symlink persistence in language folders (2025 advisory).
- Palo Alto: GlobalProtect `SESSID` path traversal attempts, unexpected files in `/var/appweb/sslvpndocs/` (CVE-2024-3400).
- Any: config changes outside change windows, new local admins, logging disabled.

## Gotchas
- Devices log in local time with no timezone in some formats; record device clock offset.
- Assigned tunnel IP is what internal logs show: map tunnel IP to user and time to attribute internal activity.

## Verify
Each attacker VPN session is mapped from public IP to user to tunnel IP to internal activity on the timeline.
