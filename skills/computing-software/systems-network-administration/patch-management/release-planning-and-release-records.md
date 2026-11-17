---
id: computing-software.systems-network-administration.patch-management.release-planning-and-release-records
name: release-planning-and-release-records
category: computing-software
field: systems-network-administration
product: patch-management
tags: [release-planning, release-management, release-record, release-types, definitive-media-library, go-no-go, itil-4, definitive-media-library-dml, go-no-go-review, release-type-classification]
level: practitioner
status: draft
description: "Plan releases under ITIL release management: release units and types, release records, schedules, readiness criteria and go/no-go, with monthly patch bundles as a worked case."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-release-management
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-deployment-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release planning and release records

**Goal:** changes reach users as coherent, tested, traceable releases rather than a stream of unrelated deployments.

## Concepts
- **Release**: a version of a service or component (or set of them) made available together.
- **Release unit**: the smallest part released independently (an app, an OS image, a monthly patch bundle).
- **Release types**: major (new features, breaking changes), minor (enhancements, fixes), emergency (urgent fix). Patch programmes often treat "October 2026 server patch bundle" as a minor release with an emergency variant for out-of-band fixes.
- **Release vs deployment**: deployment moves components to environments; release makes them available to users. Feature flags and dark launches separate the two.

## Release record (one per release)
| Field | Example |
|---|---|
| Release ID / name | REL-2026-10-SRV |
| Contents | KB list, package versions, repository snapshot ID, image versions |
| Linked changes | RFCs per deployment wave |
| Environments and dates | Test 14 Oct, Pilot 16 Oct, Prod waves 21-28 Oct |
| Readiness criteria | Tests passed, known issues reviewed, rollback tested, support briefed |
| Known errors / issues | Vendor known issues and workarounds |
| Go/no-go decision | Who, when, outcome |
| Status | Planned, built, tested, deployed, closed |

## Planning
1. Release calendar aligned to vendor cadences (Patch Tuesday, quarterly app releases) and the change schedule, avoiding freezes.
2. Build from controlled sources: definitive media library / artifact repository with hashes.
3. Readiness review before each wave; go/no-go with named decider.
4. Close the release with deployment results, incidents linked, and lessons.

## Gotchas
- Releases that silently pick up "latest" packages are not reproducible; pin to snapshots.
- Too-large releases mix risky and trivial changes; split them.

## Verify
For any production system you can name the release it is on and list exactly what that release contains.
