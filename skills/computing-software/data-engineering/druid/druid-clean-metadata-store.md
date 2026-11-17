---
id: computing-software.data-engineering.druid.druid-clean-metadata-store
name: druid-clean-metadata-store
category: computing-software
field: data-engineering
product: druid
tags: [metadata-cleanup, duration-to-retain, audit-records, supervisor-records, high-churn]
level: practitioner
status: docs-checked
description: "Configure automated cleanup of leftover Druid metadata records for deleted datasources, supervisors, rules and compaction config."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/clean-metadata-store.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deleting entities in Druid can leave related records in the metadata store. With high datasource churn (scripts that create and delete many short-lived datasources or supervisors), leftovers can fill the store and slow API calls.

The metadata store holds segment, audit, supervisor, rule and compaction configuration records, datasource records created by supervisors, indexer task logs and indexing state records.

## Defaults

Druid automatically cleans up metadata older than 90 days for all of those except compaction configuration records and indexer task logs, where cleanup is disabled by default. The retention period is set per record type through its `durationToRetain` property where available. Some records need extra conditions before they are cleaned.

## When to turn it on

- You have many high-churn datasources (for example scripts creating and deleting supervisors regularly).
- The metadata database disk is filling up.
- Metadata API calls are slow or fail.
- If you must keep audit records for compliance and enable audit cleanup, export them to external storage periodically first.

## Dependencies and scheduling

- Properties go in `coordinator/runtime.properties` unless stated otherwise.
- A segment kill task must be configured before rule or compaction-configuration cleanup can work.
- Set `druid.coordinator.period.metadataStoreManagementPeriod` to the same or a shorter period than your most frequent cleanup job (for example `PT1H` if a job runs hourly).

## Per-entity settings

Pattern for audit, supervisor, rule and datasource records: `druid.coordinator.kill.<type>.on` (enable), `.period` (ISO 8601, default `P1D`), `.durationToRetain` (ISO 8601). Types: `audit`, `supervisor`, `rule`, `datasource`.

- Segment records and deep-storage segments: the kill task. It is the only item here that affects actual data in deep storage. Eligible when the datasource passes the Coordinator dynamic config `killDataSourceWhitelist` check and `durationToRetain` has passed. Example keys: `druid.coordinator.kill.on`, `.period`, `.durationToRetain`, `.bufferPeriod`, `.maxSegments`.
- Audit records: eligible once `durationToRetain` has passed since creation.
- Supervisor records: eligible when the supervisor is terminated and `durationToRetain` has passed.
- Rule records: eligible when all segments of the datasource have been killed and `durationToRetain` has passed.
- Datasource records created by supervisors: eligible when the supervisor is terminated or absent from `druid_supervisors` and `durationToRetain` has passed.
- Compaction configuration records: only `druid.coordinator.kill.compaction.on` and `.period` exist; there is no `durationToRetain`. Records for inactive datasources (no used or unused segments) are deleted at each cleanup cycle, after the kill task has removed all segments. Gotcha: if you create a compaction config before its datasource exists (initial ingestion still running), cleanup may remove it, so wait until the datasource exists. If the config is huge and the audit log size limit blocks deletion, see `druid.audit.manager.maxPayloadSizeBytes` and `druid.audit.manager.skipNullField`.
- Indexing state records (only created with automatic compaction supervisors): cleaned by the Overlord, so set in `overlord/runtime.properties`. Keys `druid.overlord.kill.indexingStates.on`, `.period`, `.durationToRetain` (default `P7D`), `.pendingDurationToRetain` (default `P7D`; keep it longer than your longest compaction task). Eligible when no used segment references the record's fingerprint, or when a record is pending.
- Indexer task logs: Overlord removes logs from deep storage and rows from `druid_tasks`. Keys `druid.indexer.logs.kill.enabled`, `.durationToRetain`, `.initialDelay`, `.delay` (durations in milliseconds, not ISO 8601).

## Disabling

In `coordinator/runtime.properties` set `druid.coordinator.kill.on`, `.audit.on`, `.supervisor.on`, `.rule.on` and `.datasource.on` to `false`; in `overlord/runtime.properties` set `druid.overlord.kill.indexingStates.on=false`.

## Worked example from the docs

Hundreds of datasources created and deleted per day, living one to two days: metadata store management every hour (`PT1H`), segment kill daily with `durationToRetain=P4D`, `bufferPeriod=P7D`, `maxSegments=1000`; audit retained `P30D`; supervisor, rule and datasource records `P4D`; compaction config cleanup on; indexing states `P4D`. Treat these as example values, not defaults.

## Checked

2026-11-08. Read the cited clean-metadata-store page in full. Rewrote the thin draft with the per-entity eligibility rules, property names, the defaults that are stated (90 days, `P1D` periods, `P7D` indexing state retention), and the compaction-config and task-log exceptions. Example values are labelled as examples.

Method: documentation only; no commands were run.
