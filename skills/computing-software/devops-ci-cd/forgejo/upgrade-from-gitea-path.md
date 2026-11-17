---
id: computing-software.devops-ci-cd.forgejo.upgrade-from-gitea-path
name: upgrade-from-gitea-path
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [gitea-migration, upgrade-from-gitea, forgejo-v10, two-step-upgrade]
level: advanced
status: docs-checked
description: "Move a Gitea instance to Forgejo using the supported two-step path through v10.0.x."
sources:
  - https://forgejo.org/docs/latest/admin/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo is a hard fork of Gitea and supports transparent upgrades from Gitea up to and including Gitea v1.22. The guide prescribes two steps:

1. Upgrade from any Gitea version up to and including v1.22.x to Forgejo v10.0.x.
2. Upgrade from Forgejo v10.0.x to any Forgejo version greater than v10.

The generic upgrade preparation still applies: make a full backup, manually analyze and update customized templates and CSS, run `forgejo manager flush-queues` (rerun with a larger `--timeout` if it times out), then replace the binary or container image; the upgrade procedure takes care of migrations. Afterwards run `forgejo doctor check --all --log-file /tmp/doctor.log` and verify manually through the web interface.

The database version is stored in the database to prevent an accidental downgrade: a Forgejo that finds a newer database version refuses to start. Restoring the pre-upgrade backup is easy, but if a problem is only found days or weeks later it is no longer an option, so verify carefully. The guide also lists known problematic versions or paths; for example, for all versions a blank or 500 page after login on SQLite is worked around by upgrading to Forgejo 1.19.3-0 or greater and running `gitea doctor check --all --fix`.

Check that your Gitea is 1.22.x or lower before starting; the guide only describes support up to Gitea v1.22. The detailed Gitea-specific instructions are linked from the guide's "Upgrade from Gitea" section and are not covered by this skill.

## Checked

Date: 2026-11-07
Confirmed against the "Upgrade guide" page (forgejo.org/docs/latest/admin/upgrade/), read in full including its code blocks: Gitea support up to v1.22 included, the two-step path via v10.0.x, the preparation steps (templates/CSS, `forgejo manager flush-queues` and `--timeout`), the verification step with `forgejo doctor check --all`, the database version guard against downgrades, and the SQLite blank/500 workaround.
Corrected: removed "after each step" (the page does not say to verify after each step) and "keep the backup until the final version has been verified" (the page says restoring is not an option once a problem is found late); replaced with what the page states. The doctor command line now matches the page (with `--log-file`).
Method: documentation only; no commands were run.
