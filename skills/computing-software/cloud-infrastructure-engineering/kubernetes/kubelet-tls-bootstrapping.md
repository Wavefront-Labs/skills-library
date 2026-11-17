---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-tls-bootstrapping
name: kubelet-tls-bootstrapping
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubelet-tls-bootstrapping, bootstrap-kubeconfig, kubelet, certificates]
level: practitioner
status: docs-checked
description: "How kubelet TLS bootstrapping works (bootstrap token, bootstrap-kubelet.conf, CSR auto-approval) and how to debug a node stuck before registering."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/kubelet-integration/", "https://kubernetes.io/docs/reference/access-authn-authz/node/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet TLS bootstrapping

## The flow
1. `kubeadm join` writes `/etc/kubernetes/bootstrap-kubelet.conf` holding a bootstrap token
   (`<id>.<secret>`, user `system:bootstrap:<id>`, group `system:bootstrappers:kubeadm:default-node-token`;
   default token validity 24 hours, changed with `--token-ttl`).
2. The kubelet starts with `--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf
   --kubeconfig=/etc/kubernetes/kubelet.conf`; the bootstrap file is used only if `kubelet.conf` does not exist, so it
   submits a CSR with signer `kubernetes.io/kube-apiserver-client-kubelet`.
3. kubeadm-created ClusterRoleBindings auto-approve it:
   `kubeadm:kubelet-bootstrap` (create CSRs), `kubeadm:node-autoapprove-bootstrap`
   (approve bootstrap CSRs, for the `system:bootstrappers:kubeadm:default-node-token` group) and
   `kubeadm:node-autoapprove-certificate-rotation` (renewals, for the `system:nodes` group).
4. The kube-controller-manager signs with the cluster CA; the kubelet stores the issued client certificate
   under its `--cert-dir` and writes `/etc/kubernetes/kubelet.conf`. When that file exists the TLS bootstrap is
   finished and kubeadm deletes `bootstrap-kubelet.conf`.

## Debugging a node that never registers
```bash
journalctl -xeu kubelet
kubectl get csr                                  # Pending? Approved but not Issued?
kubectl get secret -n kube-system                # bootstrap-token-<id> Secret still exists?
```
- `Unauthorized` on bootstrap: the token probably expired (default TTL 24 h). Create a new one with
  `kubeadm token create --print-join-command` and re-join after `kubeadm reset`.
- CSR `Approved` but never `Issued`: the controller-manager lacks
  `--cluster-signing-cert-file/--cluster-signing-key-file` (kubeadm sets them to the cluster CA unless external CA
  mode is used) or is down.
- CSR `Pending` forever: the auto-approval ClusterRoleBinding (for example `kubeadm:node-autoapprove-bootstrap`)
  was deleted; recreate it or approve manually with `kubectl certificate approve <name>`.

## Serving certificates
Client certs are auto-approved; serving certs (requested when `serverTLSBootstrap: true`) are not approved by
the core CSR approving controllers, for security reasons. Run a custom approving controller or approve
them manually; a deployment-specific process should only approve CSRs requested by nodes
(`spec.username` of the form `system:node:<nodeName>` with group `system:nodes`).

## Gotchas

## Verify
`kubectl get node <name>` shows the node and `/etc/kubernetes/kubelet.conf` exists. The node identity is
username `system:node:<nodeName>` in group `system:nodes`.

## Checked

2026-10-26: kubernetes.io kubelet TLS bootstrapping page, kubeadm implementation-details and kubelet-integration pages (v1.37 docs, kubernetes/website main 2026-10-25). Confirmed: bootstrap-kubelet.conf and kubelet.conf behaviour, token group and 24 h default TTL, the three ClusterRoleBinding names, signer name, serving-certificate approval policy and node username/group form, signing flags. Removed unconfirmed client-cert file path, clock-skew and cloning remarks, third-party approver and openssl check.

Method: documentation only; no commands were run.
