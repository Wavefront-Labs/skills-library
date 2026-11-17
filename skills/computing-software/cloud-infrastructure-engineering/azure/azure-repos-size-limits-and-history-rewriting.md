---
id: computing-software.cloud-infrastructure-engineering.azure.azure-repos-size-limits-and-history-rewriting
name: azure-repos-size-limits-and-history-rewriting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-repos, repo-size, git-filter-repo, git-lfs, large-files]
level: advanced
status: docs-checked
description: "Keep Azure Repos Git repositories within size limits: find large blobs, move them to Git LFS, rewrite history with git-filter-repo, and force-push safely."
sources: ["https://learn.microsoft.com/azure/devops/repos/git/limits", "https://learn.microsoft.com/azure/devops/repos/git/manage-large-files", "https://github.com/newren/git-filter-repo", "https://learn.microsoft.com/azure/devops/repos/git/remove-binaries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Repos size limits and history rewriting

**Goal:** fix slow clones and push rejections caused by large files in history.

## Limits
- Repositories should be no larger than **250 GB**; Microsoft recommends staying below **10 GB** and using Git LFS, Scalar or Azure Artifacts beyond that.
- **Push size limit 5 GB** per push. Migrating a repo from another service is the exception, but a repo over 5 GB must be imported through the web, not the command line.
- Git LFS blobs don't count towards the 5 GB limit; list the extensions in `.gitattributes` and stage it before staging the large files.

## Find the culprits
```bash
git count-objects -vH
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3 > 10485760' | sort -k3 -n -r | head -20
git filter-repo --analyze        # report in .git/filter-repo/analysis
```

## Rewrite
```bash
git clone --mirror https://dev.azure.com/org/proj/_git/repo repo.git && cd repo.git
git filter-repo --strip-blobs-bigger-than 50M            # or --path big/dir --invert-paths
# or move to LFS instead of deleting:
git lfs migrate import --everything --include="*.psd,*.zip"
git push --force --mirror origin
```
- Requires **Force push** (preferred) or Admin permission on the repository (temporarily grant).
- Coordinate: everyone must re-clone (old clones will reintroduce the blobs on push). Freeze merges during the rewrite. Open PRs will need re-creating.

## Prevent
- `.gitattributes` with LFS tracking for binaries; pre-commit hooks for large files.
- Artifacts belong in Azure Artifacts or pipeline artifacts, not Git.

## Verify
- [ ] Fresh clone size reduced (`du -sh .git`); large-blob query returns nothing above the threshold.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: 250 GB repository size, 10 GB recommendation, 5 GB push limit, web import over 5 GB, LFS exemption, Force push or Admin permission for rewriting history.

Removed because not confirmed: the named repository policies, bypass permission claim, and garbage-collection timing.

Method: documentation only; no commands were run.
