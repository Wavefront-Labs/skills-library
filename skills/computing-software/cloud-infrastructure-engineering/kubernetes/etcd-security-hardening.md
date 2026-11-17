---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-security-hardening
name: etcd-security-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcdctl, peer-tls, client-tls, mtls, etcd-backup, etcd-snapshot, cluster-admin-equivalent, etcd-defrag, managed-kubernetes]
level: advanced
status: docs-checked
description: "etcd as the de facto cluster-admin-equivalent store: peer/client TLS separation, who can reach it, and why snapshot files need the same protection as a live Secret dump."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/security/", "https://etcd.io/docs/v3.6/op-guide/maintenance/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.10/etcd.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd security — whoever can read it owns the cluster

**Goal:** treat etcd access as equivalent to `cluster-admin` (because it is —
every object, including Secrets, lives there) and make sure neither the live
store nor its backups are reachable by anything less trusted than that. Secrets
encryption-at-rest (which still requires etcd access to be meaningless to
exfiltrate) is in
`computing-software.cloud-infrastructure-engineering.kubernetes.secrets-encryption-at-rest`;
this skill covers reaching the store itself, which encryption at rest does not
prevent (encrypted-at-rest Secrets are still readable *through the API*, which
means through anyone who can forge or steal apiserver-equivalent access to
etcd).

## 1. Why etcd access bypasses RBAC entirely
Kubernetes RBAC is enforced by the **apiserver**, not by etcd. Direct access to
etcd (its client port, typically 2379) with valid client certs reads and writes
every object in the cluster with no RBAC check at all — there is no etcd-level
equivalent of a Role scoping what keys you can touch by default. A workload or
operator with network access to etcd's port and a valid client cert is
cluster-admin regardless of what RBAC says about that identity in the
Kubernetes API.

## 2. Two separate TLS trust domains — don't conflate them
- **Client-to-server TLS**: protects the apiserver-to-etcd connection
  (`--etcd-certfile`, `--etcd-keyfile`, `--etcd-cafile` on kube-apiserver;
  `--client-cert-auth=true` on etcd). This is what you'd rotate/scope for "which
  Kubernetes control-plane components can talk to etcd."
  Without client certificate authentication (`--client-cert-auth=true` with a trusted CA) and without etcd
  user authentication, **any client that can reach the port can read and write the entire cluster state**.
- **Peer TLS**: protects etcd-node-to-etcd-node replication traffic
  (`--peer-cert-file`, `--peer-client-cert-auth=true`) — a separate cert chain;
  mixing up peer and client certs (or disabling peer auth while keeping client
  auth) leaves the Raft replication channel as the open door instead.

## 3. Network exposure — etcd should never be reachable off-node
- Bind etcd's client port to a private interface/localhost-plus-control-plane
  network only; never expose 2379/2380 on a public IP or a shared VPC subnet
  reachable by workload pods.
- On self-managed clusters, a firewall/security-group rule restricting the etcd
  ports to exactly the control-plane nodes (not the whole VPC, not worker nodes)
  is a second independent layer beneath TLS — defense against a misconfigured
  cert chain or a future TLS downgrade bug, not a substitute for TLS.
- Where the control plane is a managed service, etcd access is the provider's responsibility (check the
  provider's documentation); this section matters for self-managed and kubeadm clusters.

## 4. Snapshots and backups are a full cluster-admin dump
```bash
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db \
  --endpoints=https://127.0.0.1:2379 --cacert=... --cert=... --key=...
```
A snapshot file contains **every object in the cluster**, including Secrets —
if Secrets encryption at rest (see that skill) was enabled, the snapshot
preserves them encrypted; if it wasn't, the snapshot is a plaintext dump of
every credential the cluster has ever stored. Treat snapshot storage,
transport, and access control with exactly the rigor you'd apply to a Secrets
database export: encrypted at rest independently of cluster-level encryption,
access-logged, and retention-limited. A snapshot taken before encryption was
enabled (or before a key rotation + resweep, see `secrets-encryption-at-rest`
§5) remains a plaintext liability indefinitely until deleted.

## 5. Operational hygiene that's also a security property
- `etcdctl endpoint status` / `defrag` regularly — etcd that exceeds
  its quota (2 GiB by default, 8 GiB suggested maximum) goes into a maintenance mode that accepts only
  key reads and deletes, which from a security-incident-response
  standpoint means you cannot write a fix (a new RoleBinding revocation, an
  emergency NetworkPolicy) during the outage it causes.
- Client cert rotation for etcd follows the same "don't let it silently expire"
  risk as any mTLS deployment — monitor cert expiry explicitly; an expired
  apiserver↔etcd client cert is a full control-plane outage, not a graceful
  degradation.

## Gotchas
- `etcdctl` run directly on a control-plane node, using the node's own
  filesystem-resident certs, works regardless of Kubernetes RBAC — anyone with
  SSH/node access to a control-plane node already has this path; node-level
  access to control-plane nodes should be treated as equivalent to
  cluster-admin, which is a stronger requirement than many orgs' SSH access
  policies assume.
- `--auto-tls`/`--peer-auto-tls` (etcd's self-signed convenience flags) are fine
  for quick local testing but should never ship to production — they skip real
  CA-backed verification, meaning a network-position attacker could potentially
  present their own self-signed cert and be trusted.
- Encryption at rest for Secrets (apiserver-side) and TLS for etcd access are
  independent controls that are easy to assume cover each other — encryption at
  rest protects a stolen disk/snapshot; etcd TLS protects the network path;
  neither substitutes for the other.

## Verify
- [ ] `--client-cert-auth=true` and `--peer-client-cert-auth=true` are both set;
      neither falls back to `--auto-tls`/`--peer-auto-tls` in production.
- [ ] etcd client/peer ports are not reachable from worker-node or pod network
      space, confirmed by an actual connection test from a non-control-plane pod.
- [ ] Snapshot files are encrypted independently and access-controlled at least
      as strictly as a Secrets database export; retention is bounded.
- [ ] etcd disk usage/quota is monitored with alerting below the hard quota
      limit, not discovered via a write-rejection outage.
- [ ] Certs for both client and peer TLS have monitored expiry with alerting
      well before expiration.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Fixed: a NOSPACE alarm leaves the cluster in a maintenance mode that accepts only key reads and deletes (the skill said writes are rejected cluster-wide); the default quota is 2 GiB with 8 GiB suggested (not "2-8GB typically"). Confirmed: Kubernetes docs say access to etcd is equivalent to root permission in the cluster and that only the API server should have access; API server flags `--etcd-certfile`, `--etcd-keyfile`, `--etcd-cafile`; etcd flags `--client-cert-auth`, `--trusted-ca-file`, `--peer-client-cert-auth`, `--peer-cert-file`; `--auto-tls` and `--peer-auto-tls` generate self-signed certificates (kube-bench CIS items 2.3 and 2.6 require them off); encryption at rest and snapshot encryption advice. Removed as unconfirmed: the claim about exposed-etcd incident writeups and statements about specific managed Kubernetes services.

Method: documentation only; no commands were run.
