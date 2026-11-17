---
id: computing-software.cloud-infrastructure-engineering.kubernetes.metrics-server-installation
name: metrics-server-installation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, metrics-server, metrics-server-install, kubectl-top, metrics-api]
level: practitioner
status: docs-checked
description: "Install metrics-server correctly (HA manifest, kubelet address types, TLS without insecure flags, resolution) and confirm the metrics.k8s.io APIService is Available."
sources: ["https://github.com/kubernetes-sigs/metrics-server#installation", "https://github.com/kubernetes-sigs/metrics-server#requirements", "https://github.com/kubernetes-sigs/metrics-server#configuration", "https://github.com/kubernetes-sigs/metrics-server/blob/master/charts/metrics-server/README.md", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-tls-bootstrapping/#client-and-serving-certificates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing metrics-server

## Manifest or Helm
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# HA (2 replicas, PDB, anti-affinity):
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability-1.21+.yaml
# Helm
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server -n kube-system --set replicas=2
```
Pin a release version instead of `latest` in GitOps (the README has a compatibility table of metrics-server versions and Kubernetes versions).

## Args that matter
```yaml
args:
- --cert-dir=/tmp
- --secure-port=10250
- --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
- --kubelet-use-node-status-port
- --metric-resolution=15s
```
These are the args in the project's base deployment manifest. `--kubelet-insecure-tls` makes it
skip verification of kubelet serving certs and is documented as for testing purposes only. The
README requires kubelet certificates signed by the cluster CA: enable the kubelet
`serverTLSBootstrap` field and approve the serving certificate requests (kubelet serving
certificates are not approved automatically).

## Verify
```bash
kubectl get apiservice v1.metrics.k8s.io v1beta1.metrics.k8s.io   # AVAILABLE True
kubectl top nodes
kubectl top pods -A
kubectl -n kube-system logs deploy/metrics-server
```

## Failure signatures
| Log / status | Fix |
|---|---|
| `x509: cannot validate certificate for 10.0.0.5 because it doesn't contain any IP SANs` | kubelet self-signed serving cert: enable serverTLSBootstrap |
| `FailedDiscoveryCheck` on the APIService | apiserver cannot reach metrics-server: the control plane must reach the pod IP and port 10250 (check NetworkPolicy and `hostNetwork` settings) |
| `no metrics known for pod` | pod too new (wait a scrape interval) or kubelet summary API failing |

HPA and `kubectl top` both depend on this APIService.

## Checked

Checked 2026-10-24 against the metrics-server README, base manifests, `manifests/components/high-availability-1.21+`, and Helm chart README and values on GitHub, and the kubelet TLS bootstrapping page in Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- `components.yaml` and `high-availability-1.21+.yaml` release assets, the Helm repo URL `https://kubernetes-sigs.github.io/metrics-server/` and the `replicas` value: README and chart README.
- Container args: base `deployment.yaml` (`--cert-dir=/tmp`, `--secure-port=10250`, `--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname`, `--kubelet-use-node-status-port`, `--metric-resolution=15s`). APIServices `v1` and `v1beta1`: `manifests/base/apiservice.yaml`.
- `--kubelet-insecure-tls` wording and the cluster-CA requirement: README. `serverTLSBootstrap` and manual or controller approval of serving CSRs: kubelet TLS bootstrapping page.

Method: documentation only; no commands were run.
