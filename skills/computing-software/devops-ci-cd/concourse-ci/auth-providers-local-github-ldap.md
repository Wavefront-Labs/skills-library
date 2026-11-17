---
id: computing-software.devops-ci-cd.concourse-ci.auth-providers-local-github-ldap
name: auth-providers-local-github-ldap
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [auth, local-user, github, ldap, bcrypt, oauth, main-team]
level: practitioner
status: docs-checked
description: "Configure local user, GitHub and LDAP auth on the web node, with the matching set-team flags, roles config keys and CONCOURSE_MAIN_TEAM_* variables for each provider."
sources:
  - https://concourse-ci.org/docs/auth-and-teams/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each provider has an authentication half (env on the `web` node) and an authorization half (`fly set-team` flags or `roles` config).

**Local user.** Set `CONCOURSE_ADD_LOCAL_USER=myuser:mypass,anotheruser:anotherpass`; a bcrypt hash can replace the literal password (the docs example puts the hashed value in single quotes). Log in with `fly login --username --password`. Authorize with `--local-user some_username` or `local: users:` in roles. For main: `CONCOURSE_MAIN_TEAM_LOCAL_USER=myuser`. The docs recommend another provider except for small deployments.

**GitHub.** Create an OAuth application whose callback URL is the Concourse URL plus `/sky/issuer/callback`, reachable by GitHub, then set `CONCOURSE_GITHUB_CLIENT_ID` and `CONCOURSE_GITHUB_CLIENT_SECRET`. Org and team authorization needs the app created under an organization with read access to its members; a personal-account app can authorize only individual users. GitHub Enterprise adds `CONCOURSE_GITHUB_HOST` (no scheme or trailing slash) and `CONCOURSE_GITHUB_CA_CERT`. Flags: `--github-user`, `--github-org`, `--github-team ORG:TEAM`; roles keys `users`, `orgs`, `teams`. Main: `CONCOURSE_MAIN_TEAM_GITHUB_ORG`, `_TEAM`, `_USER`.

**LDAP.** Point at `CONCOURSE_LDAP_HOST` with a read-only `CONCOURSE_LDAP_BIND_DN` and `CONCOURSE_LDAP_BIND_PW`, plus `CONCOURSE_LDAP_USER_SEARCH_BASE_DN` and `CONCOURSE_LDAP_USER_SEARCH_USERNAME`. Use `CONCOURSE_LDAP_CA_CERT` for TLS or `CONCOURSE_LDAP_INSECURE_NO_SSL=true` without it. Group search uses `CONCOURSE_LDAP_GROUP_SEARCH_*` variables. Flags: `--ldap-user`, `--ldap-group`. Main: `CONCOURSE_MAIN_TEAM_LDAP_USER` and `_GROUP`.

Multiple main-team values are comma-separated.

## Checked

2026-11-04. Variables, flags and role keys confirmed on the Local User, GitHub and LDAP auth pages. The OIDC, UAA and other providers were not read.

Method: documentation only; no commands were run.
