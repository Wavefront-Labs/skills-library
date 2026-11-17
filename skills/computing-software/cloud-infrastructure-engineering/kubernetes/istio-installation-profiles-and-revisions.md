---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-installation-profiles-and-revisions
name: istio-installation-profiles-and-revisions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, istio, service-mesh, istioctl-install, istio-helm-install, istiooperator, revisions, ambient]
level: practitioner
status: docs-checked
description: "Install Istio with istioctl profiles or Helm charts (base, istiod, gateways, ambient), customise via IstioOperator values, and use revisions so upgrades are canaried."
sources: ["https://istio.io/latest/docs/setup/install/istioctl/", "https://istio.io/latest/docs/setup/install/helm/", "https://istio.io/latest/docs/ambient/install/helm/", "https://istio.io/latest/docs/setup/additional-setup/config-profiles/", "https://istio.io/latest/docs/setup/upgrade/canary/", "https://istio.io/latest/docs/reference/commands/istioctl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Istio: profiles, Helm and revisions

## istioctl
```bash
istioctl x precheck
istioctl profile list            # default, demo, minimal, remote, empty, preview, ambient
istioctl install -f istio-config.yaml --revision <revision> -y
kubectl get pods -n istio-system
```
```yaml
# istio-config.yaml — istioctl accepts the IstioOperator API as its input file
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: minimal                # istiod only; deploy gateways separately
  meshConfig:
    accessLogFile: /dev/stdout
    outboundTrafficPolicy: {mode: REGISTRY_ONLY}
    defaultConfig: {holdApplicationUntilProxyStarts: true}
  values:
    pilot: {resources: {requests: {cpu: 500m, memory: 2Gi}}, autoscaleMin: 2}
    global: {proxy: {resources: {requests: {cpu: 50m, memory: 128Mi}}}}
```
The `demo` profile is configuration designed to showcase Istio functionality with modest resource requirements; do not use it for production.

## Helm (GitOps-friendly)
```bash
helm repo add istio https://blob.istio.io/istio-release/charts
helm repo update
helm install istio-base istio/base -n istio-system --create-namespace --set defaultRevision=<revision>
helm install istiod-<revision> istio/istiod -n istio-system --set revision=<revision> -f istiod-values.yaml --wait
helm install istio-ingress istio/gateway -n istio-ingress --create-namespace --wait
# ambient: base, then istiod --set profile=ambient, istio/cni --set profile=ambient, istio/ztunnel
```
Order matters: base (CRDs) → istiod → gateways. CRD upgrades come with `base`.

## Revisions = canary control planes
- Each install has a revision; namespaces opt in with `istio.io/rev=<revision>` (remove
  `istio-injection`, which takes precedence over the revision label).
- Revision **tags** (`istioctl tag set prod --revision <revision>`) let namespaces point at
  `prod`, and you move the tag (`--overwrite`) during upgrades without relabelling everything.
- Upgrade: install new revision alongside, move a test namespace, restart its pods, validate,
  move the tag, rolling-restart the rest, then uninstall the old revision
  (`istioctl uninstall --revision <old-revision>`).

## Gotchas
- Install with a GitOps tool **and** istioctl = fights; pick one.
- Gateways are just Deployments with proxies; run them in their own namespace with HPA/PDB.
- Check the Istio supported-releases page for the Kubernetes versions each release supports before upgrading.

## Verify
- [ ] `kubectl get pods -n istio-system` Ready; `istioctl proxy-status` shows all proxies SYNCED to the intended revision.

## Checked
2026-10-26. Checked against the istio.io docs source (repository istio/istio.io, last commit 2026-10-23). Confirmed: profiles default, demo, minimal, remote, empty, preview, ambient; `minimal` installs only control plane components; the Helm repository is `https://blob.istio.io/istio-release/charts` (the old Google Cloud Storage URL in this skill is not in the current docs); Helm order base, istiod, gateway, and for ambient istiod and cni with `--set profile=ambient` then ztunnel; `defaultRevision` on the base chart for revisioned installs; `istioctl tag set <tag> --revision <rev>` and `istioctl uninstall --revision`; in canary upgrades the `istio-injection` label must be removed because it takes precedence over `istio.io/rev`. Removed as unconfirmed: the `istioctl verify-install` line, the in-cluster operator removal note, the one-minor-at-a-time skew rule and the pinned example revisions.
Method: documentation only; no commands were run.
