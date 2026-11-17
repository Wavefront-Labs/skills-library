---
id: computing-software.cybersecurity-defensive.threat-intelligence.opencti-connectors
name: opencti-connectors
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [opencti-connectors, opencti, threat-intelligence-platform, stix, enrichment, feed-integration, docker]
level: practitioner
status: draft
description: "Deploy and manage OpenCTI connectors: external import (MITRE, CISA KEV, MISP, feeds), enrichment (VirusTotal, Shodan), stream and export connectors, and tuning them."
sources: ["https://docs.opencti.io/latest/deployment/connectors/", "https://github.com/OpenCTI-Platform/connectors", "https://filigran.notion.site/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# OpenCTI connectors

## Types
- **External import**: pull data into OpenCTI (MITRE ATT&CK, CISA KEV, AlienVault OTX, MISP feeds or
  instances, abuse.ch, CVE/NVD, vendor feeds, TAXII2).
- **Internal enrichment**: triggered on entities (VirusTotal, Shodan, AbuseIPDB, GreyNoise, IPinfo),
  manually or automatically by scope.
- **Internal import file**: parse uploaded documents (PDF/STIX/CSV) and extract entities.
- **Internal export file**: export to STIX, CSV, PDF reports.
- **Stream**: consume the live stream to push into other tools (Splunk, Elastic, Sentinel, Microsoft
  Defender indicators, firewall EDLs).

## Deploy (Docker)
Each connector is a container with env vars:
```yaml
connector-cisa-kev:
  image: opencti/connector-cisa-known-exploited-vulnerabilities:<version>
  environment:
    - OPENCTI_URL=http://opencti:8080
    - OPENCTI_TOKEN=<CONNECTOR_USER_TOKEN>
    - CONNECTOR_ID=<UUID>
    - CONNECTOR_SCOPE=cisa
    - CONNECTOR_LOG_LEVEL=info
    - CISA_CATALOG_URL=https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
    - CISA_INTERVAL=2
  restart: always
```
Match connector image version to the platform version. Use a dedicated user/token per connector with
the minimal "Connector" role; set `CONNECTOR_CONFIDENCE_LEVEL`/marking defaults.

## Operating
- Data > Ingestion > Connectors shows status, queue messages, last run; reset state to re-import.
- RabbitMQ queue depth reveals backlog; scale workers (`opencti/worker` replicas) for heavy imports.
- Enrichment auto-mode can burn API quotas; scope by entity type and confidence.

## Gotchas
- Big imports (full MITRE, large MISP instances) take hours and create millions of relationships; plan
  storage (Elasticsearch/OpenSearch) and start with limited date ranges.
- Duplicates from multiple feeds: rely on STIX ID determinism and confidence-based update rules.

## Verify
Connector shows "active" with recent run; a known KEV CVE appears with the expected labels; stream
connector delivers a new indicator to the target SIEM.
