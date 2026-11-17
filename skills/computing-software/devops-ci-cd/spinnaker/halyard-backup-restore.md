---
id: computing-software.devops-ci-cd.spinnaker.halyard-backup-restore
name: halyard-backup-restore
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [halyard, backup, restore, hal-backup, disaster-recovery, secrets]
level: practitioner
status: draft
description: "Back up a Halyard-managed Spinnaker configuration with hal backup create and restore it elsewhere with hal backup restore, including the secrets and path-rewrite caveats."
sources:
  - https://github.com/spinnaker/spinnaker.github.io/blob/master/setup/install/backups.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Halyard keeps most of its state in the `.hal` directory for each deployment it manages, but credential files and user-data paths can live elsewhere on the filesystem, so copying the directory by hand is unreliable. Halyard provides a command for it.

```bash
hal backup create
```

This produces a tar file containing all linked local files plus a modified halconfig that points at the files inside the tarball.

**Restore** on any machine or user running Halyard:

```bash
hal backup restore --backup-path <backup-name>.tar
```

Halyard expands the tarball and replaces the existing `.hal` directory.

Two warnings from the page:
- The backup includes every secret you supplied to Halyard, so keep the tar file safe.
- If you run `hal backup create` and `hal backup restore` one after another on the same machine, links to local files are rewritten to point at a `.backup/required-files` directory inside `.hal`.

The page positions this as the way to reproduce or redeploy a configured Spinnaker without coupling it to the VM Halyard happens to be installed on. Related: the secrets framework (separate skill) lets you keep secret values out of the halconfig in the first place.

## Checked

2026-11-04. Create and restore commands, the contents of the tar file and both warnings were confirmed on the Back Up Your Config page. The secrets cross-reference points to the Secrets reference page, also read.

Method: documentation only; no commands were run.
