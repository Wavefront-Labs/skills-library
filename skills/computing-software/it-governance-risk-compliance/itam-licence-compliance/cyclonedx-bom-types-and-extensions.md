---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cyclonedx-bom-types-and-extensions
name: cyclonedx-bom-types-and-extensions
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cyclonedx-bom-types-and-extensions, cyclonedx-bom, hbom, mlbom, ml-bom, cbom, cryptography bom, obom, saasbom, formulation, lifecycles, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Use CycloneDX for hardware, machine-learning, cryptographic and operations BOMs, plus lifecycle and formulation."
sources:
  - https://cyclonedx.org/specification/overview/
  - https://github.com/CycloneDX/specification/blob/master/schema/bom-1.6.schema.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CycloneDX BOM types: HBOM, MLBOM, CBOM, OBOM

Goal: choose the right BOM for the need.

- SBOM: software inventory.
- SaaSBOM: services and data flows.
- HBOM: hardware components (component types device, device-driver, firmware).
- ML BOM: machine-learning-model and data components, with model details in modelCard (1.5+).
- CBOM: cryptographic assets (algorithms, keys, certificates, protocols via cryptoProperties) from 1.6.
- OBOM: operational runtime environment (the operations lifecycle phase).
- metadata.lifecycles distinguishes design, pre-build, build, post-build, operations, discovery, decommission.
- Formulation (1.5+) records how a component was built.

Method: pick types from customer requirements; confirm properties against the spec version.

Gotchas:
- Supported fields vary by spec version.

Verify: schema validation for your chosen specVersion.

## Checked

2026-11-02. Checked against the CycloneDX overview page and the 1.4 to 1.6 JSON schemas: SaaSBOM and HBOM named on the overview, OBOM / HBOM / SaaSBOM in the bom type description, lifecycles phases (design, pre-build, build, post-build, operations, discovery, decommission) from 1.5, formulation from 1.5, modelCard from 1.5, cryptoProperties from 1.6. Removed: the tooling-maturity claim.

Method: documentation only; no commands were run.
