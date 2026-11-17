---
id: computing-software.devops-ci-cd.concourse-ci.credhub-credential-manager
name: credhub-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [credhub, credential-manager, mtls, tls, lookup-paths, shared-path, cloud-foundry]
level: practitioner
status: docs-checked
description: "Configure CredHub as the credential manager: URL with client id and secret, CA cert, mTLS client cert and key, lookup order, typed credential fields, shared path and path prefix."
sources:
  - https://concourse-ci.org/docs/operation/creds/credhub/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable with these web node variables:

```properties
CONCOURSE_CREDHUB_URL=https://credhub-server:9000
CONCOURSE_CREDHUB_CLIENT_ID=...
CONCOURSE_CREDHUB_CLIENT_SECRET=...
```

For a local CA use `CONCOURSE_CREDHUB_CA_CERT`. `CONCOURSE_CREDHUB_INSECURE_SKIP_VERIFY=true` exists but must not be used in production. For mutual TLS instead of password or token auth, set `CONCOURSE_CREDHUB_URL`, `CONCOURSE_CREDHUB_CA_CERT`, `CONCOURSE_CREDHUB_CLIENT_CERT` and `CONCOURSE_CREDHUB_CLIENT_KEY`.

**Lookup.** `((foo_param))` is searched at `/concourse/TEAM_NAME/PIPELINE_NAME/foo_param`, then `/concourse/TEAM_NAME/foo_param`. The ATC tries the pipeline path first when running in pipeline context (a check or a job build) and falls back to the team path, so common credentials can be scoped widely. A one-off task has no pipeline, so only the team path is searched.

CredHub credentials have types with several values; the `user` type has `username` and `password`. Select a field with dot syntax: `((foo_param.username))`.

**Customising:**
- `CONCOURSE_CREDHUB_SHARED_PATH=some-shared-path` for credentials common to all teams and pipelines, located under the prefix (`/concourse/some-shared-path` by default). Use with care.
- `CONCOURSE_CREDHUB_PATH_PREFIX=/some-other-prefix` replaces the leading `/concourse`.

## Checked

2026-11-04. Variables, lookup rules and customisation confirmed on the CredHub credential manager page.

Method: documentation only; no commands were run.
