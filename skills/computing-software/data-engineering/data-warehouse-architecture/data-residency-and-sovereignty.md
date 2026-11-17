---
id: computing-software.data-engineering.data-warehouse-architecture.data-residency-and-sovereignty
name: data-residency-and-sovereignty
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-residency, data-sovereignty, region-pinning, cross-border-transfers, multi-region, gdpr]
level: advanced
status: docs-checked
description: "Design data platforms for residency requirements: region-pinned storage and compute, controlling replication, sharing and support access, regional splits and transfer mechanisms."
sources:
  - https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection_en
  - https://docs.snowflake.com/en/user-guide/intro-regions
  - https://cloud.google.com/assured-workloads/docs/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data residency and sovereignty

**Goal:** data that must stay in a jurisdiction (EU, country-specific, public sector) stays there, including copies, backups, logs and processing, and you can prove it.

## Clarify the requirement
- **Residency:** where data is stored (and sometimes processed).
- **Sovereignty:** which laws can compel access, who operates the service, who controls keys and support access.
- **Transfer rules:** for personal data leaving the EU, the European Commission's data protection pages list adequacy decisions, Standard Contractual Clauses and Binding Corporate Rules as transfer tools; some sector or country laws forbid transfer entirely.
Get the exact scope from legal: which data classes, storage only or processing too, support access, metadata. This skill is engineering guidance, not legal advice.

## Platform controls
| Area | Control |
|---|---|
| Storage and compute | create resources in the required region. Snowflake: each account is hosted in a single region, and regions determine where data is stored and compute runs, so you need an account per region you use |
| Organisation policy | use your cloud's policy tooling to forbid other regions; Google Assured Workloads regional data boundaries enforce this with organization policy constraints, e.g. an EU Data Boundary package restricting resources to EU-only regions |
| Replication / DR | keep the DR region inside the same jurisdiction; govern cross-region replication and failover |
| Sharing | cross-region shares and listings may copy data across regions: restrict who can create them |
| Processing | keep ETL and other processing in-region (design guidance) |
| Logs and metadata | query text and logs can contain personal data: keep log sinks in-region (design guidance) |
| Keys | Assured Workloads offers key management controls by package: CMEKs, Cloud EKM, key import, and Sovereign Controls by Partners where a local partner manages keys, access justification and audits |
| Support access | Assured Workloads can limit which Google personnel support your data (by region and background checks, via Assured Support, which needs Enhanced or Premium Support) |

## Architecture patterns (practice guidance)
- **Regional silos:** one platform stack per jurisdiction; global reporting from aggregated or anonymised exports only.
- **Federated query:** global queries run regionally and return only aggregates.
- **Split by data class:** personal data stays regional; non-personal data centralised.

## Evidence
- Inventory of datasets with location; automated checks that resources are in allowed regions.
- Data flow diagrams with the transfer mechanism for each cross-border flow.

## Gotchas
- SaaS tools in the pipeline (ELT, observability, BI) may process data in their own regions; check each vendor.
- Some global managed services sit outside regional boundaries; document them.
- Caches and CDNs in front of data APIs can hold personal data outside the region.
- Snowflake U.S. government regions have extra requirements: compliance is supported only on Business Critical or higher, and cross-region listing access needs a disclaimer.

## Verify
- [ ] Policy-as-code blocks creating storage outside allowed regions (tested).
- [ ] Every cross-region data flow listed with legal basis and approval.

## Checked
Date: 2026-11-09. Confirmed from the Snowflake regions page (first part read: single-region accounts, US government region notes) and the Assured Workloads overview (read through key management). The European Commission page is a short index of topics (adequacy decisions, SCCs, BCRs) and does not state GDPR chapter or impact-assessment rules, so those were removed along with AWS SCP, Azure Policy, GCP resourceLocations and EU Data Boundary programme specifics. Rows marked design guidance are not page claims.
Method: documentation only; no commands were run.
