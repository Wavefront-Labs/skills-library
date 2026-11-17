---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.source-available-and-fair-code-licences
name: source-available-and-fair-code-licences
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [source-available-and-fair-code-licences, licence-classification-osi-fsf, bsl, business source license, source available, elastic license, commons clause, fair code, hashicorp, itam-licence-compliance]
level: advanced
status: draft
description: "Recognise source-available licences such as BSL, SSPL, Elastic and Commons Clause and what they restrict."
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

# Source-available, BSL and non-open licences

Goal: avoid assuming a visible source means open source.

Examples (confirm each current text):
- Business Source License (BSL 1.1): source visible, production use restricted until a change date, after which the code converts to an open licence.
- SSPL: not OSI approved; requires service source release.
- Elastic License 2.0: prohibits providing the software as a managed service.
- Commons Clause: adds a restriction on selling the software.
- Several vendors relicensed from permissive to source-available (HashiCorp, Redis, Elastic) and sometimes back.

Method: add a "non-OSI" flag in your component catalogue; require legal approval and track relicensing events for critical dependencies; consider forks hosted by foundations.

Gotchas:
- A previously permissive version stays under its original licence, but updates may not.
- Cloud-provider managed services may be affected differently.

Verify: licence change alerts are on for core dependencies.
