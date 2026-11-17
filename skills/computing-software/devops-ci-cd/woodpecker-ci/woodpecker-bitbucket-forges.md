---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-bitbucket-forges
name: woodpecker-bitbucket-forges
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [bitbucket, oauth-consumer]
level: practitioner
status: docs-checked
description: "Connect Woodpecker to Bitbucket Cloud: OAuth consumer, permissions and known issues."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/forges/bitbucket"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker with Bitbucket

Bitbucket Cloud:

```ini
WOODPECKER_BITBUCKET=true
WOODPECKER_BITBUCKET_CLIENT=...   # called "Key" in Bitbucket
WOODPECKER_BITBUCKET_SECRET=...
```

Register an OAuth consumer in workspace settings under `OAuth consumers`, with `Callback URL` `https://<your-woodpecker-address>/authorize`. Required permissions: Account Email read, Workspace membership read, Projects read, Repositories read, Pull requests read, Webhooks read and write.

Known issues: build keys are limited to 40 characters; shorten them via `WOODPECKER_STATUS_CONTEXT` or `WOODPECKER_STATUS_CONTEXT_FORMAT`. Path filters for pull requests are not supported.

Bitbucket Datacenter is a separate forge in the forges feature matrix (no release or pull-request-metadata events). Its settings are not covered here; use the Woodpecker forge documentation for it.

Keep the client and secret out of Compose files with `WOODPECKER_BITBUCKET_CLIENT_FILE` and `WOODPECKER_BITBUCKET_SECRET_FILE`.

## Checked

2026-11-03. Read the Woodpecker Bitbucket forge page and forges overview and confirmed Bitbucket Cloud variables, OAuth consumer registration, required permissions, 40-character build key limit with STATUS_CONTEXT workaround, no pull-request path filters, and that Bitbucket Datacenter lacks release and pull-request-metadata events. Removed: the whole Bitbucket Datacenter configuration block (variables, service account and application link steps), which the cited page does not document. 

Method: documentation only; no commands were run.
