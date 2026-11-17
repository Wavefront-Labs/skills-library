---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-gitlab-forge
name: woodpecker-gitlab-forge
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [gitlab, oauth-application, groups]
level: practitioner
status: docs-checked
description: "Connect Woodpecker to GitLab and handle group matching and outbound request settings."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/forges/gitlab"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker with GitLab

Built-in support covers GitLab 12.4 and higher.

```ini
WOODPECKER_GITLAB=true
WOODPECKER_GITLAB_URL=http://gitlab.mycompany.com
WOODPECKER_GITLAB_CLIENT=95c0282573633eb25e82
WOODPECKER_GITLAB_SECRET=30f5064039e6b359e075
```

Registration: in your GitLab account settings, choose Applications, then New Application. Use `http://woodpecker.mycompany.com/authorize` as the callback URL and grant the `api` scope.

If Woodpecker runs on a private IP (RFC1918) or you use a non-standard TLD such as `.local` or `.intern`, allow local connections in GitLab under the admin dashboard, `Settings > Network > Outbound requests`; otherwise API requests fail.

Allowed organizations: when restricting login with `WOODPECKER_ORGS` or a forge's allowed organizations, GitLab groups are matched by `full_path`, not by name. For a subgroup use the complete path.

Only groups where the user has at least the Developer role are considered. Guest or Reporter users are denied even if the group is listed.

Options: `WOODPECKER_GITLAB_URL` defaults to `https://gitlab.com`; `WOODPECKER_GITLAB_SKIP_VERIFY` (false); `_FILE` variants exist for client and secret.

`CI_COMMIT_PULL_REQUEST_DRAFT` uses GitLab's `draft` field and falls back to the legacy `work_in_progress` when needed.

## Checked

2026-11-03. Read the Woodpecker GitLab forge page and confirmed the WOODPECKER_GITLAB_* variables and registration steps. Nothing removed. 

Method: documentation only; no commands were run.
