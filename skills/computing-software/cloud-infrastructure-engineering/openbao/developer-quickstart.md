---
id: computing-software.cloud-infrastructure-engineering.openbao.developer-quickstart
name: developer-quickstart
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, developer, kv, bao-addr, bao-token-path]
level: intro
status: docs-checked
description: "Developer quickstart against a dev-mode OpenBao: BAO_ADDR, BAO_TOKEN_PATH, bao login, kv put/get and the same read over curl."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/get-started/developer-qs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Developer quickstart

```
bao server -dev -dev-root-token-id="example-tutorial-token"
export BAO_ADDR=http://127.0.0.1:8200/
export BAO_TOKEN_PATH=/tmp/token-for-developer-quickstart
bao login
bao kv enable-versioning secret/
bao kv put -mount=secret developer-quickstart password=-
bao kv get -mount=secret -field=password developer-quickstart
bao kv get -mount=secret -format=yaml developer-quickstart
```

`password=-` makes the CLI read the value from stdin instead of putting it on the command line.

## Same read over HTTP

```
curl \
    --header "X-Vault-Token: $( cat "${BAO_TOKEN_PATH}" )" \
    --header "Accept: application/json" \
    http://127.0.0.1:8200/v1/secret/data/developer-quickstart
```

## Warnings

- The in-memory dev server is insecure, not durable, and must never protect real secrets or run in production.
- The root token allows full access; a real cluster rotates it after setup and adds more controls.
- Hard-coding a token in source (as the Go example does) is insecure; real code should authenticate the client some other way.

## Checked

2026-11-04. Confirmed against the Developer quick start page: the dev server command with -dev-root-token-id, BAO_ADDR and BAO_TOKEN_PATH, bao login, kv enable-versioning, kv put with password=-, kv get with -field and -format=yaml, the curl read and the three warnings. Nothing removed.

Method: documentation only; no commands were run.
