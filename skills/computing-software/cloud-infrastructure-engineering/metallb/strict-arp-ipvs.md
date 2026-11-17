---
id: computing-software.cloud-infrastructure-engineering.metallb.strict-arp-ipvs
name: strict-arp-ipvs
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, strict-arp, ipvs, kube-proxy, kubeadm, configmap, kube-router]
level: practitioner
status: docs-checked
description: "Enable strictARP in kube-proxy IPVS mode before installing MetalLB (Kubernetes 1.14.2 and later), with the kubectl edit and scripted diff/apply commands."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strict ARP for kube-proxy IPVS

If kube-proxy runs in IPVS mode, since Kubernetes v1.14.2 you must enable strict ARP. If kube-router is the service proxy you do not need this: it enables strict ARP by default.

Edit the config:
```bash
kubectl edit configmap -n kube-system kube-proxy
```
Set:
```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  strictARP: true
```
With kubeadm, append the same snippet to your kubeadm-config after the main configuration, separated by `---`.

Automate (preview then apply):
```bash
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl diff -f - -n kube-system

kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
```
`diff` returns nonzero if there is a difference; `apply` returns nonzero on errors only.

## Checked

2026-11-04. Confirmed against the MetalLB Installation page (Preparation section: IPVS strict ARP since Kubernetes v1.14.2, kube-router exception, kubectl edit configmap, KubeProxyConfiguration snippet, kubeadm-config append, both shell snippets and their return-code behaviour). Removed the Verify line; the page does not say whether kube-proxy needs a restart.

Method: documentation only; no commands were run.
