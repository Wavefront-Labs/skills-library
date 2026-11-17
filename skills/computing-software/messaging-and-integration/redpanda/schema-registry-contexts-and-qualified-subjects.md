---
id: computing-software.messaging-and-integration.redpanda.schema-registry-contexts-and-qualified-subjects
name: schema-registry-contexts-and-qualified-subjects
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [schema-registry, contexts, qualified-subjects, multi-team, confluent-migration, schema-ids]
level: advanced
status: docs-checked
description: "Use Schema Registry contexts as namespaces: qualified subject syntax, per-context IDs, config resolution order, enabling and limits."
sources:
  - https://docs.redpanda.com/streaming/current/manage/schema-reg/schema-reg-contexts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Contexts (Redpanda v26.1+) are namespaces inside one registry, each with its own schema ID counter, mode and compatibility settings, and compatible with the Confluent Contexts API. Use them for multi-team clusters or to migrate from Confluent without restructuring schemas.

**Terms.** Context names start with a dot (`.staging`). The default context is `.`, and `.__GLOBAL` is the lowest-priority fallback for mode and compatibility. A qualified subject is `:<context>:<subject>`, for example `:.staging:user-events-value`. `:.:x` equals bare `x`; `:.staging:` names the context itself for config and mode operations.

**Enable.** `schema_registry_enable_qualified_subjects` is on by default in v26.2 and later; earlier it defaults to false.

```bash
rpk cluster config set schema_registry_enable_qualified_subjects true
rpk cluster config get schema_registry_enable_qualified_subjects
```
It requires a restart of all brokers.

**Behaviour changes.**
- IDs are per context: ID 1 in `.staging` and `.production` are different schemas. `GET /schemas/ids/{id}` searches the default context unless you pass `?subject=:.staging:my-topic` or use a context URL prefix.
- Settings resolve Subject, then Context, then Global (`.:.__GLOBAL:`), then built-in defaults. A `.staging` context in IMPORT mode makes its subjects inherit it. Use `defaultToGlobal=true` on `GET /config` and `GET /mode` to see the effective value.
- `GET /subjects` without `subjectPrefix` returns subjects across all contexts, qualified.

**Limits.** Header-based schema ID validation does not support contexts (magic byte and prefix do). `referencedby` returns bare IDs. Contexts do not block cross-context references; unqualified references resolve in the root schema's context. The default context cannot be deleted. After enabling, existing subjects whose names match the qualified pattern change meaning. Principals need Schema Registry ACLs for the context.

## Checked

2026-11-08. Read the whole Schema Registry Contexts page. Confirmed: v26.1+ requirement, per-context ID counters, key terms, qualified subject forms, the property default in v26.2 and later, rpk set and get commands, broker restart, ID lookup scoping, resolution order with defaultToGlobal, GET /subjects behaviour, limitations (header-based validation, referencedby, cross-context references, default context deletion, upgrade reinterpretation), ACL need. Nothing removed.

Method: documentation only; no commands were run.
