---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-secret-and-registry-extensions
name: woodpecker-secret-and-registry-extensions
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [secret-extension, registry-extension, vault]
level: sme
status: docs-checked
description: "Supply Woodpecker secrets and registry credentials from external services via extensions."
sources: ["https://woodpecker-ci.org/docs/usage/extensions/secret-extension", "https://woodpecker-ci.org/docs/usage/extensions/registry-extension"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker secret and registry extensions

Both extensions are HTTP endpoints configured per repository (extensions tab) or on the server.

Secret extension:

```ini
WOODPECKER_SECRET_EXTENSION_ENDPOINT=https://example.com/secrets
WOODPECKER_SECRET_EXTENSION_NETRC=false
```

Woodpecker POSTs `repo`, `pipeline` and optionally `netrc`. The extension answers with a `secrets` array of objects with `name`, `value`, and optional `images` and `events`. Extension secrets are merged with local ones and win by name; if the extension is unavailable, local secrets are used. A repository-level extension beats the global one. Respond `204 No Content` to keep the existing secrets without adding any.

Registry extension:

```ini
WOODPECKER_REGISTRY_EXTENSION_ENDPOINT=https://example.com/registries
```

The response contains `registries` with `address`, `username` and `password`. Woodpecker falls back to credentials configured directly in Woodpecker. If both the global and repo-level extension return credentials for a registry, the repo extension wins.

Both extensions receive `netrc` only when the matching `WOODPECKER_SECRET_EXTENSION_NETRC` or `WOODPECKER_REGISTRY_EXTENSION_NETRC` is true (default false) or the repository checks "Send netrc credentials". That data contains repository access credentials, so enable it only for trusted extensions. Woodpecker signs every request; secure the endpoint.

The secret extension suits centralised secret management such as HashiCorp Vault or AWS Secrets Manager.

## Checked

2026-11-08. Read the Woodpecker secret extension and registry extension pages in full (raw markdown). Confirmed endpoints, NETRC variables, request and response shapes, merge and fallback rules, 204 handling, repo-over-global precedence, request signing. Removed: the claim that secrets without events go to all events, which the pages do not state. Added the registry-extension page to sources.

Method: documentation only; no commands were run.
