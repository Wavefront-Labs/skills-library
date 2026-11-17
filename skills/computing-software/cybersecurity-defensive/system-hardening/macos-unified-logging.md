---
id: computing-software.cybersecurity-defensive.system-hardening.macos-unified-logging
name: macos-unified-logging
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [macos-unified-logging, macos, log-show, endpoint-security-framework, sysdiagnose, audit-logging]
level: practitioner
status: draft
description: "Use macOS unified logging for security: log show and log stream predicates, persisting and collecting logs, security-relevant subsystems, private data, and shipping to a SIEM."
sources: ["https://developer.apple.com/documentation/os/logging", "https://support.apple.com/guide/deployment/welcome/web", "https://developer.apple.com/documentation/endpointsecurity", "https://github.com/usnistgov/macos_security"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS unified logging

Since macOS 10.12 most system logging goes to the unified logging system: binary `tracev3` stores under
`/var/db/diagnostics` and `/var/db/uuidtext`, queried with the `log` command. Classic BSM audit (`praudit`,
`/var/audit`) is deprecated (disabled by default since macOS 14); security tooling now uses the Endpoint
Security framework.

## Querying
```bash
log show --last 1h --predicate 'subsystem == "com.apple.securityd"' --info
log show --start "2026-10-18 09:00:00" --end "2026-10-18 10:00:00" --predicate 'process == "sshd"' --style syslog
log stream --predicate 'eventMessage CONTAINS[c] "authentication"' --level info
log show --predicate 'process == "sudo"' --last 1d        # sudo usage
log collect --last 1d --output /tmp/host.logarchive        # export for offline analysis
log show /tmp/host.logarchive --predicate '...'
```
Predicate fields: `process`, `subsystem`, `category`, `eventMessage`, `messageType` (default, info, debug,
error, fault), `senderImagePath`.

## Security-relevant sources
- Authentication and authorisation: `com.apple.Authorization`, `com.apple.opendirectoryd`, `loginwindow`,
  `sshd`, `sudo`, `com.apple.LocalAuthentication` (Touch ID).
- Gatekeeper / XProtect / notarisation: `com.apple.syspolicy` (`syspolicyd`), `XProtect`.
- TCC privacy permission changes: `com.apple.TCC` (tccd).
- Configuration profiles: `com.apple.ManagedClient`, `mdmclient`.
- Screen sharing / remote login: `screensharingd`, `com.apple.remotedesktop`.
- Firewall: `socketfilterfw`.

## Retention and private data
- Default retention is short and size-based (days to weeks); info/debug levels are not persisted unless
  configured. Configuration profiles (`com.apple.system.logging`) can enable persistence of specific
  subsystems/levels.
- Many dynamic values show as `<private>`; Apple's logging configuration profile can enable private data
  (`Enable-Private-Data`) for troubleshooting; this exposes sensitive data, so avoid fleet-wide.

## Shipping to a SIEM
- EDR/agents using the Endpoint Security framework (process exec, file events, authentication events) are the
  primary security telemetry on macOS.
- For unified log content: agents that stream predicates (Elastic Agent / Filebeat macOS unified logs input,
  osquery `unified_log` table, Jamf Protect, Splunk UF scripted `log stream` inputs) with tight predicates to
  control volume.
- macOS Security Compliance Project (mSCP) baselines include audit/logging settings and checks.

## Verify
A test `sudo` command and an SSH login appear in the SIEM within minutes via the configured predicates;
`log show` on a test Mac returns authentication events for the past week at the configured retention.
