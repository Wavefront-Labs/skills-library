---
id: computing-software.devops-ci-cd.flux.git-commit-status-and-pr-comments
name: git-commit-status-and-pr-comments
category: computing-software
field: devops-ci-cd
product: flux
tags: [commit-status, pullrequestcomment, change-request, notification, github]
level: sme
status: docs-checked
description: "Report Kustomization results back to Git commits or pull requests with notification providers."
sources:
  - https://fluxcd.io/flux/components/notification/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
notification-controller can mark Git commits as reconciled by posting Kustomization events to the origin repository through the Git provider API.

Supported provider types for commit status: `github`, `gitlab`, `gitea`, `bitbucket`, `bitbucketserver`, `azuredevops`.

```yaml
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Provider
metadata:
  name: github-status
  namespace: flux-system
spec:
  type: github
  address: https://github.com/my-gh-org/my-gh-repo
  secretRef:
    name: github-token
---
apiVersion: notification.toolkit.fluxcd.io/v1
kind: Alert
metadata:
  name: github-status
  namespace: flux-system
spec:
  providerRef:
    name: github-status
  eventSources:
    - kind: Kustomization
      name: flux-system
```

Change request comments post status on a pull or merge request: types `githubpullrequestcomment`, `giteapullrequestcomment` and `gitlabmergerequestcomment`. Flux objects without the annotation `event.toolkit.fluxcd.io/change_request` (which carries the request number) are filtered out and trigger nothing. Each object gets at most one comment per provider on the request, updated on each new event. The GitHub comment provider supports the same authentication methods as the GitHub commit status provider (personal access token or GitHub App). The token needs permission to update commit status, or to read and write pull request comments.

## Checked

2026-11-08. Read the Flux notification Providers page sections on commit status types, change request comment types, the commit status example and the GitHub pull request comment provider. Provider and Alert apiVersion changed to `notification.toolkit.fluxcd.io/v1` as in the page example. Removed unsourced advice on when to use status versus comments, the troubleshooting hint, and the claim that comment authentication matches commit status for every host (the page states it for GitHub only; GitLab and Gitea sections were read only for the one-comment and annotation rules).

Method: documentation only; no commands were run.
