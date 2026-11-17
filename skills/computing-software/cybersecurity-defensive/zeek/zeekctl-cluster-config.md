---
id: computing-software.cybersecurity-defensive.zeek.zeekctl-cluster-config
name: zeekctl-cluster-config
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, cluster-config, zeekctl-cfg, networks-cfg, zeekctl-install]
level: practitioner
status: docs-checked
description: "Set up a multi-host Zeek cluster with ZeekControl: Zeek user and ssh prerequisites, zeekctl.cfg, node.cfg entries, networks.cfg, and zeekctl install."
sources: ["https://docs.zeek.org/en/current/cluster-setup.html", "https://docs.zeek.org/en/current/quickstart.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# zeekctl cluster config

Prerequisites: the same Zeek user on every host, with passwordless ssh from the manager (for example public keys), promiscuous access to the capture interface on workers, and the same writable prefix path on all hosts.

On the manager host only:

1. Edit `<prefix>/etc/zeekctl.cfg`; you will most likely change `MailTo` and `LogRotationInterval`.
2. Edit `<prefix>/etc/node.cfg`: comment out the standalone node and add entries.

```
[logger]
type=logger
host=10.0.0.10
[manager]
type=manager
host=10.0.0.10
[proxy-1]
type=proxy
host=10.0.0.10
[worker-1]
type=worker
host=10.0.0.11
interface=eth0
```

3. Edit `<prefix>/etc/networks.cfg`, listing networks considered local.
4. Run `zeekctl install`, which pushes Zeek to all machines.

Then `deploy` starts the cluster and `top` shows each node's name, type, host, pid and resource use. The documentation also suggests a cron job on the manager to monitor the cluster.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
