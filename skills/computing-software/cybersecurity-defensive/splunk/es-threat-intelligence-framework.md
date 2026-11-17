---
id: computing-software.cybersecurity-defensive.splunk.es-threat-intelligence-framework
name: es-threat-intelligence-framework
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, es-threat-intelligence-framework, threat-intel, ioc-matching, taxii, threat-activity, intelligence-downloads]
level: advanced
status: draft
description: "Configure the Splunk ES threat intelligence framework: intel downloads, TAXII and file sources, collections, Threat Activity detection and pruning stale IOCs."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Addthreatintel", "https://docs.splunk.com/Documentation/ES/latest/Admin/Downloadthreatfeed", "https://docs.splunk.com/Documentation/ES/latest/User/ThreatIntelligenceAudit"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ES threat intelligence framework

**Goal:** load indicators into Splunk Enterprise Security so they match against events
automatically and produce Threat Activity notables you can trust.

## 1. Sources
Configure > Data Enrichment > Threat Intelligence Management (ES 7) or Intelligence
Downloads (older). Types:
- **TAXII 2.x** feeds (MISP, OpenCTI, vendor feeds): URL, collection, credentials, polling interval.
- **URL downloads** of CSV/STIX/OpenIOC files with a parser definition.
- **Local lookups/files** uploaded or written by searches.
- **Splunk Intelligence Management (TruSTAR)** enclaves in newer ES.
Each source gets a weight (1-100) used in scoring, and a retention (default 30 days for
some types). Set retention per type: IPs days to weeks, domains weeks, hashes much longer.

## 2. Collections
Indicators land in KV store collections by type: `ip_intel`, `file_intel`,
`http_intel`, `email_intel`, `certificate_intel`, `process_intel`, `registry_intel`,
`service_intel`, `user_intel`. Add your own via search:
```
| makeresults | eval domain="bad.example", description="IR-2026-114", threat_key="local_ir", weight=80
| table domain description threat_key weight
| outputlookup append=t local_domain_intel
```

## 3. Matching
The Threat Gen searches compare CIM data models (Network Traffic, Web, Email, Endpoint)
against the collections and write to the `threat_activity` index; the
"Threat Activity Detected" correlation search raises notables. Data that is not CIM mapped
never matches, which is the most common reason intel "does nothing".

## Tuning
- Allowlist: never ingest CDN, cloud-provider and sinkhole ranges as malicious IPs; filter
  them in the source parser or a suppression.
- Prune: indicators older than their useful life cause noise. Check age distribution:
  `| inputlookup ip_intel | eval age_d=(now()-time)/86400 | stats count by threat_key | ...`.
- Use the Threat Intelligence Audit dashboard to confirm downloads succeed.

## Gotchas
- Huge feeds (millions of IPs) bloat KV store and slow matching; import only feeds you have
  evaluated for hit quality.
- Defanged indicators (`hxxp`, `[.]`) must be refanged before ingest or they never match.

## Verify
Add a test indicator for a domain, browse to it from a test host, and confirm a
`threat_activity` event and notable within the matching search schedule.
