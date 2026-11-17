---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cis-kubernetes-benchmark-and-kube-bench
name: cis-kubernetes-benchmark-and-kube-bench
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cis-benchmark, kube-bench, kube-bench-targets, cis-eks-benchmark, compliance, node-hardening, managed-kubernetes]
level: advanced
status: docs-checked
description: "CIS Kubernetes Benchmark's control-plane/node/policy structure, running kube-bench correctly against each node role, and why most checks don't apply on managed Kubernetes."
sources: ["https://www.cisecurity.org/benchmark/kubernetes", "https://github.com/aquasecurity/kube-bench", "https://raw.githubusercontent.com/aquasecurity/kube-bench/main/docs/flags-and-commands.md", "https://raw.githubusercontent.com/aquasecurity/kube-bench/main/docs/running.md", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://github.com/aquasecurity/kube-bench/tree/main/cfg"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# CIS Kubernetes Benchmark: reading the scorecard correctly

**Goal:** know what the benchmark checks, run `kube-bench` against the right node roles with the right
benchmark version, and avoid two failure modes: treating "all PASS" as "secure", and treating a long FAIL
list on a managed cluster as actionable when most of it covers components you do not run. The deeper
topics (RBAC, Pod Security, audit logging, encryption at rest) have their own skills.

## 1. Structure (kube-bench `cis-1.9`)
- **1.x Control Plane Node Configuration**: configuration file permissions (1.1), API server flags (1.2),
  controller manager (1.3) and scheduler (1.4).
- **2.x Etcd Node Configuration**.
- **3.x Control Plane Configuration**: authentication and authorization (3.1) and logging (3.2): client
  certificate, service account token and bootstrap token auth for users, audit policy. All Manual.
- **4.x Worker Nodes**: configuration file permissions (4.1), kubelet (4.2), kube-proxy (4.3).
- **5.x Policies**: RBAC and service accounts (5.1), Pod Security Standards (5.2), network policies and
  CNI (5.3), secrets management (5.4), extensible admission control (5.5), general policies (5.7).

Sections 1 and 2 cover components a managed service runs for you. The CIS page publishes separate
benchmarks for EKS, EKS Auto Mode, AKS, AKS Automatic, GKE and GKE Autopilot; use the one for your
platform. Section 4 still applies where you manage the worker nodes yourself. Benchmark versions
change; kube-bench's `cfg` folder lists the versions it ships (for example `cis-1.9`, `cis-2.0`,
`eks-1.8.0`, `gke-1.9.0`).

## 2. Running kube-bench against the right target
```bash
# with no --targets kube-bench works out the targets from the benchmark version and the node
kube-bench run --targets master,etcd,node,policies
kube-bench run --benchmark eks-1.8.0          # a managed-platform profile (pick one listed in cfg/)
kube-bench run --targets node --check 4.2.1,4.2.4
```
`--benchmark` and `--version` are mutually exclusive. The repository's `job.yaml` runs kube-bench as a
Kubernetes Job on whichever node the pod lands on, mounting host directories; a single run therefore
reports one node only. To cover a fleet, run it on every node (a Job pinned to each node, or a DaemonSet)
rather than trusting one result when node configuration varies.

## 3. Reading results
kube-bench has four result states: PASS, FAIL (the test ran and failed, or could not run), WARN (needs
further attention, for example a test you must run manually) and INFO. Its docs note that WARN is not
FAIL, that a Scored test kube-bench cannot run reports FAIL while a Not Scored one reports WARN, and
that some tests labelled Automated must still be run by hand. In `cis-1.9` each check is Automated or
Manual; Manual checks carry `scored: false`.
- A FAIL on apiserver `--anonymous-auth=false` (1.2.1, itself Manual in 1.9) matters because anonymous
  requests get the `system:anonymous` user and `system:unauthenticated` group, and any RBAC binding
  to those grants unauthenticated access.
- WARN on a check you must run by hand means "decide and document", not "broken".
- **Document every accepted FAIL**: the reason (managed-cluster inapplicability, compensating control,
  risk acceptance) and the benchmark version it was reviewed against.

## 4. Automation and drift
- Run kube-bench on a schedule, not once at build time; node images, kubelet flags and RBAC drift.
  kube-bench also has an AWS Security Hub integration (see its docs) for AWS clusters.
- Re-review accepted FAILs when you move to a new benchmark version: ids and checks change.

## Gotchas
- kube-bench inspects configuration files and process arguments, not behaviour. The kubelet reference says
  command-line flags override the config file, so a config-file value can read PASS while a flag changes
  the running behaviour; check both when in doubt.
- Running the generic benchmark against a managed cluster produces a long FAIL list for components you do
  not operate; that wastes review time and trains people to ignore the output.
- Passing the benchmark is a configuration baseline, not protection against application flaws or supply
  chain compromise.

## Verify
- [ ] The benchmark variant matches the hosting model.
- [ ] Node-target checks ran on every node, not from one pod.
- [ ] Every accepted FAIL has a written reason and the benchmark version.
- [ ] kube-bench (or the provider's equivalent) runs on a schedule.

## Checked
2026-10-28. Confirmed: section layout, check ids and Automated/Manual wording against kube-bench
`cfg/cis-1.9` (`master`, `etcd`, `controlplane`, `node`, `policies`) including group titles; `--targets`, `--check`, `--benchmark`,
the `--benchmark`/`--version` exclusion and the Security Hub integration against the kube-bench docs; the
benchmark names on the CIS page; `eks-1.8.0` and `gke-1.9.0` against the `cfg` listing; the `job.yaml`
Job and host mounts against `running.md`; flag-over-file precedence against the kubelet reference.
Also confirmed: the four result states and the WARN/FAIL notes against `flags-and-commands.md`.
Removed: the "v1.9.0 for 1.30" version mapping and `eks-1.4.0` (not in kube-bench's list), the
`--config-dir` example (not documented for kube-bench), the Fargate/Autopilot node claims, the GKE
Security Command Center claim, and the dynamic-kubelet-config and `configz` remarks.
Method: documentation only; no commands were run.
