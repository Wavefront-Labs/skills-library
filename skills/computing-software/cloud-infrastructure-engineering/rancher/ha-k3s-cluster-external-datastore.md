---
id: computing-software.cloud-infrastructure-engineering.rancher.ha-k3s-cluster-external-datastore
name: ha-k3s-cluster-external-datastore
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [k3s, high-availability, datastore-endpoint, mysql, kubeconfig, token]
level: practitioner
status: docs-checked
description: "Install the two-node K3s cluster for Rancher using an external datastore: datastore-endpoint, server token joining, version pinning, kubeconfig fix, and the single-node variant."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-cluster-setup/k3s-for-rancher
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The K3s route to a Rancher management cluster assumes two nodes, a load balancer, a DNS record and an **external datastore** (the page's example is MySQL). Pin the Kubernetes version with `INSTALL_K3S_VERSION` on the install script, picking a version your Rancher release supports.

On the first node the server is started with `--datastore-endpoint`, whose value is the connection URI, for example `mysql://username:password@tcp(hostname:3306)/database-name`. The page lists etcd, MySQL, PostgreSQL or SQLite (the default) as valid datastores, and says the endpoint can instead be passed as `$K3S_DATASTORE_ENDPOINT`.

```
curl -sfL https://get.k3s.io |  INSTALL_K3S_VERSION=<VERSION> sh -s - server \
  --datastore-endpoint="<DATASTORE_ENDPOINT>"
```

Read the join token from `/var/lib/rancher/k3s/server/token`, then run the same command on the second node with `--token "<MAIN_SERVER_NODE_TOKEN>"`. Confirm both nodes appear with `sudo k3s kubectl get nodes`, and check pods across all namespaces.

K3s writes its kubeconfig to `/etc/rancher/k3s/k3s.yaml`. It contains full-access credentials; copy it to `~/.kube/config`, then replace the localhost `server` value with the load balancer DNS name on port 6443 (the API is on 6443, Rancher on 80 and 443).

For a single-node install, run the server command on just one node. That gives no high availability but keeps a migration path, and Rancher is then installed with Helm exactly as on any other cluster.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Setting up a High-availability K3s Kubernetes Cluster for Rancher. Nothing removed.

Method: documentation only; no commands were run.
