---
id: computing-software.cybersecurity-defensive.zeek.management-framework
name: management-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, management-framework, zeek-client, controller-agent, deploy-config]
level: advanced
status: docs-checked
description: "Zeek Management framework: controller, agent, instance and zeek-client terms, all-in-one quickstart with deploy-config, discontinued status."
sources: ["https://docs.zeek.org/en/current/frameworks/management.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# management framework

Status: the page says development is discontinued and the scripting code moves to an external package with Zeek 9.1. It can still be used with Zeek 9.0, but consider ZeekControl or the newer zeek.conf and zeek-systemd-generator approach.

It is a Zeek-based, service-oriented, event-driven way to manage a cluster. Terms:

- **Controller**: one per installation; a stateful Zeek process that persists cluster configurations and relays tasks to agents.
- **Instance**: the processes under one Supervisor, usually one per machine or container.
- **Agent**: runs in each instance, peers with the controller (by default agents connect to it) and carries out node-level tasks.
- **Cluster nodes**: manager, logger(s) and workers as in the cluster framework.
- **Client**: the user interface; `zeek-client` ships with Zeek and talks to the controller's event API.

All-in-one quickstart as root:

```
zeek -C -j policy/frameworks/management/controller policy/frameworks/management/agent
```

Then write `cluster.cfg` with sections such as `[manager]` `role = manager`, `[logger]`, and `[worker-01]` with `role = worker` and `interface = lo`, and deploy:

```
zeek-client deploy-config cluster.cfg
zeek-client get-nodes
```

The result lists per-node success and the owning instance.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
