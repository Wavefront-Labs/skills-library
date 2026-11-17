---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-threat-intelligence
name: sentinel-threat-intelligence
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-threat-intelligence, threatintelindicators, ti-map-rules, taxii-connector, upload-api, defender-threat-intelligence, iocs]
level: practitioner
status: docs-checked
description: "Get threat intel into Sentinel and use it: TAXII and upload API connectors, ThreatIntelIndicators tables, TI map analytics rules, indicator expiry and match tuning."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/understand-threat-intelligence", "https://learn.microsoft.com/en-us/azure/sentinel/connect-threat-intelligence-upload-api", "https://learn.microsoft.com/en-us/azure/sentinel/use-matching-analytics-to-detect-threats"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threat intelligence in Sentinel

## Getting indicators in
- **Threat Intelligence - TAXII** connector: TAXII 2.0/2.1 API root, collection ID, credentials,
  polling frequency. Good for ISAC feeds and MISP/OpenCTI TAXII servers.
- **Threat Intelligence Upload API** (STIX objects): for TIPs that push. Needs an Entra app
  registration with the role the upload API page specifies.
- **Microsoft Defender Threat Intelligence** connector: Microsoft-curated indicators.
- Manual: Threat intelligence blade > Add new, or import CSV/JSON files.

## Tables
Newer workspaces use `ThreatIntelIndicators` and `ThreatIntelObjects` (STIX-shaped); the older
`ThreatIntelligenceIndicator` table may still exist in your workspace. Check which your content queries, and
update custom rules accordingly.
```
ThreatIntelIndicators
| where IsActive == true and ValidUntil > now()
| summarize count() by SourceSystem
```

## Matching
- **Microsoft Defender Threat Intelligence Analytics** (built-in matching rule): matches MDTI
  indicators against CEF, DNS, Syslog and others automatically.
- **TI map rules** (Content hub "Threat Intelligence" solution): e.g. "TI map IP entity to
  SigninLogs". Enable those for tables you ingest.
- Custom: join active indicators to your table with a lookback; match on exact type
  (ipv4-addr, domain-name, url, file hash) and keep `ConfidenceScore` for triage.

## Hygiene
- Set expiry (`ValidUntil`) on import; indicators without expiry stay active forever and
  generate stale matches. Use the bulk tag/expire actions in the TI blade.
- Filter low-confidence feeds (low `Confidence`) out of alerting rules but keep them for hunting.
- Allowlist shared infrastructure (CDNs, cloud provider ranges, sinkholes) before matching.

## Gotchas
- Large feeds drive ingestion cost and rule runtime; prefer curated feeds over volume.
- Check each TI map rule's lookback window before expecting historical matches.
- Duplicate indicators from multiple sources create duplicate alerts; group by indicator.

## Checked
2026-10-28. Confirmed in the Sentinel threat intelligence pages: TAXII and Upload API connectors, Defender Threat Intelligence connector, `ThreatIntelIndicators` table. Removed: `Data.indicator_types`, the confidence cut-off figure, the specific TI map rule example, the 14-day lookback, the retirement claim for the legacy table and the specific role for the upload API.
Method: documentation only; no commands were run.

## Verify
Add a test indicator (a lab IP), generate a sign-in or DNS event from it, and confirm the TI map
rule raises an incident with the indicator details.
