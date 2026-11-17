---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cyclonedx-components
name: cyclonedx-components
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cyclonedx-components, cyclonedx-bom, cyclonedx, bom-ref, purl, component type, hashes, licenses, metadata component, serialnumber, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Describe components with type, name, version, purl, hashes, licences and supplier in a CycloneDX BOM."
sources:
  - https://cyclonedx.org/specification/overview/
  - https://github.com/CycloneDX/specification/blob/master/schema/bom-1.6.schema.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CycloneDX components and metadata

Goal: valid CycloneDX components.

Top-level: bomFormat "CycloneDX", specVersion (e.g. 1.6; the overview page lists 1.7 as current), serialNumber (urn:uuid:...), version (integer revision), metadata (timestamp, tools, authors, component = subject, supplier, manufacturer, lifecycles), components, services, dependencies, vulnerabilities, formulation.
Component fields: type (1.6 values: application, framework, library, container, platform, operating-system, device, device-driver, firmware, file, machine-learning-model, data, cryptographic-asset), bom-ref (unique within BOM), name, version, group, supplier, purl, cpe, hashes (alg + content), licenses ([{license:{id:"MIT"}}] or expression), copyright, externalReferences.

Method: set the product as metadata.component and every dependency in components with purl.

Gotchas:
- bom-ref must be unique within the BOM.
- License id must be SPDX ID; otherwise use name.

Verify: validate with cyclonedx-cli validate against the JSON schema.

## Checked

2026-11-02. Checked against the CycloneDX 1.6 JSON schema (top-level and metadata properties, component type enum, bom-ref uniqueness, serialNumber urn:uuid pattern, integer version, hash alg and content, licence id or name, supplier, purl, cpe, copyright, externalReferences) and the cyclonedx-cli README (validate command). Fixed: the component type list was incomplete.

Method: documentation only; no commands were run.
