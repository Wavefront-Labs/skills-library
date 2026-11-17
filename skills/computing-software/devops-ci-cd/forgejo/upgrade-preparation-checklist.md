---
id: computing-software.devops-ci-cd.forgejo.upgrade-preparation-checklist
name: upgrade-preparation-checklist
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [upgrade-preparation, flush-queues, custom-templates, docker-version]
level: practitioner
status: docs-checked
description: "Prepare a Forgejo upgrade with a full backup, queue flush, customization review and a post-upgrade verification plan."
sources:
  - https://forgejo.org/docs/latest/admin/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before replacing the binary or container image, take a full backup. It is required when moving to a new stable release, for example v17.0 to v18.0, and a good precaution even for patch releases such as v17.0.0 to v17.0.1.

Preparation steps from the upgrade guide:

- Review customizations. Read the patches to the sources of the template directory and manually update customized CSS or content. Locate CustomPath through the configuration tab of the Site administration panel as an admin, not through `forgejo help`.
- Run `forgejo manager flush-queues`. If it times out, run it again with a larger `--timeout`. This matters because the queues hold serialized data that is not guaranteed to be backward compatible between versions.
- For Docker installations, use docker 20.10.6 or newer; older versions cause mysterious problems unrelated to Docker itself.
- Read the list of things to know for your specific starting version and check whether it applies.

Then upgrade straight to the latest released version by replacing the binary or image; the upgrade procedure runs the database migrations. Afterwards verify carefully (see the verification skill), because a backup can only be restored easily if the problem is found immediately.

## Checked

Date: 2026-11-07
Confirmed against the "Upgrade guide" page (forgejo.org/docs/latest/admin/upgrade/), read in full including its code blocks: the backup requirement for a new stable release (v17.0 to v18.0 example) and precaution for patch releases, the template/CSS review, the CustomPath location note, `forgejo manager flush-queues` with `--timeout` and the reason (serialized queue data), the docker 20.10.6 note, the version-specific notes, and upgrading straight to the latest release by replacing the binary or image.
Corrected: nothing needed; every claim matched the page text.
Method: documentation only; no commands were run.
