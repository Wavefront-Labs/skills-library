---
id: computing-software.digital-forensics-incident-response.incident-response-process.forensic-readiness-logging-baseline
name: forensic-readiness-logging-baseline
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [forensic-readiness, logging-baseline, log-retention, ir-preparation, audit-policy, dfir]
level: practitioner
status: docs-checked
description: "Define a forensic readiness logging baseline: which source categories to collect, how to prioritise them, and how to learn from incidents which logs or retention were missing."
sources: ["https://www.ncsc.gov.uk/collection/device-security-guidance/managing-deployed-devices/logging-and-protective-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forensic readiness logging baseline

**Goal:** when an incident happens, the logs that answer "how did they get in, what did they touch, what left" exist
and reach back far enough. This skill is grounded in the NCSC "Logging and protective monitoring" guidance
(version 2.1, reviewed 13 May 2025); it deliberately avoids event IDs, retention figures and regulatory numbers that
no fetched page confirmed. Check your own regulatory retention requirements (for example PCI DSS or national
government policy) at the source before fixing retention periods.

## Why
Many large-scale incidents target individual hosts, from which attackers move laterally using credential theft,
account impersonation, legitimate network tools or known exploits. In an incident, logging data helps identify the
source and the extent of compromise. Even in cloud-only or zero trust architectures, monitoring device activity,
health and configuration matters when deciding whether to permit access.

## Source categories (NCSC)
| Category | What it provides |
|---|---|
| Host-based logs | File system, running processes, program load events, website connections, device or service logons; built-in logs forwarded to a central store, or extra agents (which add management overhead and can add threat risk) |
| Service logs | Identity, mail, document storage and back-end services such as databases: authentication attempts and configuration changes |
| Infrastructure logs | Firewalls, proxies, intrusion detection or prevention: website connections and DNS requests |
| Device compliance | Device status and configuration against policy, for example whether the OS is up to date |
| Device attestation | Trusted measurements of device state that stay reliable if the device is compromised; support varies widely by device and MDM |

Successful intrusion detection very often needs multiple sources of information; combine on-device logging,
compliance reporting and attestation with network-layer devices (firewalls, proxies, VPN gateway) and service logs.

## Platform notes (NCSC)
- Windows: Windows Event Collection and Forwarding (configurable by group policy); Sysmon can add system activity to
  the event log; NCSC Logging Made Easy (LME) is an open source Sysmon-based end-to-end Windows logging project.
- Linux: syslog or rsyslog forwarded to a remote store; auditd for specific events of interest.
- macOS: logs viewable by a local administrator or via remote administration tools; collection can be automated with
  third-party software.
- iOS does not support remote or local historic event collection; MDM can report device state only.
- Android (corporately owned, device-owner mode): remote logging and bug reports, with limits (for example network
  activity logging can be bypassed).

## Method
1. Start from business need and risk (NCSC 10 Steps to Cyber Security) and decide which data sources you can and need
   to collect.
2. Log device events: user activity, network communications, authentication and access, to both devices and services,
   plus device state and compliance.
3. Collect and analyse centrally; automate detection and remediation where possible.
4. Prioritise: if constraints prevent a perfect solution, prioritise the questions you need to answer to spot
   compromise.
5. Evolve: feed incident lessons into the plan, for example a data type that was missing or log storage that was too
   short.
6. If a SOC is out of reach, at least have an effective logging system in place (LME is the NCSC example).

## Verify
Pick past or likely incident types and ask for each step which log would show it; test by generating the activity in
a lab and finding it in your central store.

## Checked
2026-11-08: confirmed against the NCSC Logging and protective monitoring page. Removed: Windows, domain controller,
PowerShell and cloud event IDs and settings, the retention periods, PCI DSS 10.5.1 and OMB M-21-31 figures, the claim
about dwell time, and the list of common gaps (default log sizes, VPN overwrite time), because the cited NIST SP
800-92 abstract page carried no such detail, the CISA page returned HTTP 403, and the NCSC page did not state them.
Method: documentation only; no commands were run.
