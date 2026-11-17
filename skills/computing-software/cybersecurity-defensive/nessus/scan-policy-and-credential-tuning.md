---
id: computing-software.cybersecurity-defensive.nessus.scan-policy-and-credential-tuning
name: scan-policy-and-credential-tuning
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, tenable, scan-policy, credentials, winrm, ssh, plugin-families, scan-windows, performance, safe-checks, denial-of-service-plugins, scan-templates, tenable-io, tenable-sc]
level: practitioner
status: draft
description: "Tune a Nessus scan policy for the target environment: plugin family selection, credential setup per OS, performance settings, and avoiding scan-caused outages."
sources: ["Tenable Docs - Nessus User Guide (Scan Templates, Credentials)", "Tenable Docs - Nessus Scanner Performance and Tuning", "Tenable Community - plugin family guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scan policy and credential tuning — scan the right things, safely, without an outage

**Goal:** build a Nessus scan policy that authenticates reliably across the mixed
estate (Windows, Linux, network gear), finds what matters for the target use case
(full vuln scan vs compliance vs discovery), and doesn't take down a fragile device
or saturate a WAN link.

## 1. Pick the template deliberately, don't default to "Basic Network Scan" everywhere
`Basic Network Scan` is a reasonable default for general IT. For a PCI/compliance
scope, use the compliance-specific template with the right audit file attached.
For OT/ICS or known-fragile devices (older printers, medical devices, industrial
controllers), use a **host discovery** or explicitly disable unsafe/intrusive
checks (`Safe Checks` on, disable the denial-of-service plugin family) — a default
network scan's crash-test plugins have taken down fragile embedded devices in real
environments; always check the device vendor's stance and your change-control
process before scanning anything safety- or availability-critical.

## 2. Credentials: do this per OS, and verify, don't assume
- **Windows:** a dedicated service account, local admin or domain account with
  appropriate rights, WinRM or SMB/WMI enabled and firewalled to allow the scanner
  only. Remote Registry and Server services must be running — a scan without them
  returns "authentication successful" but near-zero plugin coverage; always check
  the **plugin 19506 / "Nessus Scan Information"** output for "Credentialed checks:
  yes" and compare plugin count against an authenticated-scanning baseline (see
  companion skill authenticated-scanning).
- **Linux/Unix:** SSH key-based auth preferred over password; the account needs
  enough privilege to read target files (often via `sudo` with a scoped command
  list, not full root) — misconfigured sudo rules are the most common
  "authenticated but incomplete" failure on Linux.
- **Network devices:** SNMP read-only community/v3 creds plus device-specific
  (Cisco enable password, etc.) where supported — these give configuration-level
  findings a port scan alone cannot.
Store all credentials in Tenable's credential manager / a vault integration, never
inline in a policy exported to a file.

## 3. Plugin family selection
For a general vulnerability scan, enable all non-destructive families and leave
`Denial of Service` disabled by default (enable only in a controlled test window
against hosts explicitly cleared for it). For compliance-only scans, you often want
the audit/compliance plugin family alone (much faster, no vuln plugins) layered with
a separate vuln scan on its own schedule — combining both in one giant policy makes
troubleshooting a slow scan harder.

## 4. Performance settings to avoid self-inflicted outages
- `Max simultaneous checks per host` and `Max simultaneous hosts per scan`: lower
  these for scans over a WAN link or against environments with thin network
  headroom; the defaults are tuned for a healthy LAN.
- `Network timeout` too low on a high-latency link causes false "host down" or
  missed checks; raise it rather than concluding the host is unreachable.
- Scan windows: schedule heavy scans outside business-critical hours for anything
  shared with production traffic, and stagger large scope scans rather than firing
  the whole estate from one scanner at once.

## Gotchas
- "Credentialed checks: no" buried in the scan results is the single most common
  silent failure — a scan that reports zero critical vulns because it never
  actually got inside the host, not because the host is clean.
- Scanning through a NAT/load balancer can make every host look like it's coming
  from one source IP to the target, breaking per-host results; scan from inside the
  segment where possible.
- A scan policy copied between environments carries stale credentials and
  stale target lists — re-validate both per environment, don't just rename and reuse.
- Safe Checks off plus DoS plugins on is appropriate only in an explicitly
  cleared test environment with no production traffic.

## Verify
- [ ] Plugin 19506 output confirms "Credentialed checks: yes" for every target
      class (Windows, Linux, network).
- [ ] Plugin count per host is in line with the authenticated-scan baseline, not
      near zero.
- [ ] Denial of Service family is disabled unless explicitly cleared for the
      target and window.
- [ ] Performance settings were sized for the actual link (LAN vs WAN) before the
      first full run.
- [ ] Credentials live in a vault/credential manager, not inline in an exported policy.

Related: computing-software.cybersecurity-defensive.nessus.authenticated-scanning,
computing-software.cybersecurity-defensive.vulnerability-management.risk-based-prioritisation
