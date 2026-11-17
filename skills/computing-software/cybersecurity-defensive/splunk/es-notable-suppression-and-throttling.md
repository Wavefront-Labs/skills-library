---
id: computing-software.cybersecurity-defensive.splunk.es-notable-suppression-and-throttling
name: es-notable-suppression-and-throttling
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, notable-suppression, throttling, alert-fatigue, notable-events, eventtypes, detection-tuning]
level: practitioner
status: draft
description: "Cut Splunk ES notable noise correctly: correlation search throttling by fields and window, notable event suppressions with expiry, and auditing what was hidden."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Customizenotables", "https://docs.splunk.com/Documentation/ES/latest/Admin/Createsuppressions", "https://docs.splunk.com/Documentation/ES/latest/Admin/Configurecorrelationsearches"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Notable suppression and throttling in Splunk ES

Two different tools:
- **Throttling** (on the correlation search): stop creating duplicate notables for the same
  entity within a window. The underlying condition is still true; you just get one alert.
- **Suppression** (on notables): hide notables matching a filter, e.g. a known-benign scanner.
  They are still created and searchable (`suppression` eventtype), but not shown in Incident Review.

## Throttling
Correlation search editor > Throttling:
- Window duration: e.g. `86400` seconds.
- Fields to group by: `src,dest,signature`. One notable per unique combination per window.
- Under the hood: `alert.suppress=1`, `alert.suppress.period`, `alert.suppress.fields` in
  savedsearches.conf.
Choose group-by fields that represent "a new thing to investigate"; grouping only by `src`
hides a second, different attack from the same host.

## Suppression
Incident Review > select notable > Actions > Suppress similar notables, or
Configure > Incident Management > Notable Event Suppressions:
- Name `notable_suppression-<name>` (stored as an eventtype).
- Search: `source="Endpoint - Suspicious PowerShell - Rule" dest="vuln-scanner01"`.
- **Always set an expiration date**. Permanent suppressions are how real incidents get missed
  a year later.
- Record the reason and ticket in the description.

## Better than suppressing
If a pattern is always benign, fix the detection (exclusion lookup, `where NOT`), so the change
is versioned with the rule. Use suppressions for temporary noise (a pentest, a migration).

## Audit what is being hidden
```
`notable` | search eventtype=notable_suppression-*
| stats count by eventtype rule_name
```
Configure > Incident Management > Suppression Audit dashboard shows suppressed counts over time.
Review monthly; delete expired ones.

## Gotchas
- Suppression filters match notable fields, which come from the correlation search output; a
  rename in the rule breaks the suppression silently.
- Risk-based alerting: suppressing a risk-incident rule hides the aggregated notable, but risk
  events still accumulate. Tune at the risk rule level instead.
- Throttle state lives in the scheduler; changing group-by fields resets it.

## Verify
After adding a suppression, count notables that match it in the last 7 days and confirm none
were true positives (check their dispositions).
