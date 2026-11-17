---
id: computing-software.systems-network-administration.headscale.upgrade-procedure
name: upgrade-procedure
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, upgrade, minor-version, release-notes, migrations]
level: practitioner
status: docs-checked
description: "Upgrade Headscale safely: one stable minor version at a time, latest patch each, read release notes, stop, back up, update, diff the config, start."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/upgrade.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Headscale

## Rule

Upgrade one stable minor version at a time, never skipping, and use the latest patch release of each. The docs' example path is 0.26.0 to 0.27.1 to 0.28.0.

## Steps

1. Read the GitHub release notes for breaking changes and version-specific instructions.
2. Stop Headscale.
3. Back up the installation (see upgrade-backup).
4. Update Headscale, ideally with the method you installed it with.
5. Compare and update your config file against the configuration reference.
6. Start Headscale.

## Why backup matters

Headscale runs database migrations during upgrades, so the docs strongly recommend a database backup first.

## Gotchas

- The page requires updating from one stable version to the next without skipping minor versions; if you are several versions behind, step through each.

## Checked

2026-11-04. Confirmed against the Headscale upgrade page: the required update path and its 0.26.0, 0.27.1, 0.28.0 example, latest patch advice, the six steps, and the migration warning. Removed unsourced remarks about example config tags and post-start log checks.
Method: documentation only; no commands were run.
