---
id: computing-software.cybersecurity-defensive.security-operations.ecs-field-mapping
name: ecs-field-mapping
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, ecs-mapping, elastic-common-schema, ingest-pipelines, custom-logs, normalisation, field-mapping]
level: practitioner
status: docs-checked
description: "Map custom log sources to the Elastic Common Schema: categorisation fields, related.* pivot arrays, custom field namespaces, dissect ingest processing and pipeline simulation."
sources: ["https://www.elastic.co/guide/en/ecs/current/ecs-category-field-values-reference.html", "https://www.elastic.co/guide/en/ecs/current/ecs-event.html", "https://www.elastic.co/guide/en/ecs/current/ecs-related.html", "https://www.elastic.co/guide/en/ecs/current/ecs-custom-fields-in-ecs.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html", "https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-pipeline-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS field mapping for custom sources

**Goal:** a new log source follows ECS so that rules, dashboards and searches built on ECS fields work on it.

## 1. Map on paper first
Take real sample events and build a table: source field, ECS field, example. Look each field up in the ECS
field reference rather than guessing names.
- ECS has four categorisation fields under `event.*`: `event.kind`, `event.category`, `event.type`,
  `event.outcome`. They hold "what it is", independent of source. Use only the allowed values listed in the
  ECS categorisation reference; if nothing matches, leave the field empty rather than inventing a value.
- `event.action` is the specific action ("group-add", "process-started"), normally implementer-defined.
  `event.dataset` names which log an event source publishes (for example `apache.access`).
- `related.ip`, `related.user`, `related.hosts`, `related.hash` hold arrays of all values seen on the event, so
  one query finds an IP wherever it appeared (host, source, destination, client, server...).

## 2. Custom fields
ECS defines nothing about custom fields. Options from the ECS guide: the `labels` field for extra keyword
fields; or nest custom fields under a proper name (such as a product name) as Filebeat modules do, using
nesting and underscores like ECS. Capitalised names will not conflict with future ECS fields. Custom fields
carry a small risk of conflicting with future ECS fields.

## 3. Ingest pipeline
Use an Elasticsearch ingest pipeline; the `dissect` processor splits fixed-layout messages. Check the dissect
and other processor pages for options before writing the pipeline.

## 4. Test
Use the simulate pipeline API with sample documents before attaching the pipeline to an index or integration.

## Verify
Sample events show `event.*` categorisation populated with allowed values, `related.*` arrays populated, and
custom fields outside ECS namespaces.

## Checked
2026-11-01. Confirmed against ECS pages: categorisation fields, event, related, custom fields; and the
Elasticsearch dissect-processor and simulate-pipeline pages. Removed: the sample pipeline JSON, specific
`event.category` and `event.type` value lists, Elastic Agent Custom Logs and `@custom` pipeline hook,
index-template mapping advice, mapping-conflict and timezone gotchas, and the verification aggregation, none
of which were read on pages this batch.
Method: documentation only; no commands were run.
