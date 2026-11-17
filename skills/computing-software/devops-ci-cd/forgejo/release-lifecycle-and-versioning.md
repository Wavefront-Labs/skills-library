---
id: computing-software.devops-ci-cd.forgejo.release-lifecycle-and-versioning
name: release-lifecycle-and-versioning
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [release-lifecycle, lts, semantic-versioning, security-announcements]
level: intro
status: docs-checked
description: "Choose between stable, LTS and experimental Forgejo releases and understand the semantic versioning promise."
sources:
  - https://forgejo.org/docs/latest/admin/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo releases pass through three states. The latest stable release gets full support, bugfixes and security fixes for three months, plus a two week window after the next stable release appears. The long term support (LTS) release is the one published in the first quarter of each year; it receives only critical bugfixes and security support for one year and three months. The experimental state is the current development version, which gets new features and should not be used in production.

Since 7.0.0 Forgejo follows semantic versioning: no breaking change happens unless the first number changes, so 8.0.0 may break things that worked in 7.0.0. The release notes list those breaking changes, and depending on the instance they may need manual intervention. The 1.19, 1.20 and 1.21 releases, before 7.0.0, each contained breaking changes and did not follow semantic versioning.

To plan upgrades ahead of security releases, watch or subscribe to the RSS feed of the security-announcements repository. It reveals only the expected release date, not the vulnerability details, so administrators can schedule maintenance and tighten the instance in advance.

## Checked

2026-11-04. Confirmed against the Forgejo Upgrade guide (Release life cycle and Semantic version compliance): the three states with their support periods, the first-quarter LTS rule, semantic versioning from 7.0.0, the 1.19 to 1.21 exception and the security-announcements RSS feed. Removed: the closing rule to track only LTS or stable, since the page says only that experimental should not be used in production.

Method: documentation only; no commands were run.
