---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.open-source-release-process
name: open-source-release-process
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [open-source-release-process, ospo-and-open-source-governance, open sourcing, release checklist, licence choice, secrets scan, contributing.md, code of conduct, trademark, itam-licence-compliance]
level: advanced
status: draft
description: "Release internal code as open source safely: IP clearance, licence choice, secrets scan, governance files and CLA/DCO."
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

# Releasing your own code as open source

Goal: publish without leaking IP or secrets.

Checklist:
1. Business case and approval; confirm ownership of all code (employee agreements, contractors).
2. Scan third-party code for compatible licences; remove incompatible parts.
3. Choose outbound licence aligned to goals (Apache-2.0 for patent grant, MIT for simplicity, AGPL/GPL for copyleft).
4. Scan history for secrets (gitleaks, trufflehog); consider publishing a clean history.
5. Add LICENSE, README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md, REUSE headers, trademark policy.
6. Decide DCO or CLA; set up governance and maintainers.
7. Set up SBOM and vulnerability reporting.

Gotchas:
- Patents are not automatically covered by MIT; consider Apache-2.0.
- Internal hostnames and customer data in code history.

Verify: legal checklist signed before the repo is made public.
