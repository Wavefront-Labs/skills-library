---
id: computing-software.devops-ci-cd.concourse-ci.idtoken-var-source
name: idtoken-var-source
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [idtoken, jwt, oidc, identity-federation, var-source, subject-scope, jwks, key-rotation]
level: advanced
status: docs-checked
description: "Use the idtoken var source to mint Concourse-signed JWTs: audience, subject_scope values, JWKS and discovery endpoints, claims, and signing key rotation settings."
sources:
  - https://concourse-ci.org/docs/operation/creds/id-token/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The idtoken credential manager loads nothing from outside; it generates JWTs signed by Concourse that carry the identity of the running pipeline and job, so a pipeline can authenticate through identity federation to services such as Vault, AWS or Azure. It cannot be a cluster-wide manager, only a var source. Verifiers use the public keys published as JWKS at `/.well-known/jwks.json`, and Concourse also serves an OIDC discovery endpoint.

```yaml
var_sources:
  - name: myidtoken
    type: idtoken
    config:
      audience: [ "sts.amazonaws.com" ]
```

The source exposes one var with the field `token`, used as `((myidtoken:token))`. Several idtoken sources with different audiences or lifetimes may coexist in a pipeline.

`subject_scope` sets how specific the `sub` claim is: `team` gives `<team_name>`; `pipeline` gives `<team_name>/<pipeline_name>`; `instance` appends instance vars as comma-separated pairs; `job` adds the job name, with empty elements kept (`my-team/my-pipeline//my-job`). Services like AWS match `sub` exactly, so `team` lets all of a team's pipelines assume one role.

Claims: `iss` (the `--oidc-issuer-url` if set, otherwise the external URL), `exp`, `aud`, `team`, `pipeline`, `job`, `instance_vars`, `sub`.

Key rotation flags on the ATC: `CONCOURSE_SIGNING_KEY_ROTATION_PERIOD` (default `7d`, `0` disables), `CONCOURSE_SIGNING_KEY_GRACE_PERIOD` (default `24h`, how long old keys stay published) and `CONCOURSE_SIGNING_KEY_CHECK_INTERVAL` (default `10m`).

## Checked

2026-11-04. Usage, subject scope table, claims and rotation flags confirmed on the IDToken credential manager page.

Method: documentation only; no commands were run.
