---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-lifecycle
name: data-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, data-lifecycle, data-retention, records-management, legal-hold, retention-schedule, data-deletion]
level: practitioner
status: draft
description: "Design data lifecycle and retention across cloud stores: retention schedule by data class, tiering, deletion and legal hold, and proving deletion across backups and replicas."
sources: ["https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html", "https://gdpr-info.eu/art-5-gdpr/", "https://pubs.opengroup.org/togaf-standard/adm/chap05.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data lifecycle and retention design

## Lifecycle stages
Create/collect -> store -> use/share -> archive -> delete (or anonymise). Each stage needs an
owner, controls and a system that enforces it.

## Steps
1. **Retention schedule**: per record type, legal/regulatory minimum (tax, financial, health),
   business need, and maximum (GDPR storage limitation, Art. 5(1)(e)). Legal and records management
   sign off.
2. **Map to stores**: for each data entity, list every copy - primary DB, replicas, caches, data
   lake, search index, logs, backups, exports, SaaS.
3. **Enforce automatically**:
   - Object storage lifecycle rules (transition to cool/archive, expire after N days).
   - Database TTL (DynamoDB TTL, Cosmos DB TTL) or scheduled purge jobs with audit.
   - Log retention per log group/workspace table.
   - Backup retention aligned; immutable (WORM / Object Lock) only where the schedule requires.
4. **Legal hold**: mechanism to suspend deletion for specific records (S3 Object Lock legal hold,
   Azure immutable storage legal hold, eDiscovery holds) and process to lift it.
5. **Deletion requests** (data subject erasure): identify all copies via lineage/catalog; delete or
   anonymise; backups age out within the documented window (state this in the privacy notice);
   crypto-shredding where per-subject keys exist.
6. **Evidence**: deletion job logs, lifecycle policy exports, periodic sampling.

## Gotchas
- Compliance-mode Object Lock cannot be shortened even by root - set it deliberately.
- Analytics copies and logs are forgotten; they often hold the most personal data.
- Keeping everything "just in case" increases breach impact and storage cost.

## Verify
- [ ] Every data entity has a retention rule and enforcement mechanism.
- [ ] Sample shows expired data actually gone from each copy.
