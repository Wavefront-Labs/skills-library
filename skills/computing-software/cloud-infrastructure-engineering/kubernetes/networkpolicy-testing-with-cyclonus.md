---
id: computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-testing-with-cyclonus
name: networkpolicy-testing-with-cyclonus
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, network-policy, cyclonus, connectivity-matrix, testing, cni-conformance]
level: practitioner
status: docs-checked
description: "Test NetworkPolicy behaviour with cyclonus and connectivity matrices, to explain what a policy set allows and to check a CNI implements the spec."
sources: ["https://github.com/mattfenwick/cyclonus", "https://github.com/mattfenwick/cyclonus/blob/main/docs/command-analyze.md", "https://github.com/mattfenwick/cyclonus/blob/main/docs/command-generate.md", "https://github.com/mattfenwick/cyclonus/blob/main/docs/command-probe.md", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing policies with cyclonus

cyclonus models NetworkPolicies, explains what they allow, and probes real connectivity
between test pods to produce a truth table.

## Explain policies offline
```bash
kubectl get netpol -A -o yaml > policies.yaml
cyclonus analyze --mode explain --policy-path policies.yaml
cyclonus analyze --mode query-traffic --policy-path policies.yaml --traffic-path traffic.json
```
`explain` prints, per target pod selector, the combined ingress and egress peers and ports.
`query-traffic` answers "would A reach B on port P" for traffic you describe.

## Probe the live cluster
`cyclonus analyze --mode probe --probe-path probe.json` runs a synthetic probe from a JSON model, without a
cluster. To probe real pods, use the separate `probe` command; it creates pods in namespaces x, y, z
(pods a, b, c by default) and, if `--policy-path` is given, creates that policy in the cluster:
```bash
cyclonus probe --policy-path policy.yaml --probe-mode service-name
```
Or run the conformance generator, which creates the namespaces and pods, installs generated policies one
at a time and compares measured connectivity with expected connectivity. The project's quickstart runs it
as a Kubernetes Job (`./cyclonus generate`) bound to a ServiceAccount with a cluster-admin
ClusterRoleBinding, or you can run it from a release binary:
```bash
cyclonus generate --include=conflict,peer-ipblock,upstream-e2e \
  --exclude=sctp --noisy --ignore-loopback --perturbation-wait-seconds=5
```
Passing `--exclude` replaces the default exclude list (`multi-peer`, `upstream-e2e`, `example`,
`end-port`). Output is a truth table of expected vs actual connectivity per pod pair and a pass
rate per tag; mismatches point to CNI bugs or unsupported features.

## Gotchas
- Run the generator only in a test cluster; it creates and deletes many policies.
- Results depend on timing; the CNI needs a few seconds to program rules.

## Checked

2026-10-27. Release: cyclonus repository docs (main), October 2026
- Confirmed `cyclonus analyze` modes (`parse,explain,lint,query-traffic,query-target,probe`), the `--policy-path` and `--traffic-path` flags, and that analyze runs without a cluster (cyclonus command-analyze docs).
- Corrected live probing: `analyze --mode probe` is a synthetic probe from `--probe-path`; probing a real cluster is the separate `cyclonus probe` command (command-probe docs). Confirmed the `generate` flags used, the default x, y, z namespaces and a, b, c pods, that `--exclude` overrides a default list containing `upstream-e2e`, and the Job-based quickstart with a cluster-admin binding.
- Removed the hand-written `nc` connectivity loop, which no source covers; the timing gotcha matches the documented `--perturbation-wait-seconds` flag.

Method: documentation only; no commands were run.
