---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-repository-password
name: fs-backup-repository-password
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [velero-repo-credentials, repository-password, backupepository, kopia-encryption, backup-repo]
level: advanced
status: docs-checked
description: "Replace the default velero-repo-credentials repository password before the first backup, and why changing it later breaks old backups."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero creates a secret named `velero-repo-credentials` in the install namespace holding a default backup repository password. You can replace it with your own, base64 encoded, under the key `repository-password`:

```
data:
  repository-password: <custom-password>
```

Timing is critical. The backup repository is created during the first backup (fs-backup or data mover) that targets it after installing with the node agent. If you change the secret after that first backup created the repository, Velero cannot connect to the older backups. Set the password before the first backup.

Security limitation from the same page: Velero uses a static, common encryption key for all backup repositories it creates by default, which means anyone with access to your backup storage can decrypt your backup data. Restrict access to the bucket accordingly, and do not treat the default as a confidentiality control.

Related: Velero creates one repository per namespace the first time FSB or a restore needs it. List them and check readiness:

```
velero repo get
velero repo get REPO_NAME -o yaml
```

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
