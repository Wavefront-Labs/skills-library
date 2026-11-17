---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sca-tool-selection-and-pipeline
name: sca-tool-selection-and-pipeline
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sca-tool-selection-and-pipeline, software-composition-analysis, sca, ort, oss review toolkit, scancode, fossology, trivy, dependency scanning, license scanning, itam-licence-compliance]
level: practitioner
status: draft
description: "Choose and wire SCA tools such as ORT, ScanCode, FOSSology, Trivy and commercial scanners into CI with policy gates."
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

# SCA tool selection and CI pipeline

Goal: automated licence and vulnerability detection per change.

Method:
- Dependency-based tools (ORT, Trivy, Dependabot alerts, commercial SCA) read manifests; file-based scanners (ScanCode, FOSSology) detect licence text and headers in source.
- Pipeline: analyse, scan, evaluate (policy rules), report (notices, SBOM). ORT stages are analyzer, scanner, evaluator, reporter.
- Gate: fail builds on denied licences or critical vulnerabilities; allow overrides via curations with reviewer approval.
- Keep curations (corrected licence data) in version control.

Gotchas:
- Scanning every commit with file-level tools is slow; schedule it for releases.
- Declared licence metadata in registries is sometimes wrong.

Verify: introduce a test component with a denied licence and confirm failure.
