---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-mesh-upgrade-strategy
name: service-mesh-upgrade-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, istio, linkerd, canary-upgrade, revision-tags, proxy-version-skew, rollback, control-plane-upgrade, data-plane-upgrade, istioctl-upgrade]
level: advanced
status: docs-checked
description: "Canary control-plane upgrades with Istio revisions and tags, control/data plane skew limits, Linkerd's in-place upgrade flow, and the rollback plan."
sources: ["https://istio.io/latest/docs/setup/upgrade/canary/", "https://istio.io/latest/docs/setup/upgrade/in-place/", "https://istio.io/latest/docs/releases/supported-releases/", "https://istio.io/latest/docs/setup/additional-setup/gateway/", "https://linkerd.io/2/tasks/upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service mesh upgrade strategy

**Goal:** upgrade the control plane and the hundreds of per-pod proxies it manages without
a mesh-wide outage, and know how far the two can drift. Architecture context in
`istio-control-plane-architecture`.

## 1. Control plane first, canary-style (Istio)
Istio's docs call the revision-based canary upgrade much safer than an in-place upgrade and
the recommended method. Run `istioctl x precheck` first, use the `istioctl` binary that
matches each version, and install the new version as a **revision** alongside the old one:
```bash
istioctl install --set revision=1-31 -f prod-values.yaml   # the old istiod revision keeps running
kubectl label namespace canary-ns istio.io/rev=1-31 istio-injection- --overwrite
kubectl rollout restart deployment -n canary-ns            # re-inject pods with the new proxy
```
- Revision names cannot contain `.`, so use something like `1-31` for 1.31. Revision-based
  upgrades may jump two minor versions at once (in-place upgrades must step through every
  minor release).
- The `istio-injection` label takes precedence over `istio.io/rev`, so remove it when you
  switch a namespace to a revision. Only namespaces labelled with the new revision move;
  the rest keep using the old `istiod`. That subset of real traffic is the canary.
- Prefer **revision tags** for promotion: `istioctl tag set prod-stable --revision 1-30`,
  `istioctl tag set prod-canary --revision 1-31`, label namespaces `istio.io/rev=prod-stable`
  or `prod-canary`, and move a tag with `istioctl tag set prod-stable --revision 1-31
  --overwrite`; restart workloads to pick up the change. `istioctl tag list` shows the
  tags, and `kubectl get ns -L istio.io/rev` shows which namespaces use which revision.
- Promote by moving namespaces (or tags) in batches, watching `istioctl proxy-status`
  (no `STALE`) and error-rate dashboards after each batch. Remove the old control plane with
  `istioctl uninstall --revision <old-revision> -y` once nothing references it.
- **Gateways**: with the default profile, gateways are upgraded in place to the new control
  plane revision. To control the rollout, set the `istio.io/rev` label on the gateway
  Deployment, or run a second gateway Deployment labelled with the canary revision and shift
  traffic by replica counts (Istio's gateway guide describes both).

## 2. Control plane / data plane skew
Istio's support policy: the control plane can be **one version ahead** of the data plane,
but the data plane must not be ahead of the control plane, and Istio recommends using
revisions so there is no skew at all. For in-place upgrades the installed version must be at
most one minor version behind the target. Do not leave a canary half-migrated for long.

## 3. Linkerd's upgrade flow
Linkerd's upgrade guide describes an in-place sequence: upgrade the CLI, then the control
plane, then extensions, then the data plane.
```bash
linkerd check                                  # healthy before you start (add --proxy for major upgrades)
linkerd upgrade --crds | kubectl apply -f -    # CRDs first
linkerd upgrade | kubectl apply -f -
linkerd prune | kubectl delete -f -            # remove resources the new version no longer has
linkerd check
kubectl -n <namespace> rollout restart deploy  # data plane: new pods get the new proxy
```
Helm installs follow the Helm upgrade procedure in Linkerd's install-helm guide. Linkerd
says the control plane may be ahead of the data plane by up to a full version
(for example edge releases within 2.17 or 2.18 for a 2.17 data plane), more is not supported, and data
planes can be upgraded lazily as workloads restart, though new features need the latest
proxy. Stage by restarting a non-critical namespace first and watching `linkerd viz stat`.

## 4. Rollback plan: write it before you upgrade, not during an incident
- Istio: keep the previous revision installed until the new one has soaked. Roll back by
  relabelling namespaces (or moving the tag) back and restarting. If gateways were upgraded
  in place, first reinstall the previous gateways with the old `istioctl` and make sure they
  are running before uninstalling the canary revision, because uninstall does not revert them.
- Linkerd: rollback means reinstalling the previous control plane version and restarting
  data-plane workloads again; stage on low-traffic namespaces first.
- Keep the control-plane and data-plane steps separate for anything business-critical so a
  bad outcome isolates to one layer.

## Verify
- [ ] `istioctl proxy-status` shows no `STALE` proxies after each promotion batch.
- [ ] Gateway revisions were set explicitly if you wanted them to move separately.
- [ ] A rollback command exists and was dry-run tested, not just written down.
- [ ] Control plane/data plane skew is within the supported window (control plane at most
  one version ahead for Istio; within one version for Linkerd), checked against this
  release's docs.

## Checked
2026-10-27. Documentation releases: istio.io docs (main; Istio 1.31.3 for `istioctl tag` source), Linkerd website 2-edge upgrade guide.
Confirmed: revision install, `istio.io/rev` and `istio-injection` precedence, revision tags, two-minor jump rule, `istioctl uninstall --revision`, gateway upgrade and rollback behaviour, skew policy and in-place upgrade rule, Linkerd command sequence (`--crds`, `prune`, `check --proxy`), Linkerd skew rule. `istioctl tag list|set|remove` subcommands exist in the 1.31.3 source.
Method: documentation only; no commands were run.
