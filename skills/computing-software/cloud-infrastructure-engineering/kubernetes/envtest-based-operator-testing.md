---
id: computing-software.cloud-infrastructure-engineering.kubernetes.envtest-based-operator-testing
name: envtest-based-operator-testing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, envtest, controller-runtime, ginkgo, gomega, setup-envtest, kubebuilder-testing, integration-test, kind, fake-client, eventually-assertions, test-environment, kubeapiserver, etcd]
level: advanced
status: docs-checked
description: "Test operators against envtest: a real kube-apiserver+etcd with no kubelet/scheduler, Ginkgo Eventually-based assertions, and what it can't catch (no real pods running)."
sources: ["https://book.kubebuilder.io/reference/envtest", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/envtest", "https://github.com/kubernetes-sigs/controller-runtime/tree/main/tools/setup-envtest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# envtest-based operator testing — a real API server, no kubelet, fast enough for CI

**Goal:** catch the bugs unit tests miss (CRD schema rejecting your own test
fixtures, RBAC gaps, a reconciler that works against a mock but not a real
optimistic-concurrency API) without the cost and flakiness of a full kind/minikube
cluster per test run.

## 1. What envtest actually is
`sigs.k8s.io/controller-runtime/pkg/envtest` starts a local control plane of a real
`kube-apiserver` and `etcd` (no kubelet, no controller-manager or other built-in
controllers — pods you create never actually run; their status never changes
from `Pending` unless you fake it). The package loads the binaries from
`/usr/local/kubebuilder/bin` or `KUBEBUILDER_ASSETS`; downloading them is the job of
`setup-envtest` (which `make test` calls). Your controller runs as a normal Go process
against this real API server. This means:
- Real CRD validation, real admission webhooks (if you wire them —
  `envtest.Environment.WebhookInstallOptions`), real optimistic-concurrency
  conflicts, real watch/informer behavior.
- **Not real**: pod scheduling, container execution, node status, anything that
  depends on kubelet or a CNI. If your operator's correctness depends on "and then
  the pod actually starts," envtest can't prove that — you need a real cluster
  (kind) or a separate e2e tier for that slice.

## 2. Setup
```bash
# Kubebuilder's Makefile installs setup-envtest into ./bin (make envtest)
./bin/setup-envtest use <k8s-version>      # downloads kube-apiserver/etcd/kubectl binaries
export KUBEBUILDER_ASSETS="$(./bin/setup-envtest use <k8s-version> -p path)"
go test ./... -ginkgo.v
```
Kubebuilder-scaffolded `suite_test.go` wires this via `envtest.Environment{
CRDDirectoryPaths: []string{filepath.Join("..", "..", "config", "crd", "bases")}}`
— point it at the generated CRD YAML (run `make manifests` first, or the suite
tests against a stale schema silently).

## 3. The Ginkgo pattern and why `Eventually` is mandatory
```go
var _ = Describe("Widget controller", func() {
    It("sets Ready when the dependency exists", func() {
        Expect(k8sClient.Create(ctx, dep)).To(Succeed())
        widget := &appsv1.Widget{...}
        Expect(k8sClient.Create(ctx, widget)).To(Succeed())

        Eventually(func(g Gomega) {
            updated := &appsv1.Widget{}
            g.Expect(k8sClient.Get(ctx, key, updated)).To(Succeed())
            g.Expect(meta.IsStatusConditionTrue(updated.Status.Conditions, "Ready")).To(BeTrue())
        }, "10s", "100ms").Should(Succeed())
    })
})
```
The controller runs in a background goroutine against the same API server, fully
asynchronously — there is no "wait for reconcile to finish" hook. Every assertion
about controller-caused state must be wrapped in `Eventually` (poll-until, with
timeout and interval), never a direct `Expect` right after `Create`/`Update`. A
direct `Expect` reads before the controller's reconcile has necessarily run and is
the single most common source of flaky envtest suites.

## 4. Isolation between tests
Each `It` should use a **unique namespace** (create one in `BeforeEach`, defer
delete) rather than sharing one — envtest doesn't reset state between tests within
a suite run, and leftover objects from a previous (possibly failed) test cause
cross-contamination that looks like a flake but is actually ordering-dependent
pollution. Envtest does not support namespace deletion: the delete appears to succeed, but the
namespace stays in `Terminating` and cannot be recreated. Don't rely on "the namespace is gone
so its contents are gone" as a cleanup mechanism; create a new namespace per test and delete
objects explicitly, and make the reconciler ignore other tests' namespaces if needed.

## 5. What to still cover elsewhere
- **Unit tests** (no envtest, pure Go, fake clientset or `sigs.k8s.io/controller-runtime/pkg/client/fake`)
  for pure logic (desired-state computation, defaulting math) — faster than
  envtest, use them for anything not needing real API-server semantics.
- **e2e on a real cluster** (kind, or a CI ephemeral cluster) for anything
  touching pod scheduling, actual container behavior, node resources, storage
  provisioning, or multi-controller interaction with built-in controllers
  (Deployments actually rolling out pods). Keep this tier separate from envtest's `make test`.
- envtest is the right default tier for "does my reconciler do the right thing
  against the real API semantics" — most operator bugs live here, not in e2e.

## Gotchas
- Pick the `setup-envtest` Kubernetes version to match your target cluster; testing behavior
  that depends on a newer API server feature against old binaries gives a false negative.
  The book also notes `ENVTEST_K8S_VERSION` must match the setup-envtest you downloaded.
- CRD YAML not regenerated (`make manifests` stale) means envtest validates
  against an outdated schema — a test "passing" by accepting an object the real
  cluster would reject. Always regenerate before running the suite in CI.
- Running controllers from multiple `Describe` blocks against the same manager
  instance without per-test namespace scoping causes watch/reconcile cross-talk
  that's hard to debug — one manager per suite, one namespace per test is the
  stable pattern.
- Webhooks in envtest are configured through `WebhookInstallOptions` (see the package docs);
  don't assume cert-manager is present in the test control plane.

## Verify
- [ ] `make test` runs the full envtest suite without requiring a real cluster or
      network access (binaries are pre-downloaded by `setup-envtest`).
- [ ] Every assertion depending on controller behavior uses `Eventually`, not a
      bare `Expect` immediately after a mutating call.
- [ ] Running the suite twice in a row (no `go clean -testcache`) produces the
      same result — no ordering-dependent flakiness from shared namespaces.
- [ ] A deliberately invalid test fixture (violates a CRD validation rule) is
      rejected by `Create`, proving the real schema is loaded, not a stub.

## Checked
2026-10-26. Checked against the Kubebuilder book envtest reference and the controller-runtime envtest package docs (repositories kubernetes-sigs/kubebuilder, last commit 2026-10-25, and kubernetes-sigs/controller-runtime, last commit 2026-10-19). Confirmed: envtest starts a local control plane of etcd and kube-apiserver with no kubelet or controller-manager; the envtest package loads binaries from `/usr/local/kubebuilder/bin` or `KUBEBUILDER_ASSETS` and does not download them (`setup-envtest` and `make test` do); `setup-envtest use <version>` and `-p path`; `ENVTEST_K8S_VERSION` must match the setup-envtest you downloaded; `CRDDirectoryPaths`; namespace deletion is unsupported (the namespace stays Terminating and cannot be recreated), so use a new namespace per test; `WebhookInstallOptions` exists for webhook tests. Corrected: the package does not download binaries. Removed as unconfirmed: the real-RBAC claim, the locally minted webhook certificate claim, the `@latest` install, the pinned version and the `make test-e2e` scaffold claim.
Method: documentation only; no commands were run.
