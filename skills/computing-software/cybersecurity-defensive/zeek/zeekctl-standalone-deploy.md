---
id: computing-software.cybersecurity-defensive.zeek.zeekctl-standalone-deploy
name: zeekctl-standalone-deploy
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, zeekctl, standalone-node, node-cfg, local-zeek]
level: practitioner
status: docs-checked
description: "Run Zeek under ZeekControl as a standalone node: node.cfg interface, local.zeek, deploy and stop, and where the compressed rotated logs end up."
sources: ["https://docs.zeek.org/en/current/quickstart.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# zeekctl standalone deploy

ZeekControl (`zeekctl`) manages deployments. Set the interface in `$PREFIX/etc/node.cfg`:

```
[zeek]
type=standalone
host=localhost
interface=en0
```

Site customisation goes in `$PREFIX/share/zeek/site/local.zeek`, which zeekctl loads by default and Zeek upgrades do not overwrite.

Start the interactive shell and deploy:

```
$ zeekctl
[ZeekControl] > deploy
[ZeekControl] > stop
[ZeekControl] > exit
```

Logs are not written to the current directory. While running they are in `$PREFIX/logs/current`. After stopping they move to a dated directory such as `$PREFIX/logs/2025-01-01/` as `.log.gz` files. Read them with `zcat`.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
