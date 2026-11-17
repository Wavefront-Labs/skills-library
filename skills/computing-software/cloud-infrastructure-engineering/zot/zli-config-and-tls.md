---
id: computing-software.cloud-infrastructure-engineering.zot.zli-config-and-tls
name: zli-config-and-tls
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, zli, zli-config, default-server, verify-tls, client-certificate]
level: practitioner
status: docs-checked
description: "Register Zot servers in the zli client, set a default, and configure TLS CA and client certificates and other per-server variables."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/user-guides/zli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`zli` is the Zot command line client. Subcommands: `completion` (bash, fish, powershell, zsh), `config`, `cve`, `image`, `repo`, `search`, `status`.

Add and list servers:

```
bin/zli config add remote-zot https://server-example:8080
bin/zli config -l
```

Default server, so `--config` can be omitted:

```
bin/zli config set-default local
bin/zli image list
bin/zli config clear-default
```

TLS:

```
bin/zli config add secure https://registry.example.com
bin/zli config secure ca-cert /etc/zot/certs/ca.pem
bin/zli config secure client-cert /etc/zot/certs/client.pem
bin/zli config secure client-key /etc/zot/certs/client-key.pem
bin/zli image list --config secure
```

Config variables: `url`, `showspinner` (true/false), `verify-tls` (default true), `ca-cert`, `client-cert`, `client-key`. Other config forms: `zli config main url`, `zli config main --list`, `zli config remove main`; flag `--reset`.

Common flags on commands: `--config`, `--url`, `-u, --user`, `--debug`, `--verbose`, and `-f text|json|yaml`. `zli status` uses `-c` for config.

## Checked

2026-11-08. Read in full: docs/user-guides/zli.md and compared every claim above against it.

Method: documentation only; no commands were run.
