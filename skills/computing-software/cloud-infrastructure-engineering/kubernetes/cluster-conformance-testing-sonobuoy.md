---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-conformance-testing-sonobuoy
name: cluster-conformance-testing-sonobuoy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sonobuoy, conformance, cncf, e2e-tests, certified-kubernetes, kubernetes-e2e, validation, custom-distribution, bare-metal-validation, certified-conformance-mode]
level: advanced
status: docs-checked
description: "Prove a cluster (custom build, air-gapped, new bare-metal distro) is a genuine conformant Kubernetes using Sonobuoy's CNCF e2e suite, and read its results correctly."
sources: ["https://sonobuoy.io/docs/main/e2eplugin/", "https://sonobuoy.io/docs/main/results/", "https://github.com/vmware-tanzu/sonobuoy/blob/main/site/content/docs/main/cli/sonobuoy_run.md", "https://www.cncf.io/certification/software-conformance/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cluster conformance testing with Sonobuoy

**Goal:** verify a cluster — especially one you built yourself via
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-bootstrap`
or an air-gapped/custom distro — actually behaves like Kubernetes claims to, not just
that `kubectl version` reports the right number. This matters most for custom/bare-metal
builds and new CNI/CSI integrations.

## 1. What conformance testing actually checks
- The CNCF **Certified Kubernetes Conformance** suite is the set of e2e tests marked
  `Conformance` in the Kubernetes e2e tree, run through Sonobuoy's `e2e` plugin.
- It does **not** test performance, scale, specific CNI feature sets beyond the
  baseline, or anything vendor-specific — passing conformance says "this is a real
  Kubernetes," not "this is a fast/secure/production-ready Kubernetes."
- Running it is how you catch a custom build that's quietly non-conformant — a CNI
  misconfiguration that breaks NetworkPolicy semantics, a CSI driver that doesn't honor
  volume resize correctly, a kubeadm config that disabled something load-bearing.

## 2. Running Sonobuoy
```bash
sonobuoy run --mode=certified-conformance --wait
```
- Valid `--mode` values are `certified-conformance`, `conformance-lite`, `non-disruptive-conformance`
  (the **default**) and `quick`. `certified-conformance` runs all `Conformance` tests and is the mode
  used when applying to the CNCF program; some tests may be disruptive, so the docs advise against
  running it on production clusters. `non-disruptive-conformance` runs the Conformance tests known
  not to disturb other workloads. `quick` runs a single simple test, only to check the cluster is
  reachable. Run `sonobuoy modes` to list them.
- Run time depends on cluster size; the timeout is the `--timeout` flag or `Server.timeoutseconds` in the config.
- `--wait` blocks until the run completes or fails (default 1440 minutes when given without a value); otherwise poll with `sonobuoy status`.

## 3. Reading results
```bash
results=$(sonobuoy retrieve)
sonobuoy results $results
```
- Reports **passed / failed / skipped** counts per plugin. Review which tests were skipped
  rather than only the count.
- Any **failed** test on the certified-conformance set means the cluster is not
  conformant, full stop — there's no "mostly passes" for an actual certification claim.
  For a non-certification sanity check, triage failures by whether they implicate core
  behavior (serious) vs an edge case in a rarely-used feature (still worth filing, less
  urgent).
- `sonobuoy results $results --mode=detailed` prints one JSON object per test for scripting;
  other modes are `report` (default), `readable` and `dump`.

## 4. When this is actually worth running
- After building or significantly changing a bare-metal/custom cluster (new CNI, new
  CSI driver, custom kubeadm patches) — this is the main real-world use.
- Before submitting to the CNCF conformance program, if that's an organizational goal.
- After an air-gapped cluster build (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.air-gapped-cluster-bootstrap-and-upgrades`)
  where mirrored images/manifests could have introduced subtle drift from upstream.
- Conformance does not cover cluster hardening; see
  `computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`.

## Gotchas
- Some Conformance tests can be disruptive; use the default `non-disruptive-conformance` mode on shared clusters.
- A cluster that passes conformance can still be badly configured for security or
  performance — conformance is a floor, not a quality bar.
- `sonobuoy delete` after a run removes the Sonobuoy namespaces; `--all` also removes dangling e2e namespaces.

## Verify
- [ ] The run completes and `sonobuoy results` shows 0 failed, or every failure is triaged.
- [ ] Skipped tests are reviewed by name, not just counted — nothing load-bearing was
      silently skipped due to a misconfigured feature gate.
- [ ] `sonobuoy delete` has been run to clean up the test namespace/aggregator after
      results are retrieved.
- [ ] If this is for a certification submission, the run matches the CNCF program's
      current submission requirements (version, mode, submission format).

## Checked

2026-10-26, against Sonobuoy docs in vmware-tanzu/sonobuoy (site/content/docs/main, CLI reference auto-generated 1-Jul-2026; sonobuoy run default image v0.57.5; repo last pushed 2026-10-14). Confirmed: mode names and the default (`non-disruptive-conformance`), `quick` is a single test, certified-conformance is the CNCF-program mode and may be disruptive, `--wait` default, `sonobuoy results` modes, `delete --all`. Wrong: the skill described certified-conformance as safe to run anywhere and omitted conformance-lite and the non-disruptive default. Removed unconfirmed 1-2 hour duration and managed-service certification claims. Re-check the CNCF program's current submission requirements before certifying.

Method: documentation only; no commands were run.
