---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cilium-install-and-connectivity-test
name: cilium-install-and-connectivity-test
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cilium, cilium-connectivity-test, cni-installation, cni]
level: practitioner
status: docs-checked
description: "Install Cilium with the cilium CLI or Helm, check health with cilium status, and validate the datapath with cilium connectivity test before taking traffic."
sources: ["https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/", "https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/", "https://docs.cilium.io/en/stable/operations/system_requirements/", "https://docs.cilium.io/en/stable/observability/hubble/hubble-ui/", "https://docs.cilium.io/en/stable/network/concepts/routing/", "https://github.com/cilium/cilium/blob/main/cilium-cli/cli/connectivity.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cilium install and connectivity test

## Install
```bash
cilium install --version <chart-version> \
  --set ipam.mode=kubernetes \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost=k8s-api.example.internal --set k8sServicePort=6443
```
With `kubeProxyReplacement=true` on a fresh cluster, run `kubeadm init --skip-phases=addon/kube-proxy`
and set `k8sServiceHost/Port` (the agent cannot use the Service VIP without kube-proxy).
GitOps: the same values via `helm install cilium cilium/cilium -n kube-system`.

## Health
```bash
cilium status --wait
cilium status --verbose | grep -iE 'kubeproxyreplacement|ipam|masquerading|encryption'
kubectl -n kube-system exec ds/cilium -- cilium-dbg status
```
All agents OK, operator OK. Pods that started before Cilium are unmanaged; `cilium install`
reports and restarts them (the install guide shows its "Restarted unmanaged pod" output), so
plan for those restarts.

## Connectivity test
```bash
cilium connectivity test                          # creates a cilium-test-<n> namespace and runs the scenarios
cilium connectivity test --test '!/pod-to-world'  # '!' skips tests matching the expression, for example internet tests
cilium connectivity test --single-node            # limit to tests that can run on a single node
```
Run it after install, upgrades and CNI config changes. Delete the `cilium-test-*` namespace
afterwards if the tool leaves it behind.

## Common failures
- `pod-to-world` failing: check egress firewalling and masquerading.
- Cross-node failing with VXLAN: UDP 8472 must be open between all nodes.
- Native routing: routes between nodes are needed; `auto-direct-node-routes: true` only works when nodes share an L2 network.

## Verify Hubble too
`cilium hubble enable --ui` then `hubble observe --verdict DROPPED` during the test.

## Checked
2026-10-26. Checked against the Cilium documentation source and the cilium-cli source (repository cilium/cilium, last commit 2026-10-25). Confirmed: `cilium install --version`, `cilium status --wait`; `kubeadm init --skip-phases=addon/kube-proxy` with `k8sServiceHost` and `k8sServicePort`; `cilium-dbg status`; `cilium connectivity test` flags `--test` (regular expressions, a leading `!` skips, scenarios such as `/pod-to-cidr`) and `--single-node`; the test namespace is `cilium-test-<n>` by default; VXLAN uses UDP 8472; `auto-direct-node-routes` needs L2 connectivity between nodes; `cilium hubble enable --ui`. Removed as unconfirmed: the pinned 1.17.6 version, the `--status --brief` flag, the blanket pod-deletion command and the cleanup label selector.
Method: documentation only; no commands were run.
