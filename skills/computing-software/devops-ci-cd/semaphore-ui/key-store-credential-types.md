---
id: computing-software.devops-ci-cd.semaphore-ui.key-store-credential-types
name: key-store-credential-types
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [key-store, ssh-key, credentials, login-with-password, ansible-vault, semaphore-ui]
level: practitioner
status: docs-checked
description: "Choose the right Key Store credential type: SSH key, login with password, String or None, and generate deploy keys."
sources:
  - https://semaphoreui.com/docs/user-guide/key-store
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Key Store credentials

Goal: store the authentication material Semaphore needs for Git, hosts and secrets.

The Key Store (per project) holds credentials used to clone repositories, connect to hosts and resolve secrets. Its Keys tab lists name, storage backend, type and sync state; the Storages tab (Pro) configures external secret managers.

Types:
- SSH Key: asymmetric auth for Linux hosts and Git over SSH. Fields: name, optional username, optional passphrase (masked), private key in PEM/OpenSSH format.
- Login with password: username and password for host SSH, `sudo` escalation, HTTPS Git (use a personal access token, not your account password), and Ansible Vault passwords (blank login is still used for vault passwords).
- String: a standalone secret such as an API bearer token or webhook secret.
- None: for repositories that need no authentication.

Built-in generator: choose SSH Key, tick Generate SSH Key, click Create. Semaphore generates the keypair, encrypts the private key in the database and shows the public key with a copy button. When editing a generated key you can show or copy the public key again without regenerating. Add the public key as a read-only deploy key on GitHub, GitLab or Bitbucket.

Gotchas:
- Secret inputs are masked in the UI. Editing an existing credential disables them until you tick the Override checkbox, which guards against accidental overwrites.
- File-based keys must live inside the secrets directory.

Verify: attach the key to a repository and run a template; the clone succeeds.

## Checked

2026-11-04: checked against the Key Store page. Replaced an unconfirmed masking and role claim with the documented Override checkbox behaviour.

Method: documentation only; no commands were run.
