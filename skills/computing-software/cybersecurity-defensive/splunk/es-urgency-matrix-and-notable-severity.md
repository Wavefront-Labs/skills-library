---
id: computing-software.cybersecurity-defensive.splunk.es-urgency-matrix-and-notable-severity
name: es-urgency-matrix-and-notable-severity
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, enterprise-security, urgency-matrix, notable-severity, asset-priority, identity-priority, alert-prioritisation]
level: practitioner
status: draft
description: "Tune Splunk ES notable urgency: how severity combines with asset/identity priority in the urgency matrix, how to edit urgency.csv, and how to keep urgency meaningful."
sources: ["https://docs.splunk.com/Documentation/ES/7.3.0/Admin/Formatnotables", "https://docs.splunk.com/Documentation/ES/7.3.0/User/Howurgencyisassigned", "https://docs.splunk.com/Documentation/ES/7.3.0/Admin/Addassetandidentitydata"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ES urgency matrix

Notable **urgency** = f(correlation search **severity**, asset/identity **priority**). Analysts sort on
urgency, so a bad matrix sends them to the wrong alerts.

## How it is computed
- Severity comes from the correlation search (`severity` field in the notable, set in the search's
  notable action or via `| eval severity=...`).
- Priority comes from the asset or identity lookup of the notable's `dest`/`src`/`user`
  (`priority` = unknown, low, medium, high, critical). The higher of matched asset and identity
  priority is used.
- The lookup `urgency.csv` (SA-ThreatIntelligence) maps priority x severity to urgency.
  Default: critical asset + high severity = critical; unknown priority + any severity drops a level.
- If the search sets `urgency` explicitly, that overrides the matrix.

## Tuning
1. Fix priority data first: crown-jewel servers, domain controllers and executives must be
   `critical`/`high` in asset/identity lists; everything else should not be `unknown`.
2. Keep correlation-search severity honest: severity reflects likelihood of real impact if true.
3. Edit urgency via Configure > Content > Lookups > Urgency levels (or `urgency.csv`). Common
   change: unknown priority should not downgrade critical-severity detections.
4. Recheck the distribution: `index=notable | stats count by urgency` should be pyramid-shaped;
   if more than ~10% are critical, the matrix is meaningless.

## Gotchas
- `unknown` priority arises when the asset lookup misses (DHCP clients, cloud IPs). Add CIDR or
  DNS-based asset entries; otherwise everything collapses to medium/low.
- Severity `informational` notables still count in urgency stats; filter them in queue views.
- RBA risk notables set their own severity from the risk score; align thresholds with urgency.

## Verify
Generate test notables for a critical asset and an unknown host with the same severity; confirm
urgency differs as intended. Review urgency distribution monthly against true-positive rates.
