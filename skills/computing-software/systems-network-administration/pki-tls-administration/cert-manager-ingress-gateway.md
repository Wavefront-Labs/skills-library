---
id: computing-software.systems-network-administration.pki-tls-administration.cert-manager-ingress-gateway
name: cert-manager-ingress-gateway
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cert-manager-ingress-gateway, pki-cert-manager, cert-manager, ingress, gateway-api, kubernetes, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Request certificates from Ingress annotations or Gateway listeners with cert-manager: supported annotations, listener rules and HTTP-01 class settings."
sources:
  - https://cert-manager.io/docs/usage/ingress/
  - https://cert-manager.io/docs/usage/gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cert-manager with Ingress and Gateway
Goal: certificates created automatically from existing routing objects.
```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts: [app.example.com]
    secretName: app-tls
```
Ingress:
- The ingress-shim watches Ingresses; with a supported annotation it ensures a Certificate named after `tls.secretName` exists in the Ingress's namespace. `tls.hosts` determine the subjectAltNames. At least `cert-manager.io/issuer` or `cert-manager.io/cluster-issuer` must be set, or no Certificate appears (the old `kubernetes.io/tls-acme: "true"` also works if a default issuer is configured via `ingressShim.defaultIssuer*` Helm values).
- `cert-manager.io/issuer` is for namespaced and external issuers (add `cert-manager.io/issuer-kind` and `issuer-group` for out-of-tree issuers); a namespaced Issuer must be in the Ingress's namespace. `cluster-issuer` refers only to cert-manager.io ClusterIssuers.
- HTTP-01 solver class: `acme.cert-manager.io/http01-ingress-class` or `acme.cert-manager.io/http01-ingress-ingressclassname` override the Issuer's `http01.ingress.class` / `ingressClassName`. By default a separate Ingress is created for the challenge; `acme.cert-manager.io/http01-edit-in-place: "true"` modifies the existing one and adds a temporary certificate.
- Other annotations map to Certificate fields: `cert-manager.io/common-name`, `duration`, `renew-before`, `usages`, `private-key-algorithm` (RSA default, ECDSA, Ed25519), `private-key-size` (RSA 2048 default; ECDSA 256 default), `private-key-rotation-policy` (`Always` by default, or `Never`).
- Several Ingresses need unique `tls.secretName` values.
Gateway API:
- cert-manager 1.15+ supports Gateway as beta and it is no longer behind a feature flag, but you must enable it: Helm `config.gatewayAPI.enabled=true`. Install the Gateway API CRDs before cert-manager starts, or restart the cert-manager Deployment afterwards.
- Annotate the Gateway with `cert-manager.io/issuer` or `cert-manager.io/cluster-issuer`. A listener produces a Certificate only if it has a non-empty `hostname`, `tls.mode: Terminate` (Passthrough is skipped), a `certificateRefs` name, kind `Secret` (if given), group core (if given) and no cross-namespace reference. Secrets are created in the Gateway's namespace only.
- Listeners sharing a Secret name get one Certificate with de-duplicated `dnsNames`.
- ListenerSet support is alpha (1.20) and needs extra Helm settings; check the page before using it.
Verify:
- [ ] A Certificate named after the Secret exists and becomes Ready.
- [ ] `openssl s_client -connect HOST:443 -servername app.example.com` shows the new certificate.

## Checked
Confirmed 2026-11-08 against the cert-manager "Annotated Ingress resource" and "Annotated Gateway resource" pages. Removed (not on those pages): the claim that wildcards need dns-01, trust-manager and reflector advice, the rate-limit and staging advice, the global-redirect gotcha and the `kubectl get challenges` check. The `--enable-gateway-api` flag was replaced with the documented Helm setting.
Method: docs-only read of cited pages, 2026-11-08
