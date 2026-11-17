---
id: computing-software.software-engineering.elixir.libcluster-pg-clustering
name: libcluster-pg-clustering
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, libcluster, pg, cluster-strategy, dns-cluster, kubernetes-dns, process-groups, clustering-libs]
level: advanced
status: draft
description: "Form clusters automatically with libcluster strategies (or dns_cluster) and use :pg process groups for cluster-wide pub/sub."
sources: ["https://hexdocs.pm/libcluster", "https://www.erlang.org/doc/apps/kernel/pg.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clustering with libcluster and :pg

**Goal:** nodes find each other in containers and orchestrators.

```elixir
# config
config :libcluster, topologies: [
  k8s: [strategy: Cluster.Strategy.Kubernetes.DNS,
        config: [service: "myapp-headless", application_name: "myapp"]]
]
# application.ex
{Cluster.Supervisor, [Application.get_env(:libcluster, :topologies), [name: MyApp.ClusterSupervisor]]}

:pg.start_link()                                 # or under supervisor; default scope
:pg.join(:room, self()) ; :pg.get_members(:room)
for pid <- :pg.get_members(:room), do: send(pid, :hello)
```

## Rules
- Strategies include Epmd (static host list), Gossip, DNS-based, Kubernetes variants; choose per platform. Phoenix apps often use `dns_cluster`.
- Node names must be resolvable and unique (`RELEASE_NODE`, `RELEASE_DISTRIBUTION=name`).
- `:pg` replaced `pg2`; membership is eventually consistent and members are removed when processes die.
- Phoenix.PubSub uses `:pg` for cross-node broadcasts automatically when nodes are connected.

## Self-check
Start 2 nodes with the Epmd strategy and confirm `Node.list/0` shows the peer.
