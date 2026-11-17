---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-attributes-properties
name: archimate-attributes-properties
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-attributes-properties, archimate-customisation, properties, attributes, element properties, lifecycle, owner, cost, metadata, model quality, enterprise-architecture]
level: practitioner
status: draft
description: "Attach properties such as cost, lifecycle, owner and criticality to elements to support analysis and reporting."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attributes, properties and model data

Goal: models that can be queried and reported.

- Decide a small property set: owner, lifecycle status, criticality, cost, TIME category, source.
- Use controlled values; define who maintains each property.
- Export to CSV or the Open Exchange format to analyse.
- Use properties for heat maps and portfolio views.

Gotchas:
- Unmaintained properties are worse than none; assign owners.

Verify: reports show at least 90 percent of elements with owner and lifecycle.
