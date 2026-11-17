---
id: computing-software.cybersecurity-defensive.system-hardening.pci-dss-fim-scope
name: pci-dss-fim-scope
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [pci-fim, pci-dss, file-integrity-monitoring, change-detection, cardholder-data-environment, compliance]
level: practitioner
status: draft
description: "Scope file integrity and change detection for PCI DSS v4: which systems and files, weekly comparison, alert response, log integrity, and payment page change detection."
sources: ["https://www.pcisecuritystandards.org/document_library/", "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCI DSS FIM scope

PCI DSS v4.0.x requires change-detection mechanisms in several places. Getting scope right avoids both audit
findings and drowning in noise.

## Requirements that need FIM-style controls
- **11.5.2**: a change-detection mechanism (e.g. file integrity monitoring) alerts personnel to unauthorised
  modification (changes, additions, deletions) of **critical files**, performs critical file comparisons
  **at least once weekly**, and alerts are responded to.
- **10.3.4**: file integrity monitoring or change detection on **audit logs** so existing log data cannot be
  changed without generating alerts.
- **11.6.1** (effective March 2025): change- and tamper-detection for **payment pages** as received by the
  consumer browser (HTTP headers and script content), evaluated at least weekly or per targeted risk analysis.
- **12.10.5**: incident response plan includes monitoring and responding to alerts from change-detection
  mechanisms.

## Which systems
All system components in the cardholder data environment (CDE) and connected-to / security-impacting systems
in scope: servers processing or storing card data, payment application servers, web servers serving payment
pages, jump hosts, domain controllers and authentication servers for the CDE, log servers, security tools.

## Which files ("critical files")
The entity defines them; typical list:
- OS binaries and libraries (`/bin`, `/sbin`, `/usr/bin`, `/usr/lib`, Windows `System32`).
- Boot and kernel files, startup configs (systemd units, services, Run keys on Windows via registry FIM).
- Security configuration: `/etc/passwd`, `shadow`, `sudoers`, `ssh/sshd_config`, PAM, firewall rules, audit
  configuration, Windows security policy.
- Payment application binaries, configuration and web content (JS served on payment pages).
- Log files and log configuration (10.3.4).
Exclude volatile data (temp, caches, data files that change by design) and document why.

## Operation
- Tools: Wazuh syscheck, OSSEC, AIDE, Tripwire, osquery, EDR/agent FIM features, commercial FIM (Tripwire
  Enterprise, Qualys FIM).
- Real-time or at least weekly comparison; alerts into the SIEM with an owner; correlate with change tickets so
  approved changes are closed quickly and unapproved ones become incidents.
- Payment pages: script inventory + integrity monitoring (CSP reporting, commercial client-side monitoring,
  synthetic crawlers hashing scripts).

## Evidence for assessors
Critical file list with rationale, tool configuration per system class, sample alerts with response records,
proof of weekly comparison (schedules, reports), and change-ticket correlation.

## Verify
Every in-scope system appears in the FIM console with the right policy, a test modification of a critical file
generates an alert that is triaged per the IR procedure, and log files have FIM or immutable storage.
