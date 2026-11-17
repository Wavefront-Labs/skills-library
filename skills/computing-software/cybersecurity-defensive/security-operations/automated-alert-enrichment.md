---
id: computing-software.cybersecurity-defensive.security-operations.automated-alert-enrichment
name: automated-alert-enrichment
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soar, automated-enrichment, alert-enrichment, threat-intel-lookup, asset-context, identity-context, playbooks]
level: practitioner
status: draft
description: "Automate alert enrichment in SOAR or the SIEM: which context to fetch per entity type, caching and rate limits, summarising results into one readable case note."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/Playbook/Overview", "https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks", "https://docs.virustotal.com/reference/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated enrichment

**Goal:** every alert arrives with the context an analyst would otherwise spend 10 minutes
collecting, presented as one concise summary.

## What to fetch per entity
| Entity | Context |
|---|---|
| IP | internal or external; asset owner/zone (CMDB); geo/ASN; reputation (TI platform, VirusTotal, AbuseIPDB); recent firewall/proxy hits; known scanner/VPN egress |
| Domain/URL | age (WHOIS), category (proxy), reputation, first seen internally, URL scan screenshot |
| File hash | reputation and detection ratio, signer, prevalence in estate (EDR), first seen |
| User | department, manager, title, privileged group membership, account status, recent risky sign-ins, MFA methods |
| Host | owner, OS, criticality, EDR health, last patch date, open vulnerabilities |

## Implementation notes
- Internal context first (CMDB, IdP, EDR): free, fast, most decisive.
- External lookups cost quota; **cache** results (e.g. 24 h for hashes, 1-6 h for IPs) in a
  KV store or SOAR list; skip private and allowlisted IPs.
- Handle rate limits with queues/backoff; free-tier VirusTotal is 4 requests per minute.
- Do not submit internal files or URLs containing tokens to public services; use hash
  lookups only, or private sandboxes.

## Output
A single case note, newest context at top, e.g.:
```
Enrichment (auto, 2026-10-16 09:14 UTC)
User: j.doe, Finance analyst, not privileged, MFA: Authenticator push, 2 risky sign-ins (7d)
Src IP 203.0.113.50: external, AS14061 hosting, AbuseIPDB 87%, first seen internally today
Hash 3f2a...: 41/72 engines, unsigned, present on 1 host
Verdict hint: HIGH - external hosting IP + malicious hash + first seen
```
Also write structured fields back to the alert (custom details/tags) so queues can sort by them.

## Gotchas
- Too much raw output (full JSON dumps) is noise; summarise.
- Stale CMDB data misleads; show the record's last-updated date.
- Enrichment failures must be visible ("TI lookup failed: timeout") so analysts know what is missing.

## Verify
Sample 20 enriched alerts: every field populated or marked as failed, and analysts' triage
time drops compared with the pre-automation baseline.
