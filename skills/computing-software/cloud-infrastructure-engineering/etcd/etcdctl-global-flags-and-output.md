---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-global-flags-and-output
name: etcdctl-global-flags-and-output
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [etcdctl-flags, write-out, endpoints, cacert, cert, key, user, command-timeout, dial-timeout, hex]
level: practitioner
status: draft
description: "Common etcdctl global flags: endpoints, TLS client certificates, credentials, timeouts, output formats and environment variables."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
  - "https://etcd.io/docs/v3.5/op-guide/security/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

Flags that apply to every etcdctl command:

- `--endpoints` (env `ETCDCTL_ENDPOINTS`): comma-separated client URLs.
- `--cacert`, `--cert`, `--key`: TLS trust bundle and client certificate pair for HTTPS endpoints.
- `--user USER[:PASSWORD]`, `--password`: authenticate against an auth-enabled cluster; with no password it prompts. `--insecure-transport`, `--insecure-skip-tls-verify` relax TLS checks.
- `--dial-timeout` and `--command-timeout`: connection and per-command limits.
- `-w, --write-out`: `simple` (default), `json`, `protobuf`, `fields`, `table` (table only for list-like commands).
- `--hex`: print byte strings as hex-escaped.
- `--debug`: log client debug output.
- `--discovery-srv`: find endpoints via DNS SRV.

Every flag can be set by an environment variable named `ETCDCTL_` plus the flag in upper snake case, for example `ETCDCTL_CACERT`, `ETCDCTL_CERT`, `ETCDCTL_KEY`, `ETCDCTL_ENDPOINTS`.

Example against a secured cluster:

```bash
export ETCDCTL_ENDPOINTS=https://10.0.1.10:2379
export ETCDCTL_CACERT=/path/to/ca.crt
export ETCDCTL_CERT=/path/to/client.crt
export ETCDCTL_KEY=/path/to/client.key
etcdctl endpoint health
```

JSON output carries keys and values base64-encoded, so decode before reading (`echo Zm9v | base64 -d`). The table format is meant for list-style outputs such as `member list` and `endpoint status`; for key listings use `json` or the default. Command timeouts apply per command, so raise `--command-timeout` for large snapshots or defrag.
