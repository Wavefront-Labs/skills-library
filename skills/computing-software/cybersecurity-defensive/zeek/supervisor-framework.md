---
id: computing-software.cybersecurity-defensive.zeek.supervisor-framework
name: supervisor-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, supervisor, supervisor-mode, node-config, process-supervision]
level: advanced
status: docs-checked
description: "Run Zeek in Supervisor mode (-j) to spawn and revive persistent node processes with Supervisor::create and NodeConfig, including a supervised cluster and remote restart."
sources: ["https://docs.zeek.org/en/current/frameworks/supervisor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# supervisor framework

A Supervisor revives any supervised process that dies and shuts the whole tree down in order when it terminates. It can underpin a ZeekControl-like deployment that integrates as a standard system service.

Launch with `-j`:

```
zeek -j simple-supervisor.zeek
```

```
event zeek_init()
    {
    if ( Supervisor::is_supervisor() )
        {
        local sn = Supervisor::NodeConfig($name="foo", $interface="en0");
        local res = Supervisor::create(sn);
        }
    }
```

The same script runs in both the Supervisor and its children; `Supervisor::is_supervisor` and `Supervisor::is_supervised` distinguish them, and `Supervisor::node()` gives a child's name. Most command-line arguments are inherited by children, except `-r` and `-i`. Add `-C` for checksum offloading.

A full cluster: build a `table[string] of Supervisor::ClusterEndpoint` with roles `Supervisor::MANAGER`, `LOGGER`, `PROXY`, `WORKER`, set `sn$cluster = cluster` and `sn$directory = n` per node, and call `Broker::listen("127.0.0.1", 9999/tcp)` in the Supervisor. Node stdout and stderr are redirected through the Supervisor with the node name prefixed.

Remote control: a peer publishes `SupervisorControl::restart_request` on `SupervisorControl::topic_prefix`, for example to reload changed scripts. APIs: `base/frameworks/supervisor/api.zeek` and `control.zeek`. An intermediate Stem process manages node lifetimes.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
