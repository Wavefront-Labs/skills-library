---
id: computing-software.cybersecurity-defensive.security-operations.detection-repository-structure
name: detection-repository-structure
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-as-code, detection-repository, versioning, git, code-review, deployment-pipeline, detection-lifecycle]
level: practitioner
status: draft
description: "Structure a detection-as-code repository: layout, metadata, semantic versioning, branching and review, deploy pipelines and keeping production in sync with git."
sources: ["https://github.com/SigmaHQ/sigma", "https://github.com/splunk/security_content", "https://learn.microsoft.com/en-us/azure/sentinel/ci-cd"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection repository structure and versioning

**Goal:** git is the source of truth for every production detection: who changed what,
why, and the ability to roll back.

## Layout
```
detections/
  windows/process_creation/office_spawns_script_host.yml
  cloud/azure/entra_risky_signin_from_new_country.yml
tests/
  office_spawns_script_host/positive.json
  office_spawns_script_host/negative.json
pipelines/          # field mappings per SIEM
macros/ lookups/    # shared allowlists and helpers (or watchlists as CSV)
docs/ads/           # Alerting and Detection Strategy per rule (or inline)
ci/                 # test runner, deploy scripts
```
One rule per file, file name equals a stable slug, rule `id` a UUID that never changes.

## Metadata every rule carries
`id, title, status (experimental/test/stable/deprecated), version, author/owner, created,
modified, ATT&CK techniques, data sources, severity, false positives, triage link,
test references`. Linters enforce presence.

## Versioning
- Bump the rule's `version` integer on any logic change; record why in the commit message
  and a `changelog` field if the platform supports it.
- Tag repository releases (`v2026.10.1`) for each production deploy; rollback = redeploy the
  previous tag.
- Deprecate rather than delete: set `status: deprecated`, disable in deploy, keep the file
  for history and metrics.

## Workflow
- Branch per change, pull request with: what the rule detects, test evidence (positive hits,
  backtest volume), tuning rationale. A second detection engineer reviews logic and noise.
- CI: lint, convert, unit tests (see detection testing CI).
- Deploy from main via pipeline: Splunk app package to search heads (deployer/ACS API),
  Sentinel Repositories or ARM/API, Elastic detection-rules CLI `kibana import-rules`.

## Drift control
Production edits made in the UI bypass review. Detect drift nightly: export deployed rules
via API, diff against main, alert on differences, and either revert or back-port into git.
Restrict UI edit rights on detections to the deploy service account where possible.

## Gotchas
- Tuning lists in the repo need fast changes; allow a lighter review path for allowlist
  data than for rule logic, still via git.
- Secrets (API keys for enrichment) never go in the repo; use the CI secret store.

## Verify
Pick a random production detection: its file, version and last change in git match what
the SIEM runs, and the drift job reports zero differences.
