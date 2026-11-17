---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-upgrade-servers
name: consul-upgrade-servers
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-upgrade, rolling-upgrade, version-skew]
level: practitioner
status: docs-checked
description: "Upgrade Consul servers one at a time with a snapshot first, check Autopilot health between steps, and upgrade clients afterwards."
sources: ["https://developer.hashicorp.com/consul/commands/snapshot", "https://developer.hashicorp.com/consul/commands/operator/autopilot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prepare, then roll.

```sh
consul snapshot save pre-upgrade.snap
consul operator autopilot state | head -30
# per server: stop, replace binary, start
systemctl stop consul && install consul-new /usr/local/bin/consul && systemctl start consul
consul operator raft list-peers
```

Check the target version's upgrade notes first. Restart servers one at a time and wait until each is healthy and has rejoined the cluster before the next. When all servers are done, roll out client agents the same way, restarting any associated Envoy proxies with a version compatible with the new Consul.

Gotchas: nodes gossip their protocol version and builds, so newer features switch on when available. For community edition the docs recommend upgrading about every 4 months to the latest major release to stay on a maintained version; for large version jumps follow the upgrade instructions and the version-specific notes.

Verify: `consul members` shows the new build and the highest protocol version for every member.

## Checked

2026-11-03. Confirmed against the Upgrading Consul page (standard upgrade steps, one server at a time, clients afterwards, Envoy restart, 4 month recommendation, consul members check) and the consul snapshot save, operator raft list-peers and operator autopilot state command pages. Removed: leader-last ordering, the downgrade and skipped-major-version claims, the quorum warning and the `consul version` check.

Method: documentation only; no commands were run.
