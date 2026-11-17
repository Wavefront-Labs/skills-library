---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.reuse-in-ci-and-spdx-export
name: reuse-in-ci-and-spdx-export
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [reuse-in-ci-and-spdx-export, reuse-specification, reuse lint, github action, pre-commit, reuse spdx, compliance badge, fsfe reuse action, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Automate REUSE compliance checks in CI, add a badge and generate SPDX output from REUSE metadata."
sources:
  - https://reuse.software/spec-3.3/
  - https://reuse.software/tutorial/
  - https://reuse.software/dev/
  - https://github.com/fsfe/reuse-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REUSE in CI and SPDX export

Goal: continuous licence hygiene.

Method:
- GitHub Action: fsfe/reuse-action in a workflow, or a pre-commit hook that runs reuse lint on every commit (both shown on the REUSE developer page).
- Register the project with the REUSE API for a dynamic compliance badge (optional; see the developer page).
- Export: reuse spdx -o FILE generates an SPDX bill of materials for the project (without -o it goes to STDOUT).
- reuse lint --json (-j) outputs the lint results as JSON.
- Combine with dependency SBOM for a full picture.

Gotchas:
- Files ignored by the version control system (for example through .gitignore) are not covered files under the specification, and the tool honours that.

Verify: failing PR with a missing header is blocked.

## Checked

2026-11-02. Checked against the REUSE developer page (fsfe/reuse-action step, pre-commit hook, REUSE API badge), the reuse-tool man pages (reuse spdx --output, reuse lint --json) and the REUSE 3.3 specification (VCS-ignored files). Removed: the vendored-files claim (not in these pages).

Method: documentation only; no commands were run.
