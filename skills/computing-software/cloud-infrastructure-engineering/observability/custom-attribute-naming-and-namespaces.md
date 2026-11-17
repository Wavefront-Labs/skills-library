---
id: computing-software.cloud-infrastructure-engineering.observability.custom-attribute-naming-and-namespaces
name: custom-attribute-naming-and-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [custom-attribute-naming, attribute-namespaces, semantic-conventions, otel-weaver, attribute-limits]
level: practitioner
status: docs-checked
description: "Name custom OTel attributes: namespacing rules, reserved prefixes, cardinality per signal, attribute limits, and defining a custom semantic-convention registry with Weaver."
sources: ["https://opentelemetry.io/docs/specs/semconv/general/naming/", "https://opentelemetry.io/docs/specs/otel/common/attribute-naming/", "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/", "https://opentelemetry.io/docs/specs/otel/metrics/sdk/", "https://github.com/open-telemetry/weaver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom attribute naming and namespaces

## Rules (from the OTel naming spec)
- Lowercase, components separated by `.`; multi-word components use `_`: `acme.order.line_count`.
- Use a namespace for your company/product: `acme.*` or reverse domain `com.acme.*`. Do not invent top-level names
  that may collide with future semconv (`order.id` might be standardised later with different meaning).
- Never use the `otel.*` prefix (reserved).
- Reuse existing semconv attributes when they fit instead of inventing `acme.*` duplicates.
- For metrics, leave units out of the name: the unit is set on the instrument.

## Cardinality
Keep unbounded values (IDs) off metric attributes. Resources are immutable by design (set once per provider).
Use a metrics SDK view with an `attribute_keys` allow-list to strip high-cardinality attributes from a metric stream.

## Limits
`OTEL_ATTRIBUTE_COUNT_LIMIT` (default 128), `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` (no limit by default),
per-signal `OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` (128) and `OTEL_SPAN_EVENT_COUNT_LIMIT` (128).

## Registry with Weaver
Define your conventions in YAML and generate constants/docs:
```yaml
groups:
  - id: registry.acme.order
    type: attribute_group
    brief: Order attributes
    attributes:
      - {id: acme.order.id, type: string, stability: development, brief: Order identifier, examples: [o-991]}
```
```bash
weaver registry check -r ./model
weaver registry generate -r ./model -t ./templates go ./gen
```
Weaver also has a live-check mode that validates runtime telemetry against a registry.

## Verify
Grep your codebase for ad-hoc attribute strings; centralise them as constants (generated) so typos cannot ship.

## Checked
Checked 2026-10-28 against the OTel specification and semantic-conventions pages (general naming, common attribute naming, SDK environment variables, metrics SDK) and the Weaver README.
- Confirmed: lowercase names, dot namespaces, reserved `otel.*` prefix, reverse-domain company prefix and the future name-clash warning, the three attribute-limit variables and their defaults (128, 128, 128, no limit), `attribute_keys` view allow-list, `weaver registry check` and `weaver registry generate`, Weaver live-check existence, immutable Resources.
- Removed: the namespace-and-leaf rule, the `_bytes` suffix advice, the per-signal cardinality table, the "dropped silently" claim and the `registry live-check` command form (README documents live-check only as a mode), the `feature_flag.key`/`enduser.*` examples.

Method: documentation only; no commands were run.
