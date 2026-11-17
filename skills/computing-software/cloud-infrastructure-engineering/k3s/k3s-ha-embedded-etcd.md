---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-ha-embedded-etcd
name: k3s-ha-embedded-etcd
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, embedded-etcd, cluster-init, quorum]
level: practitioner
status: docs-checked
description: "Build a high-availability K3s control plane with three or more servers on embedded etcd using --cluster-init."
sources:
  - https://docs.k3s.io/datastore/ha-embedded
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: an HA cluster with embedded etcd. Use an odd number of servers: quorum is (n/2)+1, and adding one node to an odd-sized cluster raises the nodes needed for quorum without improving fault tolerance.

Composition: three or more servers (API, control plane, etcd), optional agents, optional fixed registration address.

First server:

```
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server \
    --cluster-init \
    --tls-san=<FIXED_IP>
```

(--tls-san only if you use a fixed registration address.) Join the second and third servers:

```
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server \
    --server https://<ip or hostname of server1>:6443 \
    --tls-san=<FIXED_IP>
```

Any clustered server can be used in --server to join further servers and agents; agents join with `K3S_TOKEN=SECRET sh -s - agent --server https://<ip or hostname of server>:6443`.

Flags that must match on all servers: --cluster-dns, --cluster-domain, --cluster-cidr, --service-cidr; --disable-helm-controller, --disable-kube-proxy, --disable-network-policy and anything passed to --disable; and --secrets-encryption.

Warning: embedded etcd may have performance problems on slow disks such as Raspberry Pis with SD cards.

Verify: `kubectl get nodes` shows all servers Ready with roles control-plane,etcd,master.

## Checked

2026-11-03: read docs.k3s.io datastore/ha-embedded. Confirmed: the odd-server quorum rule, --cluster-init and --tls-san first-server command, the join command, the flags that must match across servers, and the SD-card performance warning. Reworded the agent join command to match the page.

Method: documentation only; no commands were run.
