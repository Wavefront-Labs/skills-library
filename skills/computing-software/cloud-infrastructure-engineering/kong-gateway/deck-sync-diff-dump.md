---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.deck-sync-diff-dump
name: deck-sync-diff-dump
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, deck, deck-sync, deck-diff, declarative, apiops]
level: practitioner
status: docs-checked
description: "Manage Kong Gateway declaratively with decK: gateway dump, diff, sync, ping and validate, the --kong-addr flag, openapi2kong and merge, and the one-process rule."
sources:
  - https://developer.konghq.com/deck/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# decK sync, diff and dump

decK manages Kong configuration from YAML or JSON state files through the Admin API.

```bash
deck gateway ping
deck gateway dump -o kong.yaml
deck gateway diff kong.yaml
deck gateway sync kong.yaml
deck gateway validate
```

- `dump` exports current configuration to a file.
- `diff` compares a state file with the running gateway.
- `sync` applies the file.
- `ping` checks the connection.

File commands:

```bash
deck file openapi2kong -s oas.yaml -o httpbin.yaml
deck file merge httpbin.yaml another-httpbin.yaml -o merged-kong.yaml
```

Flags and variables:
- `--kong-addr` (or `DECK_KONG_ADDR`): the Admin API address, for example `http://host.docker.internal:8001` when running decK in Docker.
- `--konnect-control-plane-name`: target a Konnect control plane.
- `--verbose 1`: print every Admin API query.
- `--parallelism 1`: one request at a time; a last resort for Cassandra-backed setups because it slows syncs.

Run only one decK process at a time; two processes will step on each other and might corrupt the configuration.

decK needs a database, so it cannot be used against DB-less nodes.

## Checked

2026-11-04. Confirmed against the decK page: the gateway dump, diff, sync, ping and validate commands, `deck file openapi2kong` and `merge`, `--kong-addr`/`DECK_KONG_ADDR` with host.docker.internal, `--konnect-control-plane-name`, `--verbose 1`, `--parallelism 1`, one-process warning, DB-less limitation. Removed the state-file `_format_version` line (not on this page) and softened the corruption wording.
Method: documentation only; no commands were run.
