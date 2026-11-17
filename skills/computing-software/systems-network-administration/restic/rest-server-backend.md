---
id: computing-software.systems-network-administration.restic.rest-server-backend
name: rest-server-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, rest-server, rest, backend, https, cacert]
level: practitioner
status: docs-checked
description: "Point restic at a REST server repository with rest: URLs, credentials in RESTIC_REST_USERNAME and PASSWORD, and --cacert for private CAs."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST server backend

Repository URLs take the `rest:` prefix:

```
rest:http://host:8000/
rest:https://host:8000/
rest:https://user:pass@host:8000/
rest:https://user:pass@host:8000/my_backup_repo/
rest:http+unix:///tmp/rest.socket:/my_backup_repo/
```

The trailing path selects a repository on a server that hosts several. The server uses the same directory layout as the local backend.

## Credentials

The server username and password can also be given with environment variables instead of in the URL:

```
export RESTIC_REST_USERNAME=user
export RESTIC_REST_PASSWORD=...
restic -r rest:https://host:8000/my_backup_repo/ init
```

## Private or self-signed certificates

Pass the CA with `--cacert /path/to/ca.pem`. When this option is used, the system CA store is ignored, so the file must contain every CA you need. `--tls-client-cert` supplies a client certificate for mutual TLS.

## Transport details

The HTTP API the server implements is documented in the REST backend page (see the rest-api skill). For servers reachable only over a tunnel, see the SSH tunnel skill.

## Checked

2026-11-03. Confirmed in the restic docs pages Preparing a new repository (REST Server section), Scripting (`RESTIC_REST_USERNAME`, `RESTIC_REST_PASSWORD`) and the restic command reference (`--cacert`, `--tls-client-cert`): the five URL forms, same directory layout as the local backend, system CA store ignored when `--cacert` is used. Removed: the shell-history and process-list claim and the closing init paragraph (not in the docs).

Method: documentation only; no commands were run.
