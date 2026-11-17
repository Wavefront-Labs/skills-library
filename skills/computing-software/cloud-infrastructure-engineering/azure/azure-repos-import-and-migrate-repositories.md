---
id: computing-software.cloud-infrastructure-engineering.azure.azure-repos-import-and-migrate-repositories
name: azure-repos-import-and-migrate-repositories
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-repos, repo-import, repo-migration, git-mirror, tfvc-to-git, git-tfs, git-lfs, github-enterprise-importer, large-repositories, history-preservation]
level: practitioner
status: docs-checked
description: "Import or migrate repositories into or out of Azure Repos: import repository from Git URL, mirror push with all refs and LFS, TFVC to Git, and moving to GitHub with history."
sources: ["https://learn.microsoft.com/en-us/azure/devops/repos/git/import-git-repository", "https://learn.microsoft.com/en-us/azure/devops/repos/git/import-from-tfvc", "https://learn.microsoft.com/en-us/azure/devops/repos/git/limits", "https://docs.github.com/en/migrations/using-github-enterprise-importer/migrating-from-azure-devops-to-github-enterprise-cloud"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import and migrate repositories (Azure Repos)

**Goal:** move code with full history, branches, tags and LFS objects into (or out of) Azure Repos,
and cut teams over without losing work in flight.

## 1. Into Azure Repos from another Git host
**Import repository** (server-side, simplest): Repos → *Import repository* → clone URL (+ credentials
for private) → creates the repo with all branches/tags.
```bash
az repos import create --git-source-url https://github.com/acme/orders.git --repository orders \
  --requires-authorization --user-name <user> --org https://dev.azure.com/<org> -p Shop
```
**Mirror push** (when you need control, LFS, or the source isn't reachable from Azure DevOps):
```bash
git clone --mirror https://source.example.com/acme/orders.git && cd orders.git
git lfs fetch --all                                   # if the repo uses LFS
git remote set-url --push origin https://dev.azure.com/<org>/Shop/_git/orders
git push --mirror && git lfs push --all origin
```
- Limits: pushes are capped at 5 GB, but a repo over 5 GB must be imported through the web (Import repository), not the command line; Git LFS blobs don't count towards the 5 GB. Strip unneeded binaries with `git filter-repo` *before* the move if you're allowed to rewrite.

## 2. TFVC → Git
- Built-in **import from TFVC**: up to **180 days** of history, and the imported repo plus history can't exceed 1 GB — fine for a clean start.
- Full history: `git-tfs clone https://dev.azure.com/<org> $/Project/Main --branches=all` (slow; on huge repos, take latest + keep TFVC read-only for archaeology).
- Before switching: lock TFVC (deny check-in), map users, convert `.tfignore` to `.gitignore`, move binaries to Artifacts/LFS.

## 3. Out of Azure Repos to GitHub
- **GitHub Enterprise Importer** is GitHub's supported path from Azure DevOps to GitHub Enterprise Cloud; follow GitHub's "Migrating from Azure DevOps" guide for access, install, migration and follow-up steps.
- Check which items migrate (branch policies, pipelines, PRs) in that guide, and recreate the rest as GitHub rulesets.

## 4. Cutover checklist
1. Announce freeze; final sync (`git fetch` + `git push --mirror` again).
2. Make the source read-only.
3. Re-create branch policies/rulesets, CODEOWNERS/required reviewers, pipelines' repo references, service hooks/webhooks.
4. Developers: `git remote set-url origin <new-url>`; open PRs must be recreated (unless the importer migrated them).

## Gotchas
- Update `.gitmodules` URLs if submodules point at the old host.
- Large binary history makes every clone slow; decide on LFS/filter-repo before, not after, the cutover.

## Verify
- [ ] `git ls-remote` branch/tag counts match the source; latest commit SHAs on main equal.
- [ ] `git lfs ls-files` on a fresh clone shows LFS pointers resolving.
- [ ] Source is read-only; pipelines and policies run against the new repo.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: TFVC import 180 days and 1 GB cap, 5 GB push and web-import rule, git-tfs for full history, az repos import create flags.

Removed because not confirmed: the gh ado2gh command lines (GitHub page unreadable beyond its outline), refs/pull rejection claim, submodule and author-mapping gotchas, and the dead migrate-from-tfvc-to-git source.

Method: documentation only; no commands were run.
