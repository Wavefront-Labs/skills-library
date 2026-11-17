---
id: computing-software.devops-ci-cd.dagger.engine-config-cache-gc
name: engine-config-cache-gc
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, engine, engine-json, cache, garbage-collection, registry-mirror, configuration]
level: practitioner
status: docs-checked
description: "Configure the Dagger Engine via engine.json or engine.toml (logging, security, GC, registry mirrors) and inspect, prune or tune the cache."
sources: [https://docs.dagger.io/0.21/reference/configuration/engine, https://docs.dagger.io/0.21/reference/configuration/cache]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger Engine configuration and cache management

Goal: change engine settings, control disk use, and inspect or prune the cache. Dagger 0.21 docs.

## Where config lives

- `engine.json` (schema at docs.dagger.io/reference/engine.schema.json): for an auto-provisioned engine write `~/.config/dagger/engine.json` (or `$XDG_CONFIG_HOME/dagger/engine.json`). A running engine does not pick up changes; remove it so it restarts: `docker rm -f $(docker ps -q --filter "name=dagger-engine-*")`.
- Custom runner: mount it, e.g. `-v $HOME/.config/dagger/engine.json:/etc/dagger/engine.json` (add `--privileged -v /var/lib/dagger` and the `registry.dagger.io/engine:v<version>` image).
- Legacy `engine.toml` (BuildKit syntax): only with a custom runner, mounted at `/etc/dagger/engine.toml`. If both set an option, `engine.json` wins; some options only exist in the toml.

## Settings (engine.json form)

- Log level: `{"logLevel": "error"}`; levels `error`, `warn`, `info`, `debug` (default), `debugextra`, `trace`. Toml: `debug = true|false`, `trace = true|false`.
- Security: `{"security": {"insecureRootCapabilities": false}}` locks down the default open policy. Toml: `insecure-entitlements = []`. Rootless engine is not currently supported.
- GC off: `{"gc": {"enabled": false}}` (toml `[worker.oci] gc = false`).
- GC tuning: `{"gc": {"maxUsedSpace": "200GB", "reservedSpace": "10GB", "minFreeSpace": "20%", "sweepSize": "50%"}}`. Values are bytes, unit strings, or percentages of disk. `sweepSize` is engine.json only. Fine-grained `gc.policies` entries take the same fields plus `all: true` or `keepDuration` (e.g. `6h`).
- Registry mirror: `{"registries": {"docker.io": {"mirrors": ["mirror.gcr.io"]}}}`; per-registry CA: `{"registries": {"my.custom.registry": {"ca": ["/usr/local/share/ca-certificates/my-custom-ca.crt"]}}}`.
  Test: `dagger -M call --progress=plain container from --address=hello-world with-exec --args=/hello stdout`. Verbose output still shows `docker.io/...`; confirm via the mirror's access logs.

## Cache

Dagger caches layers, volumes (persisted across sessions) and function call results. Default policy keeps long-term cache under 75% of disk while leaving at least 20% free.

```shell
dagger core engine local-cache entry-set            # summary
dagger core engine local-cache entry-set entries    # all entry metadata
dagger core engine local-cache prune                # remove ALL entries not in use
dagger core engine local-cache prune --use-default-policy   # prune per configured GC policy
```

## Gotchas

- A mis-set GC policy that cleans all cache severely hurts performance.
- Proxies and CAs cannot be set in engine.json/toml; see computing-software.devops-ci-cd.dagger.custom-ca-and-proxy and computing-software.devops-ci-cd.dagger.custom-runner-and-runtimes.

## Checked

2026-11-07

Read in full from the docs source: reference/configuration/engine.mdx and cache.mdx. Every key and default matched. No corrections needed.

Method: documentation only; no commands were run.
