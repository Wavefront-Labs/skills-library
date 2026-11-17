---
id: computing-software.systems-network-administration.backup-and-recovery.cloud-region-pairs-for-dr
name: cloud-region-pairs-for-dr
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [region-pair, alternate-sites, cloud-disaster-recovery, azure-paired-regions, aws-regions, multi-region]
level: practitioner
status: docs-checked
description: "Choose cloud DR regions: Azure region pairs and their platform behaviour, AWS and GCP region choice, data residency, service parity, quotas, and cross-region replication."
sources:
  - https://learn.microsoft.com/en-us/azure/reliability/regions-paired
  - https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html
  - https://cloud.google.com/architecture/dr-scenarios-planning-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud region pairs for DR

**Goal:** a secondary region that is independent, legally allowed, has the services you need, and has capacity when you fail over.

## Azure paired regions
- Microsoft pairs some regions (for example East US / West US, North Europe / West Europe, UK South / UK West), usually within the same geography. Pairs can be asymmetrical (for example Brazil South pairs with South Central US, which is outside its geography).
- Features tied to pairs: geo-redundant storage (GRS) can replicate to the pair; Azure Backup Cross Region Restore restores into the pair; Azure strives to stagger planned updates across a pair; in a geography-wide outage one region in each pair is prioritised for recovery.
- Many regions have no pair (the list shows Chile Central, Mexico Central, Austria East, Poland Central, Spain Central, Israel Central and others as N/A) and rely on availability zones. Many services support geo-replication between arbitrary regions, so check each service's reliability guide.
- Using a pair gives no automatic failover; Microsoft-managed GRS failover happens only in catastrophic situations, so keep your own DR plan.

## AWS and GCP
- Neither has built-in region pairs as Azure does; you choose the secondary region and the replication method per service. The AWS and Google Cloud DR guides are not readable from the documentation repositories used for this check, so read their current service-by-service replication options before designing.

## Choosing the region
1. **Residency/compliance**: stay in the same legal geography (EU, UK, AU) unless approved.
2. **Service parity**: check every service and SKU (GPU, instance families, managed DBs) exists in the target.
3. **Capacity**: reserve capacity for critical instance types where the provider offers it; in a regional event many customers fail to the same neighbour.
4. **Quotas**: raise compute, IP and service quotas in the DR region in advance.
5. **Latency and cost**: inter-region egress per GB; replication lag drives RPO.
6. **Control plane**: keep IaC, DNS and identity usable if the primary region is down.

## Gotchas
- Relying on a "global" service whose control plane lives in one region.
- Make sure the encryption keys needed to decrypt replicated data can be used from the DR region, or restores fail.

## Verify
A failover test that builds the stack from IaC in the DR region, restores data, switches DNS, and records RTO/RPO.

## Checked

Checked 2026-10-27 against Microsoft's "Azure region pairs and nonpaired regions" article (updated Oct 2026) and the Azure Backup Cross Region Restore documentation (MicrosoftDocs/azure-docs). Confirmed: the example pairs, asymmetrical pairs, GRS replicating to the pair, recovery prioritisation and staggered updates, the list of unpaired regions, the caution that pairing gives no automatic failover, and Cross Region Restore using the paired region. AWS and Google Cloud service-specific claims were removed because those guides are not readable from the repositories used for this check; the remaining AWS and Google Cloud lines are planning advice only.

Method: documentation only; no commands were run.
