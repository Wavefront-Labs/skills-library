---
id: computing-software.devops-ci-cd.gitea.actions-openid-connect
name: actions-openid-connect
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-oidc, gitea, oidc-token, id-token-request, oidc-sub-claim, cloud-federation, jwt-signing-key]
level: advanced
status: docs-checked
description: "Use short-lived OIDC tokens from Gitea Actions to sign in to clouds: issuer and audience, id-token permission, token request URL, sub claim format and GitHub differences."
sources: ["https://docs.gitea.com/next/usage/actions/openid-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenID Connect from Gitea Actions

Jobs can request short-lived OIDC tokens instead of storing long-lived secrets. Tokens use GitHub's format, so `aws-actions/configure-aws-credentials`, `google-github-actions/auth` and `azure/login` work unchanged. The official page is in the docs of the next (in-development) Gitea version, so confirm your release has the feature.

## Trust setup at the service
- Issuer: `<ROOT_URL>/api/actions/oidc`
- Audience: `<ROOT_URL>/<owner>` unless the workflow asks for another
- Restrict with a condition on the `sub` claim.
Discovery document: `<ROOT_URL>/api/actions/oidc/.well-known/openid-configuration`. Gitea signs with a key it creates at `<APP_DATA_PATH>/jwt/actions_oidc.pem`; instances behind a load balancer must share this file.

## Requesting
```yaml
permissions:
  id-token: write
```
Default permissions never include it, fork pull request jobs never get it, and owner or repository maximums can disable it (see `gitea-actions-token-permissions`). Actions request tokens themselves. In scripts use the injected variables:
```shell
curl --fail --silent --show-error \
  --header "Authorization: Bearer ${ACTIONS_ID_TOKEN_REQUEST_TOKEN}" \
  "${ACTIONS_ID_TOKEN_REQUEST_URL}&audience=my-service"
```
The token is in the response field `value` and expires after five minutes.

## Claims
`sub` embeds owner and repository IDs, so a renamed or recreated repository cannot match an old trust policy:
- `repo:<owner>@<owner-id>/<repo>@<repo-id>:ref:<ref>` for all events except pull_request (including `pull_request_target`)
- `repo:<owner>@<owner-id>/<repo>@<repo-id>:pull_request` for the `pull_request` event
Other claims match GitHub (`repository`, `ref`, `sha`, `workflow_ref`, `job_workflow_ref`).

## Differences from GitHub
No `environment` claim; pull request runs use `refs/pull/<index>/head` and its commit rather than the merge ref; `run_number` counts per repository, not per workflow.

## Checked

2026-11-03: read https://docs.gitea.com/next/usage/actions/openid-connect line by line; the commands, options, defaults and values stated above match those pages.
Changed: Added a note that the page exists only in the next (in-development) docs version.
Method: documentation only; no commands were run.
