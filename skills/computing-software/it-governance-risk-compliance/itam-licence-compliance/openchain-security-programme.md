---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.openchain-security-programme
name: openchain-security-programme
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [openchain-security-programme, openchain-iso-18974, iso/iec 18974, openchain security assurance, security policy, vulnerability process, open source security, itam-licence-compliance]
level: practitioner
status: draft
description: "Meet ISO/IEC 18974 foundation: security policy for open-source components, competence, scope and vulnerability response roles."
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

# OpenChain security assurance programme requirements

Goal: demonstrate security management of open-source components.

Core requirements (summarised; confirm the standard):
- Documented security assurance policy for open-source components in supplied software.
- Defined responsibilities, competence and awareness.
- Programme scope and resources.
- Process to identify structure and origin of components (SBOM), to track known vulnerabilities, and to assess and respond.
- Process for handling vulnerability reports from outside, with a contact point.
- Maintain records of evidence.

Method: extend the 5230 programme with security review stages, link SBOM and vulnerability tools to the process, set response SLAs.

Gotchas:
- Having scanners is not a process; show decisions and closures.

Verify: demonstrate one vulnerability from detection to release.
