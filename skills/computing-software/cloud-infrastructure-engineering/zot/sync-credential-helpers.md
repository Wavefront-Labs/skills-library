---
id: computing-software.cloud-infrastructure-engineering.zot.sync-credential-helpers
name: sync-credential-helpers
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, credential-helper, aws-ecr, gcp-registry, oauth2-credential-helper, sync-auth]
level: advanced
status: docs-checked
description: "Authenticate Zot sync to AWS ECR, Google registries or token endpoints using credentialHelper ecr, gcp or oauth2 with the oauth2CredentialHelper block."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `credentialHelper` on a sync registry entry instead of a static credentials file.

- AWS ECR: `credentialHelper: "ecr"` with `credentialsFile: ""`, on-demand, `maxRetries: 5` in the docs example. The example writes `DownloadDir` with different casing from the `downloadDir` key described elsewhere; check your version.
- Google: `credentialHelper: "gcp"`, on-demand. Uses Application Default Credentials; the principal needs read access such as `roles/artifactregistry.reader`. Works with GCR hosts accepting Google tokens.
- OAuth2: `credentialHelper: "oauth2"` plus an `oauth2CredentialHelper` block. Exactly one of `assertionFile` or `signingFile` is required.

`oauth2CredentialHelper` attributes:
- `tokenURL`: required.
- `assertionFile`: pre-signed assertion, re-read on each refresh; exclusive with `signingFile`.
- `signingFile`: JSON with `privateKeyFile` and `algorithm`, optional `keyId`, `issuer`, `subject`, `audience` (issuer and subject default to `clientID`, audience to `tokenURL`).
- `grantType`: default `client_credentials`; also `jwt-bearer` and `token-exchange`.
- `clientID`, `clientSecretFile`, `scopes` (sent space-separated): optional.
- `username`: default `<token>`; the example uses `oauth2accesstoken`.
- Token exchange: `audience` required (rejected for other grants), `subjectTokenType` default `urn:ietf:params:oauth:token-type:jwt`, `requestedTokenType` default `urn:ietf:params:oauth:token-type:access_token`.

## Checked

2026-11-08. Read in full: docs/articles/mirroring.md and compared every claim above against it.

Method: documentation only; no commands were run.
