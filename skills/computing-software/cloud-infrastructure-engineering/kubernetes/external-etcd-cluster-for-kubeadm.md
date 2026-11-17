---
id: computing-software.cloud-infrastructure-engineering.kubernetes.external-etcd-cluster-for-kubeadm
name: external-etcd-cluster-for-kubeadm
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, etcd, external-etcd, external-etcd-setup, etcd-endpoints, etcd-topology, etcd-tls, systemd-etcd, control-plane-ha]
level: advanced
status: docs-checked
description: "Stand up a 3-node external etcd cluster (kubeadm-generated certs, static pods or systemd) and point ClusterConfiguration.etcd.external at it."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External etcd cluster for kubeadm

**Goal:** run etcd on its own three hosts so control-plane node loss and etcd loss are
decoupled, then bootstrap kubeadm against it. Costs three extra machines and separate
certificate handling; buys independent scaling/backup of etcd and the ability to replace
control-plane nodes without touching quorum.

## 1. Generate etcd PKI with kubeadm (on one etcd host, then copy)
```bash
# /tmp/etcd0.yaml, etcd1.yaml, etcd2.yaml: one per host (HOST0 certificates are generated last,
# in place; hosts 1 and 2 are copied out first, as in the kubeadm HA etcd guide)
cat > /tmp/etcd0.yaml <<'EOF'
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
etcd:
  local:
    serverCertSANs: ["10.0.0.11"]
    peerCertSANs: ["10.0.0.11"]
    extraArgs:
      - {name: initial-cluster, value: "etcd0=https://10.0.0.11:2380,etcd1=https://10.0.0.12:2380,etcd2=https://10.0.0.13:2380"}
      - {name: initial-cluster-state, value: new}
      - {name: name, value: etcd0}
      - {name: listen-peer-urls, value: "https://10.0.0.11:2380"}
      - {name: listen-client-urls, value: "https://10.0.0.11:2379"}
      - {name: advertise-client-urls, value: "https://10.0.0.11:2379"}
      - {name: initial-advertise-peer-urls, value: "https://10.0.0.11:2380"}
EOF
kubeadm init phase certs etcd-ca
for h in etcd2 etcd1; do
  kubeadm init phase certs etcd-server --config /tmp/$h.yaml
  kubeadm init phase certs etcd-peer --config /tmp/$h.yaml
  kubeadm init phase certs etcd-healthcheck-client --config /tmp/$h.yaml
  kubeadm init phase certs apiserver-etcd-client --config /tmp/$h.yaml
  mkdir -p /tmp/$h && cp -R /etc/kubernetes/pki /tmp/$h/
  find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete   # keep only the CA
  find /tmp/$h -name ca.key -type f -delete                                      # CA key never leaves this host
done
# etcd0 (this host) keeps its certificates in place
kubeadm init phase certs etcd-server --config /tmp/etcd0.yaml
kubeadm init phase certs etcd-peer --config /tmp/etcd0.yaml
kubeadm init phase certs etcd-healthcheck-client --config /tmp/etcd0.yaml
kubeadm init phase certs apiserver-etcd-client --config /tmp/etcd0.yaml
```
Copy each `/tmp/<host>/pki` to the matching host's `/etc/kubernetes/pki` (owned by root). Copy
only `etcd/ca.crt` and `apiserver-etcd-client.{crt,key}` from an etcd host to the first
control-plane node (the HA guide does the same); never `etcd/ca.key`.

## 2. Run etcd as a kubelet static pod on each etcd host
First make the kubelet a service manager for etcd on every etcd host: the kubeadm HA-etcd guide
adds a kubelet configuration with `staticPodPath: /etc/kubernetes/manifests` and a systemd drop-in
(`20-etcd-service-manager.conf`) that overrides `ExecStart`. Then on each host, with that host's
own file:
```bash
kubeadm init phase etcd local --config /tmp/etcd0.yaml     # writes /etc/kubernetes/manifests/etcd.yaml
```

## 3. Point kubeadm at it
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
controlPlaneEndpoint: "k8s-api.example.internal:6443"
etcd:
  external:
    endpoints:
      - https://10.0.0.11:2379
      - https://10.0.0.12:2379
      - https://10.0.0.13:2379
    caFile: /etc/kubernetes/pki/etcd/ca.crt
    certFile: /etc/kubernetes/pki/apiserver-etcd-client.crt
    keyFile: /etc/kubernetes/pki/apiserver-etcd-client.key
```
`kubeadm init --config ...` then joins proceed as normal; kubeadm generates a local etcd static
pod only when no external etcd is configured, so control-plane joins add no etcd members.

## Gotchas
- The kubeadm guide builds a three-host cluster; dual-stack is not supported by etcd.
- External etcd is not backed up by anything Kubernetes-side; schedule `etcdctl snapshot save`
  on the etcd hosts themselves.
- Upgrading etcd is now your job and no longer part of `kubeadm upgrade apply`.
- Ports: the guide needs TCP 2379 (client) and 2380 (peer) reachable between the hosts; restrict
  them to control-plane and etcd hosts.

## Verify
- [ ] `etcdctl --endpoints=... endpoint health --cluster` reports all three healthy from a control-plane node using the apiserver-etcd-client cert.
- [ ] `kubectl -n kube-system get pods` shows **no** `etcd-*` pods (external) and the apiserver is Running.
- [ ] Stopping one etcd host leaves `kubectl get nodes` working (quorum 2/3).

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: per-host v1beta4 `etcd.local` config with `serverCertSANs`, `peerCertSANs` and the `extraArgs` name/value list; `kubeadm init phase certs etcd-ca|etcd-server|etcd-peer|etcd-healthcheck-client|apiserver-etcd-client`; generating HOST0 last and deleting `ca.key` from copied directories; the kubelet service-manager drop-in; `kubeadm init phase etcd local`; the external etcd stanza (`endpoints`, `caFile`, `certFile`, `keyFile`) and the file paths copied to the first control-plane node; no local etcd static pod when external etcd is configured. Wrong and fixed: the original loop copied `ca.key` into every host's directory and deleted host 0's certificates after copying. Removed as unconfirmed: the round-trip latency figure, `--heartbeat-interval` advice, the member-count recommendation and the stacked-to-external migration remark.

Method: documentation only; no commands were run.
