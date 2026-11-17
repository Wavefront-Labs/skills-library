---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cyclonedx-dependencies-and-services
name: cyclonedx-dependencies-and-services
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cyclonedx-dependencies-and-services, cyclonedx-bom, cyclonedx dependencies, dependson, services, endpoints, data flow, trust boundary, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Express component dependencies via ref/dependsOn and declare services with endpoints and data flows."
sources:
  - https://cyclonedx.org/specification/overview/
  - https://github.com/CycloneDX/specification/blob/master/schema/bom-1.6.schema.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CycloneDX dependency graph and services

Goal: relationship graph and service inventory.

Dependencies: array of {ref: "<bom-ref>", dependsOn: ["<bom-ref>", ...]}, also provides (added in specVersion 1.6) for components or services that implement a specification or standard. Include entries with empty dependsOn for leaf nodes to state "no dependencies" versus unknown.
Services: name, version, endpoints (URLs), authenticated, x-trust-boundary, data (classification and flow), provider.

Method:
- Generate from the lock file (resolved tree) for accuracy.
- Mark non-runtime components (for example test-only) with the component scope: required, optional or excluded.
- Use services to describe external SaaS dependencies (a SaaSBOM).

Gotchas:
- Missing leaf entries mean ambiguous completeness.
- Don't expose internal endpoints in BOMs shared externally.

Verify: graph is connected from metadata.component.

## Checked

2026-11-02. Checked against the CycloneDX 1.4 to 1.6 JSON schemas: dependency ref, dependsOn and provides (provides first appears in 1.6), the rule that components without dependencies must be declared as empty elements, service properties (provider, endpoints, authenticated, x-trust-boundary, data), and component scope values. Fixed: provides was attributed to 1.5.

Method: documentation only; no commands were run.
