---
id: computing-software.cloud-infrastructure-engineering.openbao.dev-server
name: dev-server
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, dev-mode, dev-server, in-memory, dev-kv-v1]
level: intro
status: docs-checked
description: "What bao server -dev gives you (in-memory, unsealed, no TLS, KV v2 at secret/) and why it must never reach production."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/dev-server.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dev server

```
bao server -dev
bao server -dev -dev-kv-v1
```

`-dev-kv-v1` mounts KV v1 at `secret/` instead of the default v2.

## Defaults

- Already initialized and unsealed; no `bao operator unseal` needed.
- In-memory storage: data is encrypted but held in memory, so no file permissions are needed.
- Listens on `127.0.0.1:8200` without TLS.
- Your root token is stored automatically so the `bao` CLI works at once; API users must authenticate with the printed token.
- A single unseal key, enough to practise seal and unseal.
- KV v2 mounted at `secret/`.

Some dev properties can be overridden by flags or a config file.

## Good for

Trying auth methods, secrets engines and audit devices; automating development environments.

## Warning

The docs are emphatic: never run a dev-mode server in production. `-dev` short-circuits setup to insecure defaults, and all data is lost on restart.

## Checked

2026-11-04. Confirmed against the Dev server page: bao server -dev and -dev-kv-v1, initialized and unsealed, in-memory storage, 127.0.0.1:8200 without TLS, stored root token, single unseal key, KV v2 at secret/, and the production warning. Nothing removed.

Method: documentation only; no commands were run.
