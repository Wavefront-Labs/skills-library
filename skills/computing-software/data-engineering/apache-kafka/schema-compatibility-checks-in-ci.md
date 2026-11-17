---
id: computing-software.data-engineering.apache-kafka.schema-compatibility-checks-in-ci
name: schema-compatibility-checks-in-ci
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, schema-registry, schema-ci-checks, compatibility-check, schema-registry-maven-plugin, auto-register-schemas, use-latest-version, buf-breaking, avro, protobuf]
level: advanced
status: docs-checked
description: "Gate schema changes in CI: test compatibility against Schema Registry, register from the pipeline with auto.register.schemas=false, and buf breaking for Protobuf."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/develop/api.html#compatibility
  - https://docs.confluent.io/platform/current/schema-registry/develop/maven-plugin.html
  - https://buf.build/docs/breaking/
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema compatibility checks in CI

**Goal:** an incompatible schema change fails a pull request, not production consumers.

## Principle
- Schemas live in git next to the producer code (`schemas/order-placed.avsc`).
- CI checks the candidate against the registry's latest version under the subject's configured compatibility.
- Registration happens in the deploy pipeline, and producers run with `auto.register.schemas=false` + `use.latest.version=true` so a rogue build cannot register an incompatible schema at runtime.

## REST check (any CI)
```bash
SR=https://<REGISTRY>; SUBJECT=orders.checkout.order-placed.v1-value
jq -n --rawfile s schemas/order-placed.avsc '{schema: $s, schemaType: "AVRO"}' > payload.json
curl -s -u "$SR_KEY:$SR_SECRET" -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  -X POST "$SR/compatibility/subjects/$SUBJECT/versions/latest?verbose=true" -d @payload.json \
  | tee result.json
jq -e '.is_compatible == true' result.json      # non-zero exit fails the job; verbose lists reasons
```
For `*_TRANSITIVE` modes the registry checks against all versions automatically.

## Maven plugin (JVM projects)
```xml
<plugin>
  <groupId>io.confluent</groupId><artifactId>kafka-schema-registry-maven-plugin</artifactId>
  <configuration>
    <schemaRegistryUrls><param>${sr.url}</param></schemaRegistryUrls>
    <subjects><orders.checkout.order-placed.v1-value>src/main/avro/order-placed.avsc</orders.checkout.order-placed.v1-value></subjects>
  </configuration>
</plugin>
```
`mvn schema-registry:test-compatibility` in PR builds; `mvn schema-registry:register` in the release job.

## Protobuf: buf breaking
```bash
buf breaking --against '.git#branch=main'          # rule categories: FILE, PACKAGE, WIRE_JSON, WIRE
```
Run it in addition to the registry check; `WIRE_JSON` detects breakage to the binary wire format or JSON encoding, and a stricter category implies passing every looser one.

## Set compatibility explicitly per subject
```bash
curl -X PUT -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  -d '{"compatibility":"BACKWARD_TRANSITIVE"}' "$SR/config/$SUBJECT"
```
Choose by who upgrades first: consumers first -> BACKWARD; producers first -> FORWARD; independent -> FULL.

## Gotchas
- A subject that does not exist returns 404 ("Subject not found", error code 40401); treat a new subject as a pass but require review.
- Avro default values matter: adding a field without a default breaks BACKWARD.
- JSON Schema compatibility depends on open vs closed content models (`additionalProperties`); test real changes, the rules surprise people.

## Checked
2026-10-28. Confirmed on the Confluent Schema Registry API, Maven plugin and schema evolution pages and the Buf breaking-change docs: the compatibility endpoint and its 404 for a missing subject, `schema-registry:test-compatibility` and `schema-registry:register` goals, compatibility levels including the TRANSITIVE variants and BACKWARD as default, `buf breaking --against` and the FILE, PACKAGE, WIRE_JSON and WIRE categories, `auto.register.schemas` and `use.latest.version`. Removed: the specific claim about what buf catches.
Method: documentation only; no commands were run.

## Verify
- [ ] A PR removing a required field fails CI with the registry's incompatibility message.
- [ ] Producer config in production has `auto.register.schemas=false`.
- [ ] Subject-level compatibility is set (not relying on the global default).
