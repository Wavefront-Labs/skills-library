---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubesec-and-kube-linter-manifest-analysis
name: kubesec-and-kube-linter-manifest-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, image-security, kubesec, kube-linter, static-analysis, ci]
level: practitioner
status: gated
description: "Lint Kubernetes manifests for security and reliability problems with kubesec scores and kube-linter checks in CI, with per-object exceptions."
sources: ["https://github.com/controlplaneio/kubesec", "https://docs.kubelinter.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubesec and kube-linter

## kubesec: risk score per object
```bash
kubesec scan deploy.yaml
docker run -i kubesec/kubesec:v2 scan /dev/stdin < deploy.yaml
```
The kubesec README shows JSON output with a `score` (for example `-30` for a SYS_ADMIN capability), `critical`
items that subtract and `advise` items with selectors such as `containers[] .securityContext .runAsNonRoot == true`.
The exact list of critical and advise rules and their points is not confirmed here: run `kubesec scan --list`
(or read the README table) for the current set. kubesec ships no Windows binary, so none of its commands were run
for this review (gated: unconfirmed, source is paywalled or blocked). `kubesec scan -` and `/dev/stdin` read from stdin, `--format json|table|template` and `--rules`
exist (README). Fail CI below a threshold:
```bash
kubesec scan deploy.yaml | jq -e '.[0].score >= 3'
```

## kube-linter: configurable checks
```bash
kube-linter lint ./k8s/
kube-linter lint ./chart/              # renders Helm charts itself (run: a `helm create` chart was linted, test Pod included)
kube-linter checks list
```
```yaml
# .kube-linter.yaml  (pass with --config .kube-linter.yaml)
checks:
  addAllBuiltIn: true
  exclude: [unset-cpu-requirements]
```
Defaults matter (kube-linter 0.8.3, run on a privileged `nginx:latest` Deployment): the default set reported
`latest-tag`, `no-read-only-root-fs`, `privilege-escalation-container`, `privileged-container`,
`unset-cpu-requirements` and `unset-memory-requirements` (exit status 1), but not `no-readiness-probe`,
`no-liveness-probe`, `run-as-non-root`, `no-anti-affinity` or `dangling-service`. Those exist (`kube-linter checks list`)
and only fire when enabled, for example with `addAllBuiltIn: true`. `--format json|sarif|plain` and `--output` exist.
Per-object exception, with a reason:
```yaml
metadata:
  annotations:
    ignore-check.kube-linter.io/run-as-non-root: "vendor image runs as root; tracked in SEC-123"
```
Checks available (not all on by default): `no-readiness-probe`, `latest-tag`, `privileged-container`,
`no-anti-affinity`, `no-read-only-root-fs`, `dangling-service` (a Service whose selector matches no pod).

## Where they fit
Run in pre-commit and PR CI against rendered manifests (`helm template`, `kustomize build`).
Pair with admission policy so rules are enforced, not just reported.

## Verify
A manifest with `privileged: true` fails kube-linter with exit status 1 (run). The annotation
`ignore-check.kube-linter.io/<check>` silences only that one check (run: with `run-as-non-root` ignored, the other
checks still reported), so a pass needs one annotation per remaining finding, each with a reason. kubesec was not run.
