---
id: computing-software.data-engineering.apache-kafka.deleting-schemas-and-subjects
name: deleting-schemas-and-subjects
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, schema-registry, schema-deletion, soft-delete, hard-delete, subject-cleanup, schema-id, registry-operations]
level: practitioner
status: docs-checked
description: "Soft- and hard-delete Schema Registry subjects and versions safely: what breaks consumers, the two-step permanent delete, and recovering from a bad registered version."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/schema-deletion-guidelines.html
  - https://docs.confluent.io/platform/current/schema-registry/develop/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting schemas and subjects

**Goal:** clean up test subjects or roll back a bad schema version without making existing records undeserializable.

## Soft vs hard delete
- **Soft delete:** the version is removed from the subject but the schema metadata and ID are retained (IDs are not reusable), so the schema **ID still resolves** and consumers of old records keep working. Reversible by listing with `?deleted=true` and re-registering the schema.
- **Hard delete (`?permanent=true`):** removes all metadata, including the schema ID. It is a two-step process: soft delete first, then delete with `?permanent=true`. Records in Kafka that carry that ID can then no longer be deserialized.

## Commands
```bash
# list versions
curl -s $SR/subjects/orders-value/versions
# soft-delete one version (e.g. a bad v7)
curl -s -X DELETE $SR/subjects/orders-value/versions/7
# soft-delete whole subject
curl -s -X DELETE $SR/subjects/test-orders-value
# then hard-delete
curl -s -X DELETE "$SR/subjects/test-orders-value?permanent=true"
curl -s -X DELETE "$SR/subjects/orders-value/versions/7?permanent=true"
# see soft-deleted items
curl -s "$SR/subjects?deleted=true"
curl -s "$SR/subjects/orders-value/versions?deleted=true"
```

## Rolling back a bad version
Producers already wrote records with v7's ID? Those records still need the schema: **soft-delete only**, never hard. Soft-deleting v7 makes v6 the latest version, so under BACKWARD compatibility the next schema need only be compatible with v6. To restore a wrongly hard-deleted schema, the docs describe re-registering it in IMPORT mode at its original ID (see the deletion guidelines page).

If nothing was produced with v7 (registered by CI by mistake), hard delete is fine.

## Clearing a blocking compatibility state
Instead of deleting, consider temporarily setting subject compatibility:
```bash
curl -s -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"compatibility":"NONE"}' $SR/config/orders-value
# register, then restore
curl -s -X DELETE $SR/config/orders-value    # revert to global default
```
Document why; NONE lets anything through.

## Gotchas
- Deleting a topic does not delete its subjects (and vice versa). Clean both.
- Deleting a subject (or its only version) also deletes the subject's compatibility settings.
- These APIs are mainly for development; use them in production only with great care.

## Verify
- [ ] Before hard delete: search for records with that schema ID (sample consume with schema ID logging) or confirm topic retention has expired them.
- [ ] After cleanup, `GET /subjects` matches the list of live topics' subjects.

## Checked
2026-11-01. Confirmed against the Confluent Schema Deletion Guidelines page and Schema Registry API reference: soft vs hard delete, the two-step `?permanent=true` flow, `?deleted=true` listing, ID retention, latest-version effect on compatibility, and subject compatibility removal on delete. Removed: cloud billing, `_schemas` storage, reference-blocking and `use.latest.version` claims, which were not confirmed.
Method: documentation only; no commands were run.
