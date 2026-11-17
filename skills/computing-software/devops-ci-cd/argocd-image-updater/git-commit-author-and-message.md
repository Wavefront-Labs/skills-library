---
id: computing-software.devops-ci-cd.argocd-image-updater.git-commit-author-and-message
name: git-commit-author-and-message
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, commit-message, commit-template, git-commit-user, git-commit-email, template-command, oci-labels]
level: practitioner
status: docs-checked
description: "Customise git write-back commits: author name and email via flags or ConfigMap, a commit-message-template with AppName and AppChanges, OCI labels, and the template test command."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Commit author and commit message

Author. Default `argocd-image-updater <noreply@argoproj.io>`. Override with `--git-commit-user` and `--git-commit-email` (envs `GIT_COMMIT_USER`, `GIT_COMMIT_EMAIL`) or the ConfigMap keys `git.user` and `git.email`. `--git-commit-message-path` points to a template file (default `/app/config/commit.template`).

Message. Set `git.commit-message-template` in `argocd-image-updater-config` (Go `text/template`):

```yaml
data:
  git.commit-message-template: |
    build: automatic update of {{ .AppName }}

    {{ range .AppChanges -}}
    updates image {{ .Image }} tag '{{ .OldTag }}' to '{{ .NewTag }}'
    {{ end -}}
```

Top-level variables: `.AppName`; `.AppChanges` with `.Image`, `.OldTag`, `.NewTag` and `.Labels` (a map of the image's OCI labels, empty if none).

Labels let you add upstream details, for example `index .Labels "org.opencontainers.image.source"` and `...revision` to print `{{ $source }}/commit/{{ $revision }}` (GitLab uses `/-/commit/`, Bitbucket `/commits/`). That assumes the source label is a clean repo URL and the revision label was set at build time.

Test a template first: save it to a temporary file and run `argocd-image-updater template /path/to/file` to render it with sample data.

In pull request mode the first line becomes the PR title.

## Checked

2026-11-04. Confirmed against update-methods.md (author default and git.user / git.email, git.commit-message-template, template variables, OCI label example, provider URL variants, the template command, PR title from the first line) and the run command page (--git-commit-user, --git-commit-email, --git-commit-message-path default).

Method: documentation only; no commands were run.
