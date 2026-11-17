---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.snippet-and-code-copy-risk
name: snippet-and-code-copy-risk
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [snippet-and-code-copy-risk, permissive-compliance-practice, snippet scanning, stack overflow cc by-sa, ai generated code, code provenance, copilot, matching, itam-licence-compliance]
level: advanced
status: draft
description: "Control licence risk from copied snippets, Stack Overflow answers and AI code assistants via scanning and policy."
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

# Snippets, copy-paste and AI-generated code

Goal: reduce unknown-origin code in the product.

Method:
- Policy: no copying code without a licence check; Stack Overflow content is CC BY-SA (with attribution and share-alike; confirm version), which doesn't fit proprietary code easily.
- Scan: use snippet-matching scanners (for example ScanCode for copyright and licence detection, FOSSology, commercial snippet scanners) at pull request time.
- AI assistants: configure public-code-match filters where offered; record tool usage policy; review output as third-party code.
- Keep a record of reviewed suspicious matches.

Gotchas:
- Small trivial snippets may not be copyrightable but policy still needs thresholds.
- Absence of a match is no guarantee.

Verify: scan results are attached to release approval.
