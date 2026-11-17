---
id: computing-software.cloud-infrastructure-engineering.kubernetes.linkerd-install-and-trust-anchor-rotation
name: linkerd-install-and-trust-anchor-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, linkerd, linkerd-install, trust-anchor-rotation, service-mesh, mtls, step-cli, cert-manager]
level: advanced
status: docs-checked
description: "Install Linkerd with your own trust anchor and issuer, then rotate an expiring trust anchor with a bundle so meshed traffic keeps mTLS throughout."
sources: ["https://linkerd.io/2-edge/tasks/generate-certificates/", "https://linkerd.io/2-edge/tasks/install-helm/", "https://linkerd.io/2-edge/tasks/manually-rotating-control-plane-tls-credentials/", "https://linkerd.io/2-edge/tasks/automatically-rotating-control-plane-tls-credentials/", "https://linkerd.io/2-edge/tasks/replacing_expired_certificates/", "https://linkerd.io/2-edge/features/automatic-mtls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linkerd install and trust anchor rotation

## Install with explicit certificates
`linkerd install` generates a trust anchor valid for 365 days (and an issuer certificate valid for a year);
when they expire the mesh breaks. With Helm you must supply your own anyway. Certificates must use ECDSA
P-256 (the `step` default). Generate your own:
```bash
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca --no-password --insecure --not-after=87600h
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
  --profile intermediate-ca --not-after=8760h --no-password --insecure \
  --ca ca.crt --ca-key ca.key
```
Install (Helm, production):
```bash
linkerd check --pre
helm repo add linkerd-edge https://helm.linkerd.io/edge
helm install linkerd-crds linkerd-edge/linkerd-crds -n linkerd --create-namespace
helm install linkerd-control-plane linkerd-edge/linkerd-control-plane -n linkerd \
  --set-file identityTrustAnchorsPEM=ca.crt \
  --set-file identity.issuer.tls.crtPEM=issuer.crt \
  --set-file identity.issuer.tls.keyPEM=issuer.key
linkerd check
```
The Helm docs use the edge chart repository above; they also require the Gateway API CRDs to be present
first (used for authorization policy and request routing). Pin the chart version. Store `ca.key` offline;
only the issuer key lives in the cluster.

Better: let cert-manager rotate the issuer. The docs' setup sets `identity.externalCA=true` and
`identity.issuer.scheme=kubernetes.io/tls`, has cert-manager issue a `Certificate` whose `secretName` is
`linkerd-identity-issuer` in the `linkerd` namespace, and uses trust-manager to publish the trust bundle
(a ConfigMap in `linkerd`). cert-manager then rotates the issuer automatically; rotating the trust anchor
still needs manual steps.

## Know the expiries
```bash
linkerd check --proxy          # checks trust roots and issuer are valid for at least 60 days
kubectl -n linkerd get cm linkerd-identity-trust-roots -o jsonpath='{.data.ca-bundle\.crt}' \
  | step certificate inspect --bundle -
```

## Rotate the trust anchor (zero downtime)
1. Create the new anchor `ca-new.crt/key`.
2. Bundle new + old and roll it out:
```bash
step certificate bundle ca-new.crt ca.crt bundle.crt
helm upgrade linkerd-control-plane linkerd/linkerd-control-plane -n linkerd \
  --reuse-values --set-file identityTrustAnchorsPEM=bundle.crt
kubectl -n linkerd rollout restart deploy
kubectl rollout restart deploy -n <each meshed namespace>   # proxies load the bundle
linkerd check --proxy
```
3. Once `linkerd check --proxy` is clean, issue a new issuer cert signed by the **new** anchor and apply it
   (`helm upgrade ... --set-file identity.issuer.tls.crtPEM=issuer-new.crt` and `keyPEM`, or
   `linkerd upgrade`). Wait for the `IssuerUpdated` event
   (`kubectl get events --field-selector reason=IssuerUpdated -n linkerd`), then restart meshed workloads so
   proxies pick up certificates from the new issuer.
4. Finally switch to the new anchor alone (`--set-file identityTrustAnchorsPEM=ca-new.crt`, or
   `linkerd upgrade --identity-trust-anchors-file`) and restart meshed workloads once more.

## Gotchas
- Skipping step 2's workload restart means proxies do not have the bundle that includes the new anchor
  (`linkerd check --proxy` reports "data plane proxies certificate match CA").
- The procedure only applies while the trust anchor is still valid. If a certificate has already expired
  the mesh is in an invalid state: follow the "Replacing expired certificates" guide (no zero-downtime
  guarantee).

## Verify
- [ ] `linkerd check` and `linkerd check --proxy` green; `linkerd viz edges deploy -n app` shows secured edges.

## Checked

Documentation release: Linkerd docs (linkerd/website linkerd.io/content/2-edge, repo commit 2026-10-15; linkerd2 edge release edge-26.10.1).
Confirmed: certificate generation with `step` (root-ca and intermediate-ca profiles, ECDSA P-256, `--not-after`), default 365-day trust anchor and one-year issuer from `linkerd install`, Helm values (`identityTrustAnchorsPEM`, `identity.issuer.tls.crtPEM`/`keyPEM`), `linkerd-crds` then `linkerd-control-plane` charts, `linkerd-identity-trust-roots` ConfigMap key `ca-bundle.crt`, the bundle, issuer and final-anchor rotation order and the `IssuerUpdated` event, the 60-day check, the cert-manager and trust-manager setup values (`identity.externalCA`, `identity.issuer.scheme`).
Corrected or removed: the `linkerd/` Helm repo name (docs use `linkerd-edge`), the "stable releases come from vendors" claim, the multicluster gotcha, and the `linkerd-identity` restart step (the docs restart meshed workloads).

Method: documentation only; no commands were run.
