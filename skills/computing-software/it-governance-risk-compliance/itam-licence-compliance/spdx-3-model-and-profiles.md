---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-3-model-and-profiles
name: spdx-3-model-and-profiles
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-3-model-and-profiles, spdx-relationships-and-licences, spdx 3.0, profiles, core, software profile, licensing profile, security profile, build profile, ai profile, json-ld, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Understand the SPDX 3.0 profile-based model (Core, Software, Licensing, Security, Build, AI, Dataset) and JSON-LD serialisation."
sources:
  - https://github.com/spdx/spdx-3-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX 3.0 model and profiles

Goal: know what changed from 2.3 and when to adopt 3.0.

Highlights:
- Model of elements and relationships defined in profiles. The ProfileIdentifierType vocabulary lists core, software, simpleLicensing, expandedLicensing, security, build, ai, dataset, extension, lite, hardware, supplyChain, operations, functionalSafety and service. Lite is a simple view of the data (mandatory and recommended information) for some industries.
- Serialised as JSON-LD (the spec repo has a jsonld serialization with examples); elements carry spdxId and creationInfo properties.
- Software profile has Package, File, Snippet, Sbom and SoftwareArtifact classes, with properties such as packageUrl, packageVersion and primaryPurpose.
- Security profile has Vulnerability and vulnerability assessment relationships: VEX ones (VexAffected, VexFixed, VexNotAffected, VexUnderInvestigation) plus CVSS, EPSS and SSVC assessments.
- AI and Dataset profiles describe AI models and datasets.

Method: check which SPDX version your tools and customers accept and stay on 2.3 until they read 3.0.

Gotchas:
- Confirm your consumers read 3.0 before switching.
- Property names differ from 2.3: the spec repo's converted-from-2.x JSON-LD example uses software_packageVersion for the package version.

Verify: compare your output with the JSON-LD examples in the spec repo.

## Checked

2026-11-02. Checked against the spdx-3-model repository (README, model/Software, Security, Lite, Core vocabularies, jsonld serialization examples): profile identifiers, Software classes and properties, Security VEX and assessment classes, spdxId and creationInfo, software_packageVersion in the converted example. Removed: claims about tool support and conversion-tool maturity, the Licensing profile name (the model has simpleLicensing and expandedLicensing), and the unverified 'graph-based' wording.

Method: documentation only; no commands were run.
