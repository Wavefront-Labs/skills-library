---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-e2e-focus-and-skip
name: kubernetes-e2e-focus-and-skip
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, e2e-focus, ginkgo-focus, kubetest, e2e-test, conformance, label-filter]
level: advanced
status: docs-checked
description: "Run selected upstream Kubernetes e2e tests against a cluster with the e2e.test binary: ginkgo focus/skip regexes and label filters, provider flags, and reading results."
sources: ["https://github.com/kubernetes/community/blob/master/contributors/devel/sig-testing/e2e-tests.md", "https://github.com/kubernetes/kubernetes/blob/release-1.37/test/e2e/framework/test_context.go", "https://github.com/kubernetes/kubernetes/blob/release-1.37/test/e2e/storage/external/README.md", "https://onsi.github.io/ginkgo/#filtering-specs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Kubernetes e2e tests with focus/skip

Use when validating a CNI/CSI change, a custom distro or a fix, and full conformance is too
slow or too broad.

## Get the binary for your server version
Build `e2e.test` from the release tag that matches the cluster
(`make WHAT=test/e2e/e2e.test` in a kubernetes/kubernetes checkout), or run the matching
`registry.k8s.io/conformance:<version>` image with Hydrophone or Sonobuoy. Use the **same
minor** as the cluster; tests assume features of their release.

## Run a focused set
```bash
./e2e.test \
  --kubeconfig=$HOME/.kube/config --provider=skeleton \
  --ginkgo.focus='\[sig-network\].*Services.*should serve a basic endpoint' \
  --ginkgo.skip='\[Serial\]|\[Disruptive\]|\[Flaky\]|\[Feature:.*\]' \
  --report-dir=<results-dir>
```
- `--provider=skeleton` is the generic provider and the fallback when `--provider` is unset;
  cloud providers such as `gce` enable cloud-specific tests.
- Since Kubernetes v1.29 the bracket tags are also Ginkgo v2 labels:
  `--ginkgo.label-filter='Conformance && !Serial'` selects without regular expressions.
- Dry-run a new filter first: Ginkgo's `--dry-run -v` lists what would run (it cannot be
  combined with `-p`).
- `[Serial]` tests must run in a separate serial pass, not in parallel; `[Disruptive]` tests
  count as serial too.

## Useful focus sets
| Goal | Focus |
|---|---|
| CNI change | `\[sig-network\].*(Networking|Services|DNS|NetworkPolicy)` |
| CSI driver | `--storage.testdriver=driver.yaml` with an `External.Storage` focus |
| Conformance subset | `\[Conformance\]` + area regex |

## Reading results
`--report-dir` saves JUnit XML reports (no reports are written when it is empty). Failed tests
keep their namespace when `--delete-namespace-on-failure=false`, handy for debugging. Rerun
one spec by its full name in focus.

## Gotchas
- Tests pull images from upstream test registries; air-gapped runs need
  `--kube-test-repo-list=<file>` (or `KUBE_TEST_REPO_LIST`) to remap registries.
- Clusters with admission policies (Pod Security restricted, Gatekeeper) make tests fail for
  policy, not functionality; exempt test namespaces.
- Do not run `[Disruptive]` tests against production; they restart components or taint nodes.
- `[Flaky]` tests are not run unless a focus or skip is given explicitly.

## Verify
- [ ] Dry run lists the expected spec count; JUnit has 0 failures for the focus set.

## Checked
Checked 2026-10-27 against the kubernetes/community e2e testing guide (`--ginkgo.focus`,
`--ginkgo.skip`, `--ginkgo.label-filter`, labels as Ginkgo v2 labels since v1.29, meanings of
`[Serial]`, `[Disruptive]`, `[Flaky]`, `[Feature:...]`, `make WHAT=test/e2e/e2e.test`), the
e2e framework flags in kubernetes/kubernetes release-1.37 test_context.go (`--provider` with
skeleton fallback, `--report-dir`, `--delete-namespace-on-failure`, `--kube-test-repo-list` /
`KUBE_TEST_REPO_LIST`), the external storage README (`-storage.testdriver`) and the Ginkgo docs
(`--dry-run -v`, not with `-p`). Removed the unconfirmed test tarball download (the v1.37
changelog download tables list no test tarball), the ginkgo `--nodes` invocation and the
`e2e-tests-*` namespace naming.

Method: documentation only; no commands were run.
