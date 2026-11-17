---
id: computing-software.cloud-infrastructure-engineering.rancher.ha-rke2-cluster-for-rancher
name: ha-rke2-cluster-for-rancher
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rke2, high-availability, tls-san, kubeconfig, load-balancer, local-cluster]
level: practitioner
status: docs-checked
description: "Build the three-node RKE2 cluster for Rancher: config.yaml token and tls-san, joining via port 9345, load balancer listeners, kubeconfig."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-cluster-setup/rke2-for-rancher
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The documented HA layout for the Rancher management cluster is three RKE2 server nodes, a load balancer and a DNS record. RKE2 runs embedded etcd, so no external datastore is needed. The load balancer needs **two listeners**: the supervisor on port 9345 and the Kubernetes API on port 6443.

On the first node, create `/etc/rancher/rke2/config.yaml` with a pre-shared `token` and a `tls-san` list holding the hostnames or IPs clients will use, so the fixed registration address does not cause certificate errors. If you omit the token, RKE2 generates one at `/var/lib/rancher/rke2/server/node-token`. Pin the RKE2 version with the `INSTALL_RKE2_VERSION` environment variable on the install script, choosing a Kubernetes version your Rancher release supports.

```
token: my-shared-secret
tls-san:
  - my-kubernetes-domain.com
  - another-kubernetes-domain.com
```

Install with `curl -sfL https://get.rke2.io | sh -`, then `systemctl enable rke2-server.service` and `systemctl start rke2-server.service`. The other two servers use the same token plus `server: https://<DNS-DOMAIN>:9345`.

Check readiness with the bundled kubectl and `--kubeconfig /etc/rancher/rke2/rke2.yaml`: nodes should be Ready and system pods healthy. That kubeconfig holds full-access credentials, so store it securely. When copied to `~/.kube/config` on a workstation its `server` points at localhost; change it to the load balancer DNS name on port 6443. The Rancher UI itself is served by the Traefik ingress on ports 80 and 443, not 6443.

## Checked

2026-11-09. Read the cited RKE2 for Rancher page in full and checked every claim against it (listeners 9345 and 6443, config.yaml, tls-san, node-token path, INSTALL_RKE2_VERSION, join config, readiness commands, kubeconfig edit, Traefik ports). No claims removed.

Method: documentation only; no commands were run.
