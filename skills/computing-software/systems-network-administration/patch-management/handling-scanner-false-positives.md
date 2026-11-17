---
id: computing-software.systems-network-administration.patch-management.handling-scanner-false-positives
name: handling-scanner-false-positives
category: computing-software
field: systems-network-administration
product: patch-management
tags: [scanner-false-positive, false-positive, vulnerability-scanning, patch-verification, patch-management]
level: practitioner
status: draft
description: "Prove and handle vulnerability scanner false positives: evidence standards, common sources (backports, leftover files, banners), vendor tickets and expiring suppressions."
sources:
  - https://access.redhat.com/security/updates/backporting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling scanner false positives

A false positive claim needs evidence; otherwise it is just an unremediated finding with a nicer label.

## Common real false positives
- **Backported fixes**: RHEL `httpd-2.4.57-5.el9` fixed via backport; scanner compares upstream 2.4.58. Evidence: RHSA/USN listing the CVE as fixed in that package version, `rpm -q --changelog`.
- **Leftover files**: old DLL/JAR in an uninstalled app folder or backup directory that is never loaded. Evidence: file path, no process loads it (`Get-Process | % Modules`, `lsof`), better still delete it.
- **Banner-based detection**: uncredentialed scan reads version string; proxy/load balancer banner, or vendor-patched build with same banner.
- **Detection plugin bugs**: confirmed by vendor ticket or plugin update notes.
- **Mitigation-only conditions**: config already disables the vulnerable feature, and the plugin cannot see it (this is a mitigated finding, not false positive; record as such).

## Process
1. Reproduce: read plugin output (path, version found, version expected).
2. Gather evidence on host; for backports, link the vendor advisory.
3. Peer review by security (not the system owner alone).
4. Suppress narrowly in the scanner: Tenable recast/accept rule, Qualys Ignore, scoped to plugin + asset (+ path if possible), with expiry (90-180 days) and comment linking evidence.
5. Raise vendor ticket for plugin bugs; remove suppression when fixed.

## Gotchas
- Never suppress plugin-wide across all assets for one host's evidence.
- Suppressions without expiry hide real future vulnerabilities on the same plugin.
- "Leftover file" often means the app still bundles it somewhere else; scan the whole filesystem.

## Verify
False-positive rate and count of active suppressions reported monthly; each suppression has evidence, reviewer and expiry.
