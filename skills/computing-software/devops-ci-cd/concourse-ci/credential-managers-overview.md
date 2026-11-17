---
id: computing-software.devops-ci-cd.concourse-ci.credential-managers-overview
name: credential-managers-overview
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [credentials, credential-manager, vars, vault, credhub, kubernetes, aws, conjur, idtoken]
level: intro
status: docs-checked
description: "Choose a Concourse credential manager: what it replaces, what config it can parameterise, and seven backends (Vault, CredHub, Kubernetes, SSM, Secrets Manager, Conjur, IDToken)."
sources:
  - https://concourse-ci.org/docs/operation/creds/
  - https://concourse-ci.org/docs/operation/creds/id-token/
  - https://concourse-ci.org/docs/operation/creds/credhub/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Credential management goes beyond database encryption. Credentials are provided to builds for a short time without being persisted, can be rotated and managed outside the pipeline or team, and are not revealed by `fly get-pipeline`.

You replace credentials with `((vars))` in pipeline or task config. When Concourse is about to run a step or `check` that has vars, it resolves them by fetching from the credential manager. If a value is missing, the action errors.

Parameterisable config: `resource.source`, `resource_type.source`, `resource.webhook_token`, task step `params`, and tasks in their entirety (from `file`, step `config`, or `fly execute`).

Supported backends, each with its own page: AWS Secrets Manager, AWS SSM, Conjur, CredHub, IDToken, Kubernetes and Vault. All but IDToken are configured with environment variables on the `web` node and act as a cluster-wide manager. IDToken is different: it does not load credentials but generates signed JWTs, and can only be used as a var source.

Common behaviours handled elsewhere: lookups are tried team-and-pipeline scoped first, then team scoped; one-off tasks have no pipeline so only the team path is searched. Caching, retries and redaction are configured generally and covered in their own skills.

Where the pipeline needs a different backend than the cluster default, use a pipeline `var_sources` entry instead. See the var source skill.

## Checked

2026-11-04. Backend list, parameterisable configs and behaviour confirmed on the Credential Management page and the backend pages.

Method: documentation only; no commands were run.
