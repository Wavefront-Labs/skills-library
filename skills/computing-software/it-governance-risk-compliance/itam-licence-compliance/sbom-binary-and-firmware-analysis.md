---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-binary-and-firmware-analysis
name: sbom-binary-and-firmware-analysis
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-binary-and-firmware-analysis, sbom-generation, binary composition analysis, firmware sbom, third party sbom, supplier sbom, ossbom, binary scanning, itam-licence-compliance]
level: advanced
status: draft
description: "Reconstruct SBOMs when source is unavailable using binary composition analysis, vendor SBOM requests and enrichment."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SBOMs from binaries, firmware and third-party software

Goal: component visibility without source.

Method:
- Request SBOMs from suppliers in SPDX or CycloneDX, with contract language specifying format, frequency, depth.
- If none, run binary analysis (strings and signature matching, commercial BCA tools, open-source options like Syft's binary cataloger or EMBA for firmware; confirm capabilities).
- Unpack firmware images (binwalk) then identify packages and versions.
- Mark confidence and generation context (analysed from binary) so consumers know limits.
- Enrich with licence data from package metadata.

Gotchas:
- Binary matching gives false positives; verify high-risk results manually.
- Obfuscation and stripped symbols reduce accuracy.

Verify: spot-check 10 detected components against known build manifests.
