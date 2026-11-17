---
id: computing-software.cloud-infrastructure-engineering.harbor.sbom-generation
name: sbom-generation
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [sbom, spdx, trivy, sbom-generation, harbor]
level: practitioner
status: docs-checked
description: "Generate SBOMs in Harbor 2.11 and later automatically on push or manually, and download them in SPDX format."
sources:
  - https://goharbor.io/docs/main/administration/sbom-integration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Harbor 2.11 an SBOM (inventory of components, versions and licences) can be generated together with the default scanner, Trivy. The SBOM is produced with the scanner assigned to the project.

Automatic generation on push:
1. Open the project, **Configuration** tab.
2. Tick **SBOM generation** and **SAVE**.
3. Newly pushed artifacts (`docker push ...`) in that project then trigger SBOM generation using the scanner assigned in the project's Scanner section.

Results: on the project artifact page an **SBOM Details** link opens a table of package name, version and licence. **DOWNLOAD SBOM** retrieves the full SBOM in SPDX format.

Manual generation: if automatic generation is off or unwanted, go to the artifact page, select one or more images and click **GENERATE SBOM**, which is enabled once a selection exists. The **ACTIONS** drop-down lets you abort SBOM generation.

Deleting an SBOM: use the three-dot menu next to the SBOM accessory and choose Delete; the physical deletion happens during garbage collection. Pull-based or push-based replication rules can replicate artifacts together with their SBOMs.

## Checked

2026-11-03. Version 2.11, Trivy, the Configuration tab steps, SBOM Details, DOWNLOAD SBOM (SPDX), GENERATE SBOM, ACTIONS abort, deletion and replication were read against the Harbor docs page SBOM Generation Capabilities. Removed: the claim that earlier pushes are not covered and the advice to confirm the project scanner supports SBOM (neither is on the page).

Method: documentation only; no commands were run.
