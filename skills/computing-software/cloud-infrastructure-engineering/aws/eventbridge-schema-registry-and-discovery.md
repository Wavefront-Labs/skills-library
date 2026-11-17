---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-schema-registry-and-discovery
name: eventbridge-schema-registry-and-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, schema-registry, schema-discovery, openapi-schema, jsonschema-draft4, code-bindings, event-contracts, schema-versioning, discovered-schemas, event-catalog, event-driven]
level: practitioner
status: docs-checked
description: "Use the EventBridge schema registry: enable discovery on a bus, curate and version schemas for custom events, generate code bindings, and catch producer drift."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema-registry.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema-code-bindings.html", "https://docs.aws.amazon.com/eventbridge/latest/schema-reference/what-is-eventbridge-schemas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge schema registry and discovery

**Goal:** every event on the bus has a documented shape consumers can code against, new
versions are visible when producers change payloads, and typed bindings exist in the
languages the team uses.

## 1. Registries
- The AWS event schema registry: built-in schemas for AWS service events.
- The discovered schema registry: populated by schema discovery on buses you enable it on.
- Custom registries: where curated, versioned contracts for your own events live.
```bash
aws schemas list-registries
aws schemas create-registry --registry-name orders-contracts
aws schemas create-schema --registry-name orders-contracts --schema-name com.example.orders@OrderPlaced \
  --type OpenApi3 --content file://OrderPlaced.openapi.json
```
Schema types are `OpenApi3` and `JSONSchemaDraft4`. Schema content is limited to 100,000
characters. A naming convention such as `<source>@<detail-type>` keeps lookup predictable.

## 2. Discovery
```bash
aws schemas create-discoverer --source-arn arn:aws:events:<REGION>:<ACCOUNT_ID>:event-bus/orders --cross-account
```
Discovery infers schemas from events on the bus into the discovered schema registry.
`--cross-account` (API `CrossAccount`) includes events published from other accounts.
When a bus uses an input transformer, discovery infers the original event, not the
transformed one sent to the target. Discovery has a cost on high-volume buses; check the
EventBridge pricing page before enabling it on production.
Inferred schemas are approximations: treat them as a starting point to copy into a custom
registry, not as the contract.

## 3. Versioning and contracts
- `update-schema` with new content creates a new version; remove old ones with
  `delete-schema-version`. Consumers pin a version in their bindings.
- Put the contract version in the event too (`detail.version`). Treat the registry as
  documentation and code generation rather than enforcement: validate in the producer
  before publishing, or in a Lambda guard.
- Tag schemas with owner/team; `list-schemas --registry-name ...` plus tags is the event catalog.
- Schema registry API calls mask some property values with asterisks (the `Content` of
  `CreateSchema` and `UpdateSchema`, the `Events`/`Content` of `GetDiscoveredSchema`, the
  `keywords` of `SearchSchemas`), so do not build applications that depend on those fields in
  CloudTrail records.

## 4. Code bindings
Bindings exist for Golang, Java, Python and TypeScript, for AWS service events, your own
schemas and discovered schemas. Generate them in the console (Schemas > schema > Download
code bindings), the Schema Registry API, or the AWS Toolkit for JetBrains / VS Code.
```bash
aws schemas put-code-binding --registry-name orders-contracts --schema-name com.example.orders@OrderPlaced --language <LANGUAGE>
aws schemas describe-code-binding --registry-name orders-contracts --schema-name com.example.orders@OrderPlaced --language <LANGUAGE>   # wait for Status CREATE_COMPLETE
aws schemas get-code-binding-source --registry-name orders-contracts --schema-name com.example.orders@OrderPlaced --language <LANGUAGE> out.zip
```
`<LANGUAGE>` is the binding language identifier from the API reference. `Status` is
`CREATE_IN_PROGRESS`, `CREATE_COMPLETE` or `CREATE_FAILED`; a `--schema-version` can be
given. Regenerate on each version in CI; commit generated code or publish as a package.

## 5. Discovering what is actually on the bus
`aws schemas search-schemas --registry-name <DISCOVERED_REGISTRY> --keywords Order` finds
schemas by keyword. `list-schema-versions` shows how often a producer's shape has changed;
a schema with many versions in a month is a producer with no contract discipline.

## Gotchas
- Discovered schemas for events with highly variable keys (maps keyed by IDs) explode into
  useless versions; restructure the event (`items: [{id, ...}]`).
- Many teams generate their own types from the JSON schema instead of using the bindings.

## Verify
- [ ] After enabling discovery and publishing three distinct custom events, `list-schemas --registry-name <DISCOVERED_REGISTRY>` shows three schemas.
- [ ] Publishing the same event with an extra field creates version 2 of its discovered schema.
- [ ] `get-code-binding-source` returns a zip whose generated class deserialises a real event sample without error.

## Checked
2026-10-31. Confirmed against the botocore `schemas` model (operations, `Type` enum, `CrossAccount`, content maximum, `PutCodeBinding`/`DescribeCodeBinding` parameters and `Status` values), and the EventBridge User Guide pages on schemas (OpenAPI 3 and JSONSchema Draft4, value masking, input transformer note), registries (the three default registries) and code bindings (languages, console path, IDE toolkits). Removed as unconfirmed: free-tier event counts, the built-in registry name `aws.events` and the discovered registry name (now placeholders), binding language identifiers with version suffixes, the 385-character schema name limit, the CloudFormation resource name, the numeric-string typing remark and the five-minute timing.
Method: documentation only; no commands were run.
