---
id: computing-software.cybersecurity-defensive.security-operations.detection-tuning-and-allowlists
name: detection-tuning-and-allowlists
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, detection-tuning, allowlist-management, false-positives, suppression, alert-fatigue, exceptions]
level: practitioner
status: draft
description: "Tune noisy detections without blinding them: precise allowlist conditions, central exception lists with owners and expiry, suppression vs filters, and review cadence."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://www.elastic.co/guide/en/security/current/add-exceptions.html", "https://docs.splunk.com/Documentation/ES/latest/Admin/Customizenotables"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tuning and allowlist management

**Goal:** cut false positives while keeping the detection able to catch the same technique
when an attacker uses it.

## Diagnose the noise first
Group recent alerts by the fields that differ: `stats count by process_path, parent, user,
host` and find the few combinations causing most volume (usually 2-3 cause 80%).

## Precise allowlist conditions
Bad: `NOT process_name=powershell.exe` (blinds the rule).
Good: combine multiple attributes the attacker cannot easily reproduce:
- full path + signer + parent + command-line pattern + specific host group + service account.
```
NOT (process_path="C:\\Program Files\\Backup\\agent.exe" AND signer="Example Backup Ltd"
     AND user="svc_backup" AND dest_category="backup_server")
```
- Avoid allowlisting by file name only, by user only, or by whole subnets.
- Prefer hash or signer for executables that change rarely.

## Central exception store
Keep allowlists in data, not hardcoded queries: Splunk lookup/macro (`<rule>_filter`),
Sentinel watchlist, Elastic exception list. Each entry has:
`rule_id, condition fields, reason, ticket, owner, created, expires`.
Expired entries are reviewed (renewed or removed) by a scheduled check.

## Filters vs suppression
- **Filter/allowlist:** permanently known benign; event never alerts.
- **Suppression/throttle:** same alert for the same entity within N hours is collapsed; use
  for repeated identical alerts, not for benign behaviour.
- **Lower to risk score / hunting:** behaviour is too common to alert but meaningful in
  combination (risk-based alerting).

## Process
1. Analyst marks alert as FP with the reason in the case.
2. Detection engineer adds the exception via pull request (detection-as-code) with the
   backtest showing alerts removed and none of the true positives lost.
3. Monthly review: top noisy rules, exception counts per rule (a rule with 40 exceptions
   probably needs redesign), expiring entries.

## Gotchas
- Allowlisting the vulnerability scanner or admin jump host broadly creates a perfect
  hiding place; scope to the specific tool behaviour.
- Tuning by deleting the rule: if precision cannot be fixed, demote it, do not lose it silently.
- Exceptions added in the UI bypass review and get lost in redeploys.

## Verify
Rerun the detection over the period that produced the noise: the FP combinations are gone
and replayed true-positive samples still alert.
