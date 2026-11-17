---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-chart-testing-ct-and-unittest
name: helm-chart-testing-ct-and-unittest
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, helm-unittest, chart-testing, ct, helm-lint, kind, snapshot-testing, assertion-testing, ci-cd, github-actions, values-matrix, helm-test]
level: practitioner
status: gated
description: "Test Helm charts before release: helm-unittest assertions/snapshots on rendered templates, and chart-testing (ct) lint-and-install against a real kind cluster."
sources: ["helm-unittest README (quintush/helm-unittest)", "helm/chart-testing README", "chart-testing-action (helm/chart-testing-action)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm chart testing — helm-unittest and chart-testing (ct)

**Goal:** catch a broken chart in CI, not in a user's cluster. Two tools cover two
different failure classes and you want both, not one instead of the other.

## 1. `helm-unittest` — fast, offline, template-level
Tests `helm template` output against fixed values **without a cluster**. Install as a
plugin: `helm plugin install https://github.com/helm-unittest/helm-unittest`.
```
mychart/tests/deployment_test.yaml
```
```yaml
suite: deployment
templates: [deployment.yaml]
tests:
  - it: sets replica count from values
    set: {replicaCount: 3}
    asserts:
      - equal: {path: spec.replicas, value: 3}
  - it: requires image.repository
    set: {image.repository: null}
    asserts:
      - failedTemplate: {errorMessage: "image.repository is required"}
  - it: matches golden snapshot
    asserts:
      - matchSnapshot: {}
```
Run: `helm unittest mychart` (the plugin's `untt` binary ran the example suite directly: 3 tests, snapshot written to
`tests/__snapshot__/deployment_test.yaml.snap`; the example's `failedTemplate` test needs a `required` call in the
template, which `helm create` charts lack. helm-unittest 1.2.1's `plugin.yaml` failed to load as a plugin on Helm 4.3.1:
`unknown field "platformHooks"`, so match plugin and Helm versions). Snapshots live in `mychart/tests/__snapshot__/*.snap` —
commit them; a snapshot diff in a PR is exactly the review signal you want when
someone touches a shared `_helpers.tpl`. `helm unittest -u mychart` updates snapshots
— never run `-u` blind in CI, only locally after confirming the diff is intentional.
- Covers: every `if`/`with`/`range` branch, `required` failures, label/selector
  correctness, resource name truncation — anything decidable from rendered YAML alone.
- Does **not** cover: whether the rendered YAML is actually schema-valid for your
  Kubernetes version, or whether it actually applies/reconciles. That's `ct`'s job.

## 2. `chart-testing` (`ct`) — lint, diff-aware, real install
`ct` is the tool behind the `helm/chart-testing-action` GitHub Action.
```bash
ct lint --config ct.yaml                 # helm lint, version check, Chart.yaml schema + yamllint, maintainer validation
# on a bare install also pass --chart-yaml-schema and --lint-conf (the `etc/` files in the release zip)
ct lint-and-install --config ct.yaml      # + installs into the current kube-context
```
`ct.yaml` essentials:
```yaml
chart-dirs: [charts]
chart-repos: [bitnami=https://charts.bitnami.com/bitnami]
target-branch: main
validate-maintainers: false
helm-extra-args: "--timeout 600s"
```
- `ct` selects **changed charts** by file changes under the chart directory versus `target-branch` (run: editing
  only `values.yaml` selected the chart), not by a changed `Chart.yaml` `version`. Version checking is a separate
  lint step (`--check-version-increment`, default true; `--all` and `--charts` disable it, per `ct lint --help`),
  so a forgotten bump is a lint failure, not a silent skip. I could not reproduce the failing case on Windows: `ct`
  3.15.0 printed `Unable to find chart on main. New chart detected.` for an existing chart (gated: unconfirmed, source is paywalled or blocked).
- `lint-and-install` needs a cluster: the standard CI recipe is `helm/kind-action` to
  spin up `kind` first, then `ct lint-and-install` installs the chart for real and
  waits for it to become ready (`--helm-extra-args "--wait --timeout 300s"`),
  catching things unittest can't: CRD ordering, webhook readiness races, actual
  probe/resource validity against the API server's admission (gated: unconfirmed, source is paywalled or blocked).
- Dependencies on charts from another repository go in `chart-repos` (`name=url`), per `ct lint --help`.

## 3. Values matrix coverage
Neither tool tests multiple values files by default. For `ct lint-and-install`, drop
one or more `ci/*-values.yaml` files inside the chart (`ci/default-values.yaml`,
`ci/ha-values.yaml`) — `ct` auto-discovers and installs once per file, which is the
only way to get CI coverage of an alternate configuration (e.g. `replicaCount: 3`,
`ingress.enabled: true`) without hand-rolling a matrix job.

## Gotchas
- `helm-unittest` snapshot tests are brittle to **cosmetic** template changes
  (reordering `nindent` calls) — expect noisy snapshot diffs on refactors; review them
  rather than reflexively re-running `-u`.
- The version check compares against `target-branch` (and `remote`, default `origin`); in a scratch repo with no
  `origin/main` ref, `ct lint` failed with `targetBranch 'origin/main' does not exist`, so fetch the remote or
  set `--remote`/`--target-branch` correctly in CI.
- `kind` clusters in CI default to a single node and no real LoadBalancer — a chart
  depending on an actual cloud LB (status.loadBalancer.ingress) will hang on
  `--wait`; use `NodePort`/`ClusterIP` in the CI values override (gated: unconfirmed, source is paywalled or blocked).
- Both tools run against **rendered output**; neither one exercises `helm.sh/hook`
  Jobs the way a real `helm install` lifecycle would in production (hook ordering,
  `hook-delete-policy`) — `ct lint-and-install` does run real hooks since it's a real
  install, `helm-unittest` does not (`helm template` never executes hooks).

## Verify
- [ ] `helm unittest -f 'tests/**/*_test.yaml' mychart` passes locally and in CI.
- [ ] `ct lint-and-install --config ct.yaml` passes against a freshly booted `kind`
      cluster for every `ci/*-values.yaml` file.
- [ ] Bumping `Chart.yaml` version is enforced: the log shows `Checking chart ... for a version bump...`.
- [ ] Snapshot files are committed and a reviewer actually reads snapshot diffs in PRs
      touching `_helpers.tpl` or shared templates.
