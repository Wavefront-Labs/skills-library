---
id: computing-software.qa-testing-engineering.test-case-design.installability-and-upgrade-testing
name: installability-and-upgrade-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [installability-testing, upgrade-testing, maintainability-testing, portability-testing, uninstall-testing, database-migration-upgrade, istqb-tta, rollback-testing]
level: practitioner
status: draft
description: "Test installation, upgrade, rollback and uninstall: clean and dirty installs, upgrade paths from supported versions, data migration on upgrade and zero-downtime deploys."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installability and upgrade testing

**Goal:** users and operators can install, upgrade, downgrade and remove the software reliably. CTAL-TTA v4.0 4.6 (portability: installability).

## Install
- Clean install on each supported OS/platform with default and custom options (path with spaces/non-ASCII, non-admin user, offline install).
- Prerequisites missing: installer detects and reports clearly.
- Interrupted install (kill mid-way, disk full) leaves a recoverable state.
- Silent/unattended install (`msiexec /i app.msi /qn /l*v install.log`, `apt-get install -y`, Helm `--atomic`).

## Upgrade
- Every **supported upgrade path** (N-1 -> N, N-2 -> N, skipped versions) with real data from each old version.
- Data and config migrated; user settings preserved; database migrations idempotent and reversible.
- Zero-downtime upgrade for services: rolling deploy while load test runs; old and new versions running side by side against the same DB (expand/contract migrations).

## Rollback / downgrade
Rollback to previous version with data written by the new version; feature flags off path.

## Uninstall
Removes files, services, registry keys; keeps or removes user data as documented; reinstall afterwards works.

## Gotchas
- Testing only clean installs; real customers upgrade.
- Migrations that work on empty schemas but lock big tables in production; test with production-sized data.

## Verify
Upgrade matrix (from version x platform) with results and timings, plus rollback evidence.
