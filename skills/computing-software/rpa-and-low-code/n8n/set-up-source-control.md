---
id: computing-software.rpa-and-low-code.n8n.set-up-source-control
name: set-up-source-control
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, source-control, git, deploy-key, personal-access-token, environments]
level: practitioner
status: docs-checked
description: "Connect an n8n instance to a Git repository for environments: SSH deploy keys or HTTPS tokens, GIT_SSL_CAINFO for private CAs, branch choice and Protected instance."
sources:
  - https://docs.n8n.io/administer/use-source-control-and-environments/set-up-source-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: link a Git repository so n8n can push and pull work as environments.

1. **Repository and branches**: create a repository for n8n and a branch per environment (for example test and production).
2. **Connection**: SSH (deploy keys) or HTTPS (Personal Access Tokens).
3. **Auth**:
   - SSH: create a deploy key in the repository using the SSH key n8n shows; it must have write access.
   - HTTPS: create a PAT with repository read/write access: Contents read/write on GitHub, source code pull/push on GitLab.
   - Private certificate authority (n8n 2.40.0 and later): set `GIT_SSL_CAINFO` to a PEM file with the CA certificate. Git uses its own trust store and this replaces the default, so include public roots if the instance also reaches public Git hosts.
4. In **Settings > Environments** select **Connect**. Under **Instance settings** choose the branch for this instance. Optionally tick **Protected instance** (prevents editing source-controlled resources; good for production) and pick an instance colour shown near the push and pull buttons. **Save settings**.

See the branching patterns skill for how many branches to use.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Set up source control" page (docs.n8n.io, read in full).
Nothing removed; auth methods, token permissions, GIT_SSL_CAINFO note (2.40.0) and instance settings match the page.
