---
id: engineering-technology.biomedical-engineering.device-verification-validation.software-maintenance-release
name: software-maintenance-release
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [software-maintenance, software-release, regression-testing, sbom, software-update]
level: practitioner
status: draft
description: "Run software release and maintenance under IEC 62304: release checklist, versioning, regression strategy, change classification, SBOM, field updates and archiving."
sources: ["IEC 62304 Medical device software - Software life cycle processes (release and maintenance clauses; confirm edition)", "FDA guidance on cybersecurity in medical devices including software bill of materials (confirm current text)", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Software release and maintenance

**Goal:** a repeatable release process and controlled updates through the product life.

## Release
1. **Release criteria:** verification complete, anomalies reviewed (see software-anomaly-management), risk file and traceability current, documentation (including version identification) archived.
2. **Version identification:** unique version on the build and shown in the device and the labelling; a reproducible build with configuration items identified; archive the source, tools and build environment.
3. **Software bill of materials (SBOM)** listing third-party and open-source components with versions, for vulnerability tracking (see soup-management and device-cybersecurity).
4. **Delivery and installation** verification, including checksum or signature checks, and instructions for the installer.

## Maintenance
- **Monitor feedback** from the field and vulnerabilities in dependencies.
- **Classify each change** (corrective, adaptive, perfective, security) and assess the impact on risk and on regulatory status (some changes require a new submission or notification; confirm with regulatory affairs by market).
- **Regression test** in proportion to the change and the risk; full regression for changes touching safety functions; automated test suites help.
- **Field update:** controlled deployment, ability to roll back, user notification and compatibility with hardware and other software versions.
- **End of support:** declare and communicate; plan for obsolete third-party components.

## Verify
- [ ] Release checklist completed and signed with build identification.
- [ ] SBOM current and vulnerability review recorded.
- [ ] Change impact on regulatory status documented for each update.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
