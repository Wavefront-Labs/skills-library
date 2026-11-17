---
id: computing-software.systems-network-administration.rclone.rclone-rc-api-and-security
name: rclone-rc-api-and-security
category: computing-software
field: systems-network-administration
product: rclone
tags: [rc, rcd, remote-control, rc-api, async-jobs, security, rc-htpasswd]
level: advanced
status: docs-checked
description: "Run the rclone remote control API safely, call it with rclone rc or HTTP, and use async jobs, groups and config options."
sources: ["https://rclone.org/rc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start the API with `--rc`, or run the dedicated `rclone rcd`. It binds to `localhost:5572` by default.

## Security first

Access to the rc is equivalent to shell access as the rclone user. A caller can run OS commands (`core/command`, or `config/create` for backends that shell out), read and write any reachable file through a `local` remote, read back stored credentials with `config/dump`, change behaviour with `options/set`, and stop the process with `core/quit`. There is no per-endpoint scope. So: keep the loopback bind, never use `--rc-no-auth` on a non-loopback address, and use `--rc-user`/`--rc-pass` or `--rc-htpasswd` plus `--rc-cert` and `--rc-key` (and raise `--rc-min-tls-version`) whenever others can reach the port. With `--rc-serve` and no authentication only remotes already in the config can be served; inline remotes and bare local paths are rejected.

## Calling it

```console
rclone rc rc/noop param1=one param2=two
rclone rc --url http://host:1234/ rc/noop
rclone rc --unix-socket /tmp/rclone.sock rc/noop
rclone rc --json '{ "p1": [1,"2",null,4] }' rc/noop
rclone rc operations/list fs=/tmp remote=test opt='{"showHash": true}'
```

An object parameter can be passed as a JSON string without `--json`. Use forward slashes in Windows paths, or escape backslashes in JSON.

## Special parameters

- `_async=true` runs the call as a background job and returns a `jobid`; poll `job/status`. The `Prefer: respond-async` header does this and returns HTTP 202. `sync/copy`, `sync/move` and `operations/purge` are typical.
- `_config` sets config flags for one call; `_filter` sets filter flags; `_group` assigns stats groups.
- Other useful calls: `core/stats`, `core/bwlimit`, `config/listremotes`, `vfs/forget`, `core/version`.

`--rc-enable-metrics` exposes `/metrics`; `--rc-files` and `--rc-web-gui` serve a browser GUI.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
