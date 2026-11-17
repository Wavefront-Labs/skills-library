---
id: computing-software.cybersecurity-defensive.security-operations.elastic-rule-exceptions-and-value-lists
name: elastic-rule-exceptions-and-value-lists
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, rule-exceptions, value-lists, shared-exception-lists, endpoint-exceptions, detection-tuning, false-positives]
level: practitioner
status: docs-checked
description: "Tune Elastic Security detection rules with exceptions: rule vs shared exception lists, value lists for big allowlists, endpoint exceptions, and avoiding over-broad suppression."
sources: ["https://www.elastic.co/guide/en/security/current/detections-ui-exceptions.html", "https://www.elastic.co/guide/en/security/current/value-lists-exceptions.html", "https://www.elastic.co/guide/en/security/current/shared-exception-lists.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic rule exceptions and value lists

## Kinds
- **Rule exceptions**: attached to one rule. Conditions on fields (`is`, `is not`, `is one of`,
  `exists`, `matches` wildcard, `is in list`), combined with AND/OR.
- **Shared exception lists**: one list referenced by many rules (Rules > Shared exception lists).
  Good for "our vulnerability scanners" or "IT admin jump hosts".
- **Endpoint exceptions**: apply to Elastic Defend's own protections (malware, behaviour) and to
  the Endpoint Security rule; they stop prevention on the host, so treat them as policy changes.
- **Value lists**: uploaded lists (keyword, IP, IP range, text) used with `is in list` / `is not in list`
  for large sets (thousands of hashes or IPs) without bloating the exception.

## Add an exception from an alert
Alerts table > row actions > Add rule exception: fields pre-populate from the alert. Delete the
noisy ones and keep only the minimum that identifies the benign pattern, e.g.:
```
process.executable : "<PROGRAM_FILES>\\Backup\\agent.exe"   (use the real full path)
AND process.code_signature.subject_name : "Backup Vendor Inc"
AND process.code_signature.trusted : true
```
Tick "Close all alerts that match this exception" to bulk-close existing matching alerts.

## Value lists
Rules > Manage value lists > upload a `.txt`/`.csv` with one value per line, choosing type.
Reference in an exception with `is in list`. Update by re-uploading (same name replaces).
Value lists are also usable in indicator match rules.

## Good exception design
- Anchor on stable, hard-to-spoof fields: code signature subject + trusted, full executable path,
  parent process, user. Avoid `process.name` alone (attackers rename binaries).
- Prefer narrowing the rule query itself when the exclusion is universal (versioned with the rule
  in detection-as-code); use exceptions for environment-specific noise.
- Add a comment (exceptions have a comments field) with ticket and owner, and optionally set an expiration date
  when creating the exception.

## Gotchas
- Exceptions are evaluated after the query; they do not reduce search cost.
- `matches` wildcards on Windows paths need escaped backslashes and are case-sensitive unless
  the field is a case-insensitive type.
- Exceptions on prebuilt rules survive rule updates; edits to the rule query itself do not.
- Indicator match and ML rules support exceptions with some limits; check per rule type.

## Checked
2026-10-28. Confirmed in the Elastic shared exception lists and value lists pages: `is in list` / `is not in list` operators, optional expiration date and comment on an exception, "Close all alerts that match this exception". Removed: the 8.x version gate.
Method: documentation only; no commands were run.

## Verify
Rule details > Exceptions tab lists the item; run "Preview rule" over the last 24h and confirm the
benign alerts drop while a test true positive still fires.
