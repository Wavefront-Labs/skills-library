---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-ha-external-database
name: k3s-ha-external-database
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, external-database, node-taint, server-token]
level: practitioner
status: docs-checked
description: "Run an HA K3s cluster with two or more servers on an external datastore, including token handling and taints."
sources:
  - https://docs.k3s.io/datastore/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: HA control plane with servers sharing an external database.

Steps:

1. Create the external datastore.
2. Launch two or more servers with --datastore-endpoint and, optionally, a deterministic --token:

```
curl -sfL https://get.k3s.io | sh -s - server \
  --token=SECRET \
  --datastore-endpoint="mysql://username:password@tcp(hostname:3306)/database-name" \
  --tls-san=<FIXED_IP>
```

3. Join more servers with the same command and token. If the first server started without --token or K3S_TOKEN, read the token from any joined server:

```
cat /var/lib/rancher/k3s/server/token
```

4. Optionally join agents: `K3S_TOKEN=SECRET k3s agent --server https://server-or-fixed-registration-address:6443`.

Servers are schedulable by default. For a dedicated control plane use taints, for example `--node-taint CriticalAddonsOnly=true:NoExecute`.

Flags that must be identical on all servers: --cluster-dns, --cluster-domain, --cluster-cidr, --service-cidr; --disable-helm-controller, --disable-kube-proxy, --disable-network-policy and every --disable component; --secrets-encryption.

Keep a copy of the token: it is required when restoring from backup and adding nodes. Previously K3s did not enforce a token with external SQL datastores.

Verify: `k3s kubectl get nodes` shows the servers Ready.

## Checked

2026-11-03: read docs.k3s.io datastore/ha. Confirmed: the --datastore-endpoint server command, reading /var/lib/rancher/k3s/server/token, the agent join command, the CriticalAddonsOnly taint example, the must-match flags and the token retention note.

Method: documentation only; no commands were run.
