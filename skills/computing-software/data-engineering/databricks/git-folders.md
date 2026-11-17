---
id: computing-software.data-engineering.databricks.git-folders
name: git-folders
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, git-folders, databricks-repos, git-integration, sparse-checkout, notebooks-as-source, git-credentials]
level: practitioner
status: docs-checked
description: "Use Databricks Git folders (formerly Repos): link credentials, branch and commit from the workspace, notebook source formats, sparse checkout and when to use bundles instead."
sources:
  - https://docs.databricks.com/aws/en/repos/
  - https://docs.databricks.com/aws/en/repos/git-operations-with-repos
  - https://docs.databricks.com/aws/en/repos/limits
  - https://docs.databricks.com/aws/en/repos/ci-cd-techniques-with-repos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databricks Git folders

**Goal:** develop notebooks and Python modules in the workspace with real Git history, without Git folders becoming the deployment mechanism for prod.

## 1. Connect
- User settings > Linked accounts > add Git provider (GitHub app/OAuth recommended over PAT). For GitHub, install the Databricks GitHub App on the repos you need.
- Create: Workspace > Create > Git folder > repo URL. It lands in `/Workspace/Users/<you>/<repo>`.
- Private Git servers behind a firewall need Git server proxy (or allowlisting Databricks egress IPs).

## 2. Daily operations (Git dialog)
- Pull, create branch, commit & push, merge, rebase, resolve conflicts, reset — all from the Git dialog. Work on a branch per person; never commit to `main` from the workspace.
- Notebooks are stored as source files: `.py` source files with a notebook header comment by default; `.ipynb` is supported (set default format in settings). Outputs are not committed unless you choose `.ipynb` with outputs enabled — keep them off to avoid leaking data into Git.
- Files in the folder are importable: `from mypkg.transforms import clean` works because the Git folder root is on `sys.path` for notebooks in it.
- `.gitignore` is honoured. Sparse checkout (cone patterns) set at clone time limits large monorepos.

## 3. Limits to know
- Size limits per repo/working tree and per file apply (see the limits page); very large repos need sparse checkout.
- Changing a notebook's language or moving it out of the Git folder loses the link to history.
- Git folders do not create jobs, clusters or permissions; that is what Asset Bundles do.

## 4. Production pattern
- Old pattern: a "prod" Git folder updated by CI through the Repos API/CLI and jobs pointing at it. Works, but job definitions still live outside Git.
- Preferred: jobs reference code via `git_source` (job pulls the commit at run time) or — better — deploy with Asset Bundles from CI, which ships both code and job definitions.
With a job-level Git source, task notebook paths are relative to the repo root; pin a tag or commit for reproducible prod runs (field names: see the Jobs API reference).

## Verify
- [ ] Each developer works in their own Git folder on a feature branch.
- [ ] Committed notebooks contain no cell outputs.
- [ ] Prod jobs run from a bundle deploy or a pinned `git_source`, never from someone's user folder.

## Checked

2026-10-28. Confirmed: sparse checkout with cone patterns on the Git operations page. Removed: an unconfirmed CLI command, JSON field names and a header string.

Method: documentation only; no commands were run.
