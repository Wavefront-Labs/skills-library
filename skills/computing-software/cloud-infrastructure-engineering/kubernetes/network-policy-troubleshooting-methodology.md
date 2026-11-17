---
id: computing-software.cloud-infrastructure-engineering.kubernetes.network-policy-troubleshooting-methodology
name: network-policy-troubleshooting-methodology
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, troubleshooting, debugging, calico, cilium, hubble, connectivity, ephemeral-container]
level: advanced
status: docs-checked
description: "A repeatable method for 'why is this connection blocked/allowed' — isolate DNS vs policy vs routing, read the CNI's own verdict, and avoid the three most common false leads."
sources: ["https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container", "https://docs.cilium.io/en/stable/security/policy/troubleshooting/", "https://docs.cilium.io/en/stable/observability/hubble/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network policy troubleshooting — a method, not a guess

**Goal:** stop guessing at YAML and follow a deterministic sequence that isolates whether a
broken connection is DNS, policy, routing, or the app itself — in that order, because each
later layer is invisible until the earlier ones are ruled out.

## 1. The ordering law: DNS → routing → policy → app
Fixing policy first is the most common wasted hour: if DNS resolution itself fails, every
symptom looks identical to a policy block (connection just hangs/times out). The Kubernetes
docs warn that a default deny-all egress policy also blocks DNS, so check name resolution
and reachability *before* editing NetworkPolicy YAML.

## 2. Step 1 — test from a pod that the policy actually selects
A test pod only proves something if the policy selects it the way it selects the real client:
same namespace and same labels. Two ways to get that:
- `kubectl exec` into the real client pod if it has a shell, or
- add an ephemeral debug container to the real pod with `kubectl debug -it <pod> --image=<image with
  network tools> --target=<container>` (the Kubernetes "debug running pods" page documents ephemeral
  containers); the debug container runs inside the client pod, so it has the pod's IP and labels.

From there test in layers: resolve the name, open a bare TCP connection to the port, then make the
application request. A TCP connect timeout with DNS resolved correctly narrows the problem to
routing or policy. A TCP connect that succeeds while the application request fails narrows it to
the app layer (path, TLS, auth), not the network.

## 3. Step 2 — ask the CNI what it decided, don't infer from the client
A client-side timeout looks the same whether the cause is a policy drop or a routing problem, so
use the CNI's own tooling:
```bash
# Cilium: flows dropped between two pods (Hubble CLI)
hubble observe --from-pod <ns>/<client-pod> --to-pod <ns>/<server-pod> --verdict DROPPED -f
# Cilium: which policy rules an endpoint has realised (cilium-dbg runs inside the cilium-agent container)
cilium-dbg endpoint list
cilium-dbg endpoint get <endpoint-id>
cilium-dbg policy get
# Calico: the policies in the namespace
calicoctl get networkpolicy -n <ns> -o yaml
```
Cilium's policy troubleshooting page pairs `cilium-dbg endpoint get` (the `derived-from-rules` labels
of the realised policy) with `cilium-dbg policy get` to show the exact source rule behind an
allow. Other CNIs have their own tooling; use it rather than inferring from timeouts.

## 4. Step 3 — the classic false leads
1. **`from`/`to` AND vs OR.** A single list entry with both `namespaceSelector` and `podSelector`
   selects pods with that label in namespaces with that label (AND); two separate list entries
   are an OR. The Kubernetes docs call out the YAML-indentation pitfall and suggest
   `kubectl describe` to see how Kubernetes interpreted the policy.
2. **Wrong direction.** `policyTypes` says which directions a policy isolates. If it is not set,
   `Ingress` is always set and `Egress` is set only if the policy has egress rules; with an
   explicit `policyTypes: [Ingress]`, an `egress:` block is not enforced as an egress policy.
3. **The traffic doesn't arrive from the address you think.** Cluster ingress and egress mechanisms
   often rewrite source or destination IPs, and the Kubernetes docs say it is not defined whether that
   happens before or after NetworkPolicy processing; behaviour varies by network plugin, cloud
   provider and Service implementation. Allow by the label or namespace of the component that
   actually connects (for example the ingress controller's pods), and verify with the CNI's flow
   data what source it sees.

## 5. Step 4 — default-deny side effects
After applying any default-deny NetworkPolicy, re-test:
- DNS egress to the cluster DNS service (the DNS pods usually carry `k8s-app=kube-dns`; confirm in your cluster).
- Metrics scraping: the scraper needs an explicit ingress allow once the target is isolated for ingress.
- Probes: the Kubernetes docs state that traffic to and from the node where a pod runs is always
  allowed, so kubelet probes are not blocked by a NetworkPolicy; if probes fail after a policy change, look at the
  application or the CNI instead.

## Debug routine (condensed)
```bash
kubectl get networkpolicy -A
kubectl get pod <client> -n <ns> --show-labels      # confirm the selectors match
kubectl describe networkpolicy <name> -n <ns>        # how Kubernetes interpreted it
hubble observe --verdict DROPPED -f                  # if the CNI is Cilium
```

## Verify
- [ ] DNS resolution confirmed working from the actual client pod/labels before any policy
  change was made.
- [ ] The CNI's own verdict tool (not client-side timeout) was used to confirm cause.
- [ ] After any default-deny rollout, DNS and metrics scraping were explicitly re-tested,
  not assumed fine.
- [ ] The fix was re-verified by reproducing the original failing request, not just
  by reading the new YAML and assuming correctness.

## Checked
Checked 2026-10-24 against the kubernetes/website Network Policies page (default-deny DNS caution,
AND/OR selectors, `policyTypes` defaults, node traffic always allowed, address rewriting caveat), the
"Debug Running Pods" page (ephemeral containers via `kubectl debug --target`), the Cilium Hubble CLI
help (`--from-pod`, `--to-pod`, `--verdict DROPPED`) and the Cilium policy troubleshooting page
(`cilium-dbg endpoint get`, `cilium-dbg policy get`). Removed: `cilium policy trace` (no such
subcommand in the current `cilium-dbg policy` reference) and iptables chain-name details that no
documentation covers.
Method: documentation only; no commands were run.
