---
id: computing-software.devops-ci-cd.semaphore-ui.repositories-and-deploy-keys
name: repositories-and-deploy-keys
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [repositories, git, deploy-keys, ssh, https, semaphore-ui]
level: practitioner
status: docs-checked
description: "Add Git repositories (SSH, HTTPS, file, local path) and authenticate with read-only deploy keys."
sources:
  - https://semaphoreui.com/docs/user-guide/repositories
  - https://semaphoreui.com/docs/faq/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repositories

Goal: tell Semaphore where playbooks, roles and scripts live.

Supported sources: local path (`/path/to/the/repo`), `file://` Git repo, remote HTTPS, SSH (`ssh://` or `git@host:org/repo.git`), and `git://` (not recommended for security). All task templates require a repository.

A repository that needs authentication uses a key from the Key Store. SSH repositories use an SSH key; for HTTPS the troubleshooting page uses a Login with password key (login plus personal access token). For repositories without authentication use a key of type `None`.

Recommended: one read-only deploy key per repository.
1. Key Store, New Key, select SSH Key, click Generate; Semaphore shows the public key to copy.
2. Copy the public key.
3. On GitHub: repository Settings, Deploy keys, Add deploy key, leave Allow write access unchecked. GitLab: Settings, Repository, Deploy keys. Bitbucket: Repository settings, Access keys, Permissions set to Read.
4. In Semaphore set the URL to `git@github.com:organization/repository.git` and pick the key.

Benefits: independence from personal accounts, least privilege, small blast radius on rotation.

The repository key is used only for that repository. For submodules, `requirements.yml` roles and other hosts, use Host config mappings.

Common error: `fatal: bad numeric config value '0' for 'GIT_TERMINAL_PROMPT': invalid unit` means an HTTPS repo needs auth; add a Login with password key (a PAT) and select it on the repository.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository: user-guide/repositories.md (it imports only the Tabs components, no snippet files) and faq/troubleshooting.md. Confirmed: the supported URL forms and git:// caveat, Key Store authentication and the None key type, the deploy key benefits, the Generate flow, the GitHub, GitLab and Bitbucket menu paths and read-only settings, the Host config remark, and the GIT_TERMINAL_PROMPT error and its fix. Removed: the unstated Create button, the branch remark (it belongs to the template page), and the invented clone-log Verify step.
Method: documentation only; no commands were run.
