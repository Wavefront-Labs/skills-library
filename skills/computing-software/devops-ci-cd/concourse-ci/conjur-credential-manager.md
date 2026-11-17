---
id: computing-software.devops-ci-cd.concourse-ci.conjur-credential-manager
name: conjur-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [conjur, cyberark, credential-manager, policy, token-file, secret-templates, lookup]
level: practitioner
status: docs-checked
description: "Set up CyberArk Conjur as the credential manager: appliance URL, account, login and API key or token file, CA cert, a host policy example, and the three secret path templates."
sources:
  - https://concourse-ci.org/docs/operation/creds/conjur/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable with web node variables `CONCOURSE_CONJUR_APPLIANCE_URL`, `CONCOURSE_CONJUR_ACCOUNT`, `CONCOURSE_CONJUR_AUTHN_LOGIN` and `CONCOURSE_CONJUR_AUTHN_API_KEY`. Alternatively use `CONCOURSE_CONJUR_AUTHN_TOKEN_FILE` instead of login and key. For a locally signed CA, `CONCOURSE_CONJUR_CERT_FILE`.

**Permissions.** The page's example policy defines `!host concourse` and a `concourse` policy it owns, containing a policy per `TEAM_NAME` with a team variable and a nested `PIPELINE_NAME` policy with a pipeline variable. With that, `host/concourse` can read and update all secrets under those policies. Replace TEAM_NAME and PIPELINE_NAME to match your setup.

**Lookup.** `((foo_param))` is searched at `/concourse/TEAM_NAME/PIPELINE_NAME/foo_param`, then `/concourse/TEAM_NAME/foo_param`; pipeline context first, one-off tasks only the team path.

**Templates.** Three variables control the paths:

```properties
CONCOURSE_CONJUR_TEAM_SECRET_TEMPLATE
CONCOURSE_CONJUR_PIPELINE_SECRET_TEMPLATE
CONCOURSE_CONJUR_SECRET_TEMPLATE
```

with `{{.Team}}`, `{{.Pipeline}}` and `{{.Secret}}`. Setting them to `{{.Team}}/concourse/{{.Secret}}`, `/{{.Team}}/concourse/{{.Pipeline}}/{{.Secret}}` and `conjur/{{.Secret}}`, `((password))` in team `myteam` and pipeline `mypipeline` is looked up at `/myteam/concourse/mypipeline/password`, `/myteam/concourse/password`, then `/conjur/password`.

## Checked

2026-11-04. Variables, policy and template example confirmed on the Conjur credential manager page.

Method: documentation only; no commands were run.
