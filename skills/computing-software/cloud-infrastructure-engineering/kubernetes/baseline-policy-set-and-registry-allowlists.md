---
id: computing-software.cloud-infrastructure-engineering.kubernetes.baseline-policy-set-and-registry-allowlists
name: baseline-policy-set-and-registry-allowlists
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, policy-engines, baseline-policies, require-labels, disallow-latest-tag, registry-allowlist, allowed-registries, kyverno, gatekeeper]
level: practitioner
status: docs-checked
description: "Ship a baseline admission policy set (required labels, no :latest, requests set, allowed registries, probes) with Kyverno or Gatekeeper, rolled out audit-first with exceptions."
sources: ["https://kyverno.io/policies/best-practices/restrict-image-registries/restrict-image-registries/", "https://kyverno.io/docs/policy-types/overview/", "https://kyverno.io/docs/guides/exceptions/", "https://open-policy-agent.github.io/gatekeeper-library/website/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baseline policy set and registry allowlists

> Kyverno `ClusterPolicy` (`kyverno.io/v1`) is deprecated as of Kyverno v1.19 and removed in v1.20 (estimated Nov 2026); the CEL-based `ValidatingPolicy`/`ImageValidatingPolicy` types (`policies.kyverno.io/v1`) are stable since v1.18. The YAML below is the legacy form still used by the policy library.

## The baseline (beyond Pod Security Standards)
| Policy | Why |
|---|---|
| allowed image registries | stop pulling arbitrary/typosquatted images; enforce mirror use |
| disallow `:latest` / require tag or digest | reproducibility, rollback |
| require `app.kubernetes.io/name`, `team` labels | ownership, cost, alert routing |
| require CPU/memory requests, memory limit | scheduling and node stability |
| require readiness probe on Deployments | safe rollouts |
| disallow `NodePort`/`LoadBalancer` outside allowed ns | network exposure, cost |
| disallow default ServiceAccount use / automount | token hygiene |
| restrict `hostPath`, `hostNetwork` (complements PSS) | node escape |
Pull from the Kyverno policy library / Gatekeeper library; don't write from scratch.

## Registry allowlist (Kyverno)
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: {name: restrict-image-registries}
spec:
  validationFailureAction: Audit          # switch to Enforce after review
  background: true
  rules:
  - name: validate-registries
    match: {any: [{resources: {kinds: [Pod]}}]}
    exclude: {any: [{resources: {namespaces: [kube-system]}}]}
    validate:
      message: "Images must come from registry.internal or ghcr.io/acme"
      pattern:
        spec:
          "=(ephemeralContainers)":
          - image: "registry.internal/* | ghcr.io/acme/*"
          "=(initContainers)":
          - image: "registry.internal/* | ghcr.io/acme/*"
          containers:
          - image: "registry.internal/* | ghcr.io/acme/*"
```
Gatekeeper equivalent: `K8sAllowedRepos` template with `parameters.repos: ["registry.internal/"]`
(prefix match: the library template says to end each entry with `/` to prevent bypasses; `K8sAllowedReposV2`
supports exact and glob-like matches). The template checks containers, init containers and ephemeral containers.
Images written without a registry (`nginx`) do not match a prefix or pattern list, so they are rejected; write the full registry in manifests.
Include init and **ephemeral** containers, or `kubectl debug` bypasses the allowlist.

## Rollout
1. Install in Audit, `background: true` to scan existing resources → PolicyReports
   (`kubectl get polr -A`) / Gatekeeper `status.violations`.
2. Fix or grant **PolicyExceptions** (Kyverno; off by default, enable with the `enablePolicyException` flag and set `exceptionNamespace`) scoped by namespace + name, with expiry noted.
3. Enforce per policy; keep a break-glass procedure (exclude a namespace by label owned by platform).
4. Shift left: run the same policies in CI (`kyverno apply`, `gator test`) on manifests.

## Verify
- [ ] `kubectl run t --image=docker.io/library/nginx:latest -n team-a --dry-run=server` is denied with both messages.
- [ ] PolicyReport fail counts trend to zero before enforcement.

## Checked

Checked 2026-10-27 against Kyverno docs source (kyverno/website, main; policy types overview and sigstore pages describe Kyverno v1.19), the Gatekeeper library (`library/general/allowedrepos`) and the Gatekeeper docs.

- Kyverno policy library "Restrict Image Registries" confirmed: it uses a `pattern` with `eu.foo.io/* | bar.io/*` style alternatives and covers ephemeral, init and regular containers; the foreach/deny form in the earlier text was replaced by that confirmed pattern.
- `K8sAllowedRepos` confirmed: parameter `repos` is a list of prefixes, entries need a trailing `/` to prevent bypasses, ephemeral and init containers are checked; `K8sAllowedReposV2` exists for exact and glob-like matches. Gatekeeper library templates for disallowed tags, required labels, required probes and NodePort/LoadBalancer blocking exist in `library/general`.
- Kyverno ClusterPolicy deprecation (v1.19) and removal (v1.20, estimated Nov 2026), PolicyException being disabled by default (`enablePolicyException`, `exceptionNamespace`), `kubectl get polr`, `kyverno apply --resource` and `gator test` confirmed.

Method: documentation only; no commands were run.
