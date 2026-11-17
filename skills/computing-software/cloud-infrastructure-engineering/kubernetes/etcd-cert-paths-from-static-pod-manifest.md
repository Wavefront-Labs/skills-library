---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-cert-paths-from-static-pod-manifest
name: etcd-cert-paths-from-static-pod-manifest
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-backup, etcd-cert-paths, etcdctl-snapshot-save, static-pod]
level: practitioner
status: docs-checked
description: "Find etcd endpoints and the CA/cert/key paths from the etcd static pod manifest so etcdctl commands authenticate correctly, the classic CKA task."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/", "https://etcd.io/docs/v3.6/op-guide/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding etcd endpoints and certs

## Read them from the manifest
```bash
sudo grep -E -- '--(listen-client-urls|advertise-client-urls|cert-file|key-file|trusted-ca-file|peer-)' \
  /etc/kubernetes/manifests/etcd.yaml
```
Typical kubeadm values:
```
--advertise-client-urls=https://10.0.0.11:2379
--cert-file=/etc/kubernetes/pki/etcd/server.crt
--key-file=/etc/kubernetes/pki/etcd/server.key
--trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```
Or from the API server's side (useful for external etcd):
```bash
sudo grep -- '--etcd' /etc/kubernetes/manifests/kube-apiserver.yaml
# --etcd-servers, --etcd-cafile, --etcd-certfile (apiserver-etcd-client.crt), --etcd-keyfile
```

## Use them
```bash
export ETCDCTL_API=3
sudo etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health
```
`etcdctl` takes `--cacert/--cert/--key`, while the etcd server flags are
`--trusted-ca-file/--cert-file/--key-file`; mixing them up is the most common exam slip.
`healthcheck-client.crt` or `apiserver-etcd-client.crt` also work as client certs.

## No etcdctl on the host
Run the tool from a container image with your container runtime (for example `crictl run`), not through
Kubernetes, as the kubeadm external etcd guide does. Mount the PKI directory read-only and write snapshots
to a mounted host directory so the file lands on the node.

## Gotchas
- An endpoint of `127.0.0.1` only works from the node running that member.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Confirmed: the kubeadm certificate file names and the etcd flag to file mapping (`--cert-file`, `--key-file`, `--trusted-ca-file` on etcd versus `--cert`, `--key`, `--cacert` on etcdctl; Kubernetes PKI page); kube-apiserver flags `--etcd-servers`, `--etcd-cafile`, `--etcd-certfile`, `--etcd-keyfile`; the Kubernetes docs say the certificate paths can be obtained from the etcd Pod description. Removed as unconfirmed: running etcdctl through `kubectl exec` (the kubeadm external etcd guide runs etcdctl from a container image through the container runtime instead), the claim that the etcd static pod image carries etcdctl, and the `context deadline exceeded` diagnosis.

Method: documentation only; no commands were run.
