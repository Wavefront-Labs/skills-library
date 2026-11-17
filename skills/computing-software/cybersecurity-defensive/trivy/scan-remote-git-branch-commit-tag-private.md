---
id: computing-software.cybersecurity-defensive.trivy.scan-remote-git-branch-commit-tag-private
name: scan-remote-git-branch-commit-tag-private
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [git-branch, git-commit, git-tag, github-token, gitlab-token, private-repository]
level: practitioner
status: docs-checked
description: "Scan a specific branch, commit or tag of a remote repository and authenticate to private GitHub or GitLab repositories with environment tokens."
sources:
  - https://trivy.dev/latest/docs/guide/target/repository/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags for remote git repositories, each used with `trivy repo`:

```
trivy repo --branch <branch-name> <repo-name>
trivy repo --commit <commit-hash> <repo-name>
trivy repo --tag <tag-name> <repo-name>
```

`--branch` takes a valid branch on the remote repository, `--commit` scans up to a valid commit hash, and `--tag` takes a valid tag.

To scan private GitHub or GitLab repositories, set the environment variable `GITHUB_TOKEN` or `GITLAB_TOKEN` respectively, with a valid token that has access to the repository. `GITHUB_TOKEN` takes precedence over `GITLAB_TOKEN`, so to scan a private GitLab repository `GITHUB_TOKEN` must be unset.

```
export GITHUB_TOKEN="your_private_github_token"
trivy repo <your private GitHub repo URL>

export GITLAB_TOKEN="your_private_gitlab_token"
trivy repo <your private GitLab repo URL>
```

Git metadata: for local and remote git repositories Trivy automatically extracts and includes metadata in scan results. It covers repository URL, branch name, tags, commit details (hash, message, committer) and author information. With `--format json` it appears in the `Metadata` field:

```bash
trivy repo --format json <repo-name>
```

Scan cache: for git repositories, Trivy stores analysis results in the cache keyed by the latest commit hash. The cache is not used when the repository is dirty, otherwise Trivy would miss files that are not committed.

## Checked

2026-11-03. Read and confirmed against the Code Repository page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
