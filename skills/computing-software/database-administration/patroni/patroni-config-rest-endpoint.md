---
id: computing-software.database-administration.patroni.patroni-config-rest-endpoint
name: patroni-config-rest-endpoint
category: computing-software
field: database-administration
product: patroni
tags: [patroni, rest-api, dynamic-config, patch, config]
level: practitioner
status: docs-checked
description: "GET, PATCH and PUT /config to read and change dynamic configuration, including removing keys with null."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage cluster configuration over HTTP.

- `GET /config` returns the current dynamic configuration.
- `PATCH /config` merges changes into it and returns the new configuration:

```
curl -s -XPATCH -d '{"loop_wait":5,"ttl":20,"postgresql":{"parameters":{"max_connections":"101"}}}' http://localhost:8008/config
```

A change such as `max_connections` requires restart, so `pending_restart` appears in `GET /patroni` output. The nodes begin applying `loop_wait` on the next cycle.

- Remove a setting by patching it with null:

```
curl -s -XPATCH -d '{"postgresql":{"parameters":{"max_connections":null}}}' http://localhost:8008/config
```

- `PUT /config` is an unconditional full rewrite of the dynamic configuration.

Other uses: patch `{"pause": true}` / `false` / `null` to enter or leave pause mode, and `failsafe_mode` can be enabled through PATCH.

Unsafe methods (PATCH, PUT) are subject to basic-auth, allowlist and client-certificate settings.

CLI equivalents: `patronictl show-config`, and `patronictl edit-config` with `-s CONFIG="VALUE"` (dot-separated path; null removes it), `-p PG_PARAM="VALUE"` (shorthand for `postgresql.parameters.` prefix), `--apply FILE` (merge, `-` reads stdin), `--replace FILE` (full replace), `-q` to skip the diff, and `--force` to skip prompts. With a TTY it shows a diff via a pager (`less` or `more`, or `PAGER`).

## Checked

2026-11-03. Confirmed against the REST API page (`GET`/`PATCH`/`PUT /config`, null removal, `pending_restart`), the Pause page (`pause` key) and the patronictl edit-config synopsis (`-s`, `-p`, `--apply`, `--replace`, `-q`, `--force`, pager).

Method: documentation only; no commands were run.
