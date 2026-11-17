---
id: computing-software.devops-ci-cd.argocd-image-updater.git-pull-request-providers
name: git-pull-request-providers
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, pull-request, github, gitlab, azure-devops, gitea, forgejo, pr-labels]
level: advanced
status: docs-checked
description: "Configure pull or merge requests for GitHub, GitLab, Azure DevOps and Gitea or Forgejo with pullRequest.github, gitlab, azuredevops or gitea, plus labels and token scopes."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/examples/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pull request providers and labels

Exactly one of `github`, `gitlab`, `azuredevops` or `gitea` must be set under `gitConfig.pullRequest`. Each takes an empty object (`{}`); URL, branch and credentials come from the enclosing config.

```yaml
writeBackConfig:
  method: "git:secret:git-creds"
  gitConfig:
    repository: "https://github.com/example/example.git"
    branch: "main"
    pullRequest:
      github: {}
      labels: [image-update, automated]
```

- GitHub: github.com and Enterprise Server; the API base URL is derived from the repo URL.
- GitLab: `gitlab: {}` for gitlab.com or self-managed; labels are set in the creating call and missing labels are created.
- Azure DevOps: `azuredevops: {}`; repository URL must be HTTPS (dev.azure.com, visualstudio.com, Server 2022.1+); HTTPS secret with a PAT in `password` needing Code (Read & write).
- Gitea and Forgejo: `gitea: {}`; HTTP or HTTPS (plain HTTP intended for in-cluster URLs); token scopes `write:repository`, plus `write:issue` for labels.

`pullRequest.labels` (max 100, duplicates and empties ignored) applies to all providers. GitHub, Gitea and Azure DevOps apply labels in follow-up calls; a failure logs a warning and the update still counts as successful. Gitea label-by-name needs Gitea 1.22 or Forgejo 8 or newer.

## Checked

2026-11-04. Confirmed against update-methods.md (PR labels behaviour per provider, GitHub, GitLab, Azure DevOps and Gitea sections, token scopes) and images.md (pullRequest field table: exactly one provider, empty provider objects, labels max 100).

Method: documentation only; no commands were run.
