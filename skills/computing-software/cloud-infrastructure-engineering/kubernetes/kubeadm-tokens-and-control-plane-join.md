---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-tokens-and-control-plane-join
name: kubeadm-tokens-and-control-plane-join
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-token, certificate-key, control-plane-join, upload-certs, bootstrap-token, discovery-token-ca-cert-hash, token-ttl, kubeadm-join]
level: practitioner
status: docs-checked
description: "Manage kubeadm bootstrap tokens (create/list/delete/TTL) and the certificate-key used to add control-plane nodes with --control-plane, including expiry traps."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/", "https://kubernetes.io/docs/reference/access-authn-authz/bootstrap-tokens/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/cmd/token.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm tokens and control-plane join

**Goal:** add worker and control-plane nodes days or months after `kubeadm init`, when the
original token (24h) and certificate-key (2h) are long gone.

## 1. Bootstrap tokens
A token is `<6 chars>.<16 chars>` stored as a Secret `bootstrap-token-<id>` in `kube-system`.
```bash
kubeadm token list                              # id, TTL, usages, groups
kubeadm token create --ttl 1h --print-join-command
kubeadm token create --ttl 0                    # never expires (listed as <forever>); delete after use
kubeadm token delete <id>
kubeadm token generate                          # just prints a random token value, creates nothing
```
The join command needs the CA hash too; recompute it any time:
```bash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null \
  | openssl dgst -sha256 -hex | sed 's/^.* //'
# -> --discovery-token-ca-cert-hash sha256:<that>
```
Token usages: `usage-bootstrap-authentication` (the token can authenticate to the API server) and
`usage-bootstrap-signing` (the token may sign the `cluster-info` ConfigMap).

## 2. Adding a control-plane node
Control-plane joins additionally need the cluster's CA/SA/etcd keys. kubeadm encrypts them into
Secret `kubeadm-certs` with a certificate-key that lives **2 hours**:
```bash
kubeadm init phase upload-certs --upload-certs
# -> [upload-certs] Using certificate key: 0a1b...  (64 hex chars)
kubeadm token create --print-join-command --certificate-key 0a1b...
```
On the new node:
```bash
kubeadm join <lb-endpoint>:6443 --token ... --discovery-token-ca-cert-hash sha256:... \
  --control-plane --certificate-key 0a1b... [--apiserver-advertise-address <this-node-ip>]
```
Without `--certificate-key` you must distribute the certificates to the node yourself before
joining (see "Manual certificate distribution" in the kubeadm HA guide); omit `--upload-certs`
at init time if you prefer that route.

## 3. Expiry traps
| Thing | Lifetime | Fix |
|---|---|---|
| bootstrap token | 24h for the token created by `init`; `--ttl` sets it for new tokens | `kubeadm token create --print-join-command` |
| certificate key and `kubeadm-certs` Secret | 2h by default | `kubeadm init phase upload-certs --upload-certs` |

Regenerate whichever expired and retry; nothing else needs to change.

## 4. Automation
Terraform/Ansible flows usually mint a short-TTL token per node on the first control plane and
pass it via cloud-init. For control-plane joins, run `upload-certs` immediately before each join
in the same pipeline step; do not cache the certificate-key.

## Gotchas
- Adding control-plane nodes requires `controlPlaneEndpoint` to have been set at init (a DNS name
  or load balancer address); kubeadm does not support converting a cluster created without it
  into an HA cluster.
- With the stacked topology the joining control plane adds itself as an etcd member; after a
  failed half-join check `etcdctl member list` before retrying.
- Each token is a Secret in `kube-system`, so anyone who can read those Secrets can read the
  token; avoid `--ttl 0`.
- `kubeadm token create` must run where `/etc/kubernetes/admin.conf` exists (or pass `--kubeconfig`).

## Verify
- [ ] `kubeadm token list` shows the token with the expected TTL and `signing,authentication` usages.
- [ ] After a control-plane join, `kubectl get nodes -l node-role.kubernetes.io/control-plane` lists the node and `etcdctl endpoint status --cluster` shows it as a started member.
- [ ] `kubectl -n kube-system get secret kubeadm-certs` disappears ~2h later (expected).

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: token format `[a-z0-9]{6}.[a-z0-9]{16}`, Secret `bootstrap-token-<id>` in `kube-system`, the `usage-bootstrap-authentication` and `usage-bootstrap-signing` fields, `kubeadm token create --print-join-command --certificate-key` (source: `--certificate-key` requires `--print-join-command`), `--ttl 0` shown as `<forever>`, the 24 hour initial token TTL, the 2 hour certificate-key and `kubeadm-certs` expiry, and the manual certificate distribution section of the HA guide. Removed as unconfirmed: the quoted error messages and the "pre-1.15" history.

Method: documentation only; no commands were run.
