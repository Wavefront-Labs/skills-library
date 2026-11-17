---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.environment-variable-config
name: environment-variable-config
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-prefix, toml, docker, environment-variables, toml-env]
level: practitioner
status: docs-checked
description: "Replace weed flags and TOML settings with environment variables: flag-name vars, WEED_ prefix rules, dots to underscores, and secrets for security.toml."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Environment-Variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# environment variable config

Flags: upper-case the flag name.
```bash
export IP_BIND=0.0.0.0 PORT=5000 MDIR=/tmp VOLUMEPREALLOCATE=true
weed master     # same as: weed master -port 5000 -mdir /tmp -volumePreallocate -ip.bind 0.0.0.0
```
Logging and similar flags (`v`, `logtostderr`, `logdir`, `config_dir`, ...) need the `WEED_` prefix, e.g. `WEED_CONFIG_DIR`.

TOML settings (filer.toml, replication, security.toml): prefix `WEED_` and replace dots with underscores.
```bash
WEED_REDIS2_ENABLED=true
WEED_REDIS2_ADDRESS=localhost:6379
WEED_REDIS2_PASSWORD=secret
WEED_REDIS2_DATABASE=0
```
That mirrors `[redis2]` in filer.toml.

Keep secrets out of version control this way:
```bash
WEED_JWT_SIGNING_KEY=...   WEED_JWT_FILER_SIGNING_KEY=...
WEED_GRPC_CA=/path/to/ca.crt   WEED_GRPC_VOLUME_CERT=...
WEED_S3_SSE_KEK=$(openssl rand -hex 32)   # or WEED_S3_SSE_KEY, set only one
```
For S3 admin credentials the page points to its S3 Credentials page: config file highest priority, filer configuration medium, environment variables lowest, including the standard `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.

Filer stores: only one store can be enabled, so when using an external store set `WEED_LEVELDB2_ENABLED=false`. Changing store does not migrate existing data. Array values are comma-separated (for example `WEED_REDIS_CLUSTER2_ADDRESSES=host1:6379,host2:6379`). `weed scaffold -config=filer` lists the available stores and options.

## Checked

2026-11-08. Confirmed against the Environment Variables wiki page. Removed the unsupported "check the startup log" verification and the claim that replication settings use the same example; added the leveldb2, migration and array-value notes.

Method: documentation only; no commands were run.
