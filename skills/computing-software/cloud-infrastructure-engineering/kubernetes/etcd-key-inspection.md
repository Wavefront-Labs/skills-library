---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-key-inspection
name: etcd-key-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-operations, etcdctl-get-prefix, etcd-object-count, etcd-defrag]
level: practitioner
status: docs-checked
description: "Inspect what is filling etcd: list keys by prefix, count objects per resource type, find large objects and events, read-only and safely."
sources: ["https://etcd.io/docs/v3.6/op-guide/security/", "https://etcd.io/docs/v3.6/dev-guide/limit/", "https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiserver/pkg/storage/etcd3/metrics/metrics.go", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting etcd keys and object counts

The API server prepends a configurable prefix (`--etcd-prefix`) to every resource path it stores in etcd; the
examples below assume the common `/registry`, so confirm the value on your API server. The key layout under
the prefix is an implementation detail of the API server, so use this for read-only diagnostics, not as an
interface. Secrets are stored encrypted only if encryption at rest is configured.

## Setup
```bash
alias e='sudo ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key'
```

## List keys
```bash
e get /registry --prefix --keys-only                      # every key: large on busy clusters
e get /registry/<resource-path> --prefix --keys-only      # one resource type
```
For per-resource object counts prefer the API server's own metric (`apiserver_resource_objects`, labels
`group` and `resource`) over scanning etcd.

## Large objects
etcd rejects requests above its maximum request size (1.5 MiB by default, `--max-request-bytes`). Objects
near that size (big ConfigMaps, Helm release Secrets) slow every list; find them from the API side by
listing the resource and checking sizes, not by reading every value out of etcd.

## Also useful
```bash
e endpoint status -w table            # DB SIZE vs the in-use size shows fragmentation
kubectl get --raw /metrics                # look for apiserver_resource_objects
```
`apiserver_storage_objects` is deprecated since Kubernetes 1.34 in favour of `apiserver_resource_objects`.

## Rules
- Read only. Never `etcdctl put/del` under `/registry` on a live cluster; the API server cache
  will not know and you can corrupt object state.
- Avoid `get --prefix` without `--keys-only` on huge prefixes; it returns every value.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: `apiserver_storage_objects` is deprecated since Kubernetes 1.34; use `apiserver_resource_objects` (labels group and resource). Confirmed: the API server option `--etcd-prefix` prepends a prefix to all resource paths; etcdctl `get` with `--prefix`, `--keys-only` and `--print-value-only`; the default 1.5 MiB maximum request size in the etcd limits page. Removed as unconfirmed: the awk, grep and shell-loop counting pipelines, `get --count-only`, the per-resource key layout (only the Secrets path `/registry/secrets/<namespace>/<name>` appears in the encryption docs) and the statement about value encoding, which are implementation details of the API server.

Method: documentation only; no commands were run.
