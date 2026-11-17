---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k0s-clusters-with-k0sctl
name: k0s-clusters-with-k0sctl
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, edge-lightweight-distros, k0sctl, k0s, cluster-provisioning, ssh]
level: practitioner
status: docs-checked
description: "Create, upgrade, back up and reset k0s clusters over SSH with k0sctl and a declarative k0sctl.yaml, including controller and worker roles and kubeconfig retrieval."
sources: ["https://docs.k0sproject.io/stable/k0sctl-install/", "https://github.com/k0sproject/k0sctl", "https://docs.k0sproject.io/stable/backup/", "https://docs.k0sproject.io/stable/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k0s clusters with k0sctl

k0s is a single-binary Kubernetes distribution; k0sctl installs and upgrades it across machines
over SSH from one declarative file. k0sctl does not discover hosts: it only operates on the
hosts listed in the configuration.

## Config
```bash
k0sctl init --k0s > k0sctl.yaml         # template including an example spec.k0s.config block
```
```yaml
apiVersion: k0sctl.k0sproject.io/v1beta1
kind: Cluster
metadata: {name: edge-site-1}
spec:
  hosts:
  - {role: controller, ssh: {address: 10.0.0.10, user: admin, keyPath: ~/.ssh/id_ed25519}}
  - {role: controller, ssh: {address: 10.0.0.11, user: admin, keyPath: ~/.ssh/id_ed25519}}
  - {role: controller, ssh: {address: 10.0.0.12, user: admin, keyPath: ~/.ssh/id_ed25519}}
  - {role: worker, ssh: {address: 10.0.0.20, user: admin, keyPath: ~/.ssh/id_ed25519}}
  k0s:
    version: <k0s-version>        # optional; when omitted k0sctl uses the latest stable or the version already running
    config:
      spec:
        api: {externalAddress: k8s.edge-site-1.example.com, sans: [10.0.0.5]}
        network: {provider: calico}
```
Roles: `controller`, `worker`, `controller+worker`, `single` (a one-host cluster; the file can hold
only one host). By default k0s taints `controller+worker` nodes so only workloads with a
toleration run there. `spec.api.externalAddress` is the load-balancer address for controllers;
`sans` adds names/addresses to the API server certificate. `spec.network.provider` accepts
`calico` and `kuberouter` (the default, per the k0s configuration reference).

## Lifecycle
```bash
k0sctl apply --config k0sctl.yaml                 # install or reconcile
k0sctl kubeconfig --config k0sctl.yaml > kubeconfig
k0sctl backup --config k0sctl.yaml                # control-plane state archive in the current directory
k0sctl apply --config k0sctl.yaml --restore-from k0s_backup_<timestamp>.tar.gz
k0sctl reset --config k0sctl.yaml                 # uninstall k0s from the listed hosts
```
Upgrade: raise `spec.k0s.version` above the version on the cluster and run `apply`; hosts not yet
in the cluster are configured and joined by the same command. Nodes are drained before disruptive
operations by default (`spec.options.drain.enabled`, default true; `--no-drain` skips it).

## Backup and restore notes
- The k0s backup holds the certificates and the etcd snapshot (when etcd is the datastore); other
  datastores are not covered by the backup utility.
- Restore is meant for disaster recovery and expects no k0s components on the controllers; the
  control plane address (`externalAddress`) must stay the same between backup and restore.
- Backup files are named with a running timestamp (for example `k0s_backup_<epoch>.tar.gz`).

## Notes
- Put an external load balancer or `externalAddress` in front of controllers for HA.
- Air-gapped: use per-host `files` entries to upload an airgap image bundle.
- Keep `k0sctl.yaml` in Git; it is the source of truth for the cluster.

## Verify
`kubectl --kubeconfig kubeconfig get nodes -o wide` shows every worker Ready at the new version after an apply.

## Checked

Checked 2026-10-27 against k0s and k0sctl documentation (k0sproject/k0s docs and k0sproject/k0sctl README, current main branch) and Kubernetes documentation (release v1.37.1): k0sctl README (apply, init --k0s, backup and restore-from, reset, kubeconfig, roles controller/worker/controller+worker/single, drain default true, version auto-discovery, upgrade triggered by a higher spec.k0s.version, files entries for airgap bundles), k0s backup page (certificates and etcd snapshot, naming) and k0s configuration reference (spec.api.externalAddress and sans, network provider calico or kuberouter). Replaced the pinned k0s version and removed the unconfirmed claim about the order of controller and worker upgrades.

Method: documentation only; no commands were run.
