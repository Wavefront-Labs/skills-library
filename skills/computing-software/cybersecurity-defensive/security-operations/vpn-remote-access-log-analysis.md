---
id: computing-software.cybersecurity-defensive.security-operations.vpn-remote-access-log-analysis
name: vpn-remote-access-log-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [vpn-log-analysis, investigation-data-sources, remote-access, globalprotect, fortinet, impossible-travel, credential-stuffing]
level: practitioner
status: draft
description: "Analyse VPN and remote access logs (GlobalProtect, AnyConnect, FortiGate, Ivanti, ZTNA) for credential abuse, impossible travel, session anomalies and appliance exploitation."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/use-syslog-for-monitoring/syslog-field-descriptions/globalprotect-log-fields", "https://www.cisa.gov/news-events/cybersecurity-advisories", "https://docs.fortinet.com/document/fortigate/7.4.0/fortios-log-message-reference/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VPN and remote access log analysis

Edge VPN appliances are a top initial access vector (credential abuse and appliance exploits).

## Key fields
User, source public IP, assigned internal IP, client OS/version, hostname, auth method (MFA?),
gateway/portal, login/logout times, bytes, failure reasons. GlobalProtect logs (`log_subtype`
`gateway-auth`, `portal-auth`), AnyConnect syslog `%ASA-6-113039/722022`, FortiGate `subtype=vpn`
`action=tunnel-up/ssl-login-fail`, Ivanti `AUT24414` / `AUT22673`.

## Hunts
- **Password spraying / stuffing**: many users failing from one IP, or one user from many IPs;
  successful login following bursts of failures.
```spl
index=vpn action=failure | stats dc(user) as users count by src_ip | where users>10
```
- **Impossible travel / new country**: successive logins with geodistance/time too large;
  compare against the user's 90-day history.
- **Unusual client**: hostname not matching corporate naming, OS/version mismatch, missing HIP
  (host information profile) checks.
- **Concurrent sessions** for one user from different IPs.
- **Session to internal IP mapping**: join assigned IP to internal logs (DHCP-like) to see what the
  VPN session touched (RDP, SMB, AD queries).

## Appliance exploitation
Check vendor advisories (Ivanti Connect Secure, Fortinet, Citrix NetScaler, Palo Alto) for log
indicators: unexpected admin logins, config changes, crashes of web processes, new local users.
Run vendor integrity checkers (e.g. Ivanti ICT) and compare against CISA advisories.

## Gotchas
- CGNAT and mobile carriers make geolocation unreliable; rely on ASN and device data too.
- Logs from appliances often lack detail; forward to SIEM with debug-level auth logging enabled.
- Appliance compromise can include log tampering; preserve off-box logs.

## Verify
Every successful VPN session in the incident window mapped to user, device and internal activity;
spray sources blocked and affected accounts reset.
