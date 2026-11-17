---
id: computing-software.systems-network-administration.backup-and-recovery.git-repository-and-devops-saas-backup
name: git-repository-and-devops-saas-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [git-repository-backup, saas-backup, git-mirror, git-bundle, github-backup, gitlab-backup]
level: practitioner
status: docs-checked
description: "Back up Git repositories and DevOps SaaS: mirror clones and bundles, LFS objects, wikis, issues and PRs via APIs, GitHub Enterprise backup-utils, and GitLab backup plus secrets."
sources:
  - https://git-scm.com/docs/git-bundle
  - https://github.com/github/backup-utils
  - https://docs.gitlab.com/administration/backup_restore/backup_gitlab/
  - https://docs.github.com/en/rest/migrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git repository and DevOps SaaS backup

**Goal:** you can rebuild source code, history and the surrounding project data if the platform, an org admin account or a repo is lost.

## Code
```sh
git clone --mirror git@github.com:acme/app.git app.git      # all refs
git -C app.git remote update --prune                        # incremental refresh
git -C app.git bundle create ../app-$(date +%F).bundle --all
git bundle verify ../app-DATE.bundle
```
Enumerate repos via API (`gh repo list acme --limit 1000 --json name`; the default limit is 30) so new repos are included automatically. If the repos use Git LFS, check that your backup also captures the LFS objects.

## Beyond code
Issues, pull requests, releases, CI settings, project boards and webhooks are not in a Git clone; check what your platform's export covers.
- GitHub: organisation migration archives via the Migrations REST API (start, download and delete an organisation migration archive), or a third-party backup service.
- **GitHub Enterprise Server**: the `backup-utils` project provides `ghe-backup` and `ghe-restore`. It is now the legacy tool: GHES 3.20 has a built-in backup service, and Backup Utilities is to be retired from GHES 3.22. Use the built-in service for new deployments on 3.20 or later.
- **GitLab self-managed**: `sudo gitlab-backup create` (Git repositories and LFS objects, uploads, CI/CD artifacts and job logs, and the database) **plus** `/etc/gitlab/gitlab-secrets.json` and `/etc/gitlab/gitlab.rb` backed up separately. The secrets file holds the database encryption key, so without it GitLab cannot decrypt stored data such as two-factor and CI/CD secure variables; it may also change after upgrades. Keep it apart from the backup it protects.

## Gotchas
- Force-push or repo deletion propagates to mirrors that refresh with `--prune`; keep dated bundles or snapshots, not just a live mirror.
- Credentials used by backup jobs can expire; alert on failures.

## Verify
Monthly: clone from a bundle, check out the default branch and build; restore a GitLab backup to a test instance including the secrets file.

## Checked
2026-10-28. Confirmed against git-bundle and git-clone docs (`bundle create`, `bundle verify`, `clone --mirror`, `remote update`), the gh CLI `repo list` page (`--limit` default 30, `--json`), the GitHub Migrations REST page (organisation archive download and delete), the backup-utils README (`ghe-backup`, `ghe-restore`, retirement notice) and the GitLab backup page (`gitlab-backup create`, contents, secrets file). Removed: the claims about LFS in mirrors, wiki repo naming, named SaaS products, Actions secrets export, Azure DevOps and Bitbucket statements and the `--filter` advice, none of which the pages state.
Method: documentation only; no commands were run.
