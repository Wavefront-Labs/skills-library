---
id: computing-software.devops-ci-cd.rundeck.key-storage-paths-and-acls
name: key-storage-paths-and-acls
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, key-storage, ssh-key-storage-path, storage-acl, project-key-storage]
level: practitioner
status: docs-checked
description: "Organise Rundeck Key Storage by project path, reference keys from nodes with ssh-key-storage-path, grant storage ACLs, and control public key download."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/key-storage/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Key Storage holds private keys and passwords for plugins and node executors. UI: System Menu (gear) or Project Settings. Recommended layout is by project: `keys/project/[project-name]/[key-name]`, for example `keys/project/project1/default.pem`; subfolders are allowed. Add a key via "Add or Upload a Key", choose type (Private Key or Password), upload a file or enter text, set path and name.

Use in the default SSH node executor with a node attribute:

```
ssh-key-storage-path="/keys/users/${job.username}/default.pem"
```

Context values such as `${job.username}` can be embedded.

ACLs (`for: storage`, actions `create`, `update`, `read`, `delete`):

```yaml
description: authorize keys/ storage files
by:
  group: admin
for:
  storage:
    - match:
        path: 'keys/project/${name}.*'
      allow: [read]
context:
  application: rundeck
```

By default `keys` access needs project-scope authorization. Set `rundeck.feature.projectKeyStorage.enabled=false` to move it to application scope.

Backends: `db` (default, BLOBs in the database) and `file`; or a storage plugin (Vault, AWS Secrets Manager, CyberArk, Thycotic, Azure Key Vault).

Public key download is off by default: enable `rundeck.feature.publicKeysDownload.enabled=true`, and for the GUI also `rundeck.gui.keystorage.downloadenabled=true`.

## Checked

2026-11-04: UI location, project path layout, ssh-key-storage-path example, ACL actions and example, feature flags, storage backends and plugin list confirmed against the Rundeck Key Storage page.
Method: documentation only; no commands were run.
