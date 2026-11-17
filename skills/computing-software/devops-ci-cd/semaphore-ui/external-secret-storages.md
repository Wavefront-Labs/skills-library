---
id: computing-software.devops-ci-cd.semaphore-ui.external-secret-storages
name: external-secret-storages
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [vault, hashicorp-vault, openbao, secret-sync, aws-secrets-manager, semaphore-ui]
level: advanced
status: docs-checked
description: "Use HashiCorp Vault, OpenBao and other external secret managers (Pro) as Key Store backends and sync secrets with sync paths."
sources:
  - https://semaphoreui.com/docs/user-guide/key-store/secret-sync
  - https://semaphoreui.com/docs/user-guide/key-store
  - https://semaphoreui.com/docs/user-guide/key-store/hashicorp-vault
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External secret storages (Pro)

Goal: keep credentials in a central secret manager instead of the Semaphore database.

Supported storages include HashiCorp Vault, OpenBao, AWS Secrets Manager, Azure Key Vault, Devolutions Server and CyberArk; they are configured on the Storages tab of the Key Store. The Key Store page marks AWS Secrets Manager and CyberArk as Enterprise, and the Vault page marks HashiCorp Vault as Pro.

HashiCorp Vault options:
- Vault URL and secrets-engine Mount.
- Token, stored in the database, provided by an environment variable, or read from a file (useful for Vault Agent). A token file must be inside the secrets directory (`dirs.secrets` / `SEMAPHORE_SECRETS_PATH`).
- The storage can run in read-only mode.

Using it: configure the connection, then when creating a Key Store key choose the Vault storage type and give the secret path.

Vault Agent: run it as a sidecar writing a token to a file inside the secrets directory so Semaphore never stores the token.

Syncing: a sync path imports many secrets automatically. Each path has a Path (base folder or subtree to read in the remote storage), a Prefix and a Separator that control how imported secrets are named in Semaphore. Semaphore reconciles remote secrets with local keys.

Related: task JWTs let a task authenticate to Vault or OpenBao without a stored token.

Gotchas:
- Remote storage access is Pro; verify your edition first.
- Rejected token paths produce an error that the file must be inside the secrets directory.

Verify: a key using the storage resolves its value when a task runs.

## Checked

2026-11-04: checked against the Key Store, secret sync and HashiCorp Vault pages. Added which storages the pages mark as Enterprise or Pro.

Method: documentation only; no commands were run.
