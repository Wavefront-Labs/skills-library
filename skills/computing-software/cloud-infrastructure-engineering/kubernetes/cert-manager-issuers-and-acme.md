---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cert-manager-issuers-and-acme
name: cert-manager-issuers-and-acme
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cert-manager, clusterissuer, cert-manager-issuer, acme, letsencrypt, http01, dns01, ingress-tls]
level: practitioner
status: docs-checked
description: "Set up cert-manager Issuers/ClusterIssuers (ACME HTTP-01/DNS-01, CA, Vault) and Ingress TLS, and debug a Certificate stuck not Ready through Order/Challenge objects."
sources: ["https://cert-manager.io/docs/configuration/acme/", "https://cert-manager.io/docs/usage/ingress/", "https://cert-manager.io/docs/usage/gateway/", "https://cert-manager.io/docs/troubleshooting/acme/", "https://letsencrypt.org/docs/rate-limits/", "https://letsencrypt.org/docs/challenge-types/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cert-manager issuers, ACME and Ingress TLS

## Issuer vs ClusterIssuer
`Issuer` is namespaced (secrets it references live in its namespace); `ClusterIssuer` is
cluster-wide and reads its secrets from the **cluster resource namespace** (default
`cert-manager`). Platform teams usually ship ClusterIssuers; tenants get Issuers.

## ACME ClusterIssuer (staging first)
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: {name: letsencrypt-staging}
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: ops@example.com
    privateKeySecretRef: {name: le-staging-account}
    solvers:
    - http01:
        ingress: {ingressClassName: nginx}
    - selector: {dnsZones: ["internal.example.com"]}
      dns01:
        route53: {region: eu-west-1}      # IRSA/workload identity, no static keys
```
Switch `server` to `https://acme-v02.api.letsencrypt.org/directory` only after staging issues.
Let's Encrypt production rate limits bite fast: up to 50 certificates per registered domain every 7 days,
and up to 5 authorization failures per identifier per account per hour.

**HTTP-01** can only be done on port 80 and cannot issue wildcard certificates.
**DNS-01** is required for wildcards and works when port 80 is unavailable; scope the solver to the zone
(for Route 53 the policy needs `route53:ChangeResourceRecordSets`, optionally limited by `hostedZoneID`).

## Ingress TLS
```yaml
metadata:
  annotations: {cert-manager.io/cluster-issuer: letsencrypt-prod}
spec:
  tls:
  - hosts: [app.example.com]
    secretName: app-tls
```
ingress-shim creates a `Certificate` that stores its secret under `tls.secretName`. Gateway API uses the
same `cert-manager.io/issuer` or `cert-manager.io/cluster-issuer` annotation on the `Gateway`, but Gateway
API support must be switched on with the file-based config value `config.gatewayAPI.enabled=true` (Helm)
and the Gateway API CRDs installed before cert-manager starts (or restart the Deployment).

## Debugging a Certificate that never goes Ready
Follow the chain: Certificate → CertificateRequest → Order → Challenge.
```bash
kubectl describe certificate app-tls
kubectl get certificaterequest,order,challenge -n <ns>
kubectl describe challenge <name>     # "Waiting for http-01 challenge propagation: failed to perform self check ..."
cmctl status certificate app-tls -n <ns>
cmctl renew app-tls -n <ns>           # force re-issue
```
Common causes: the HTTP-01 self check fails (the challenge page shows the failed GET); wrong ingress class
on the solver; for DNS-01 with split-horizon DNS, set `--dns01-recursive-nameservers` (and optionally
`--dns01-recursive-nameservers-only`) on the controller; DNS-01 IAM missing
`route53:ChangeResourceRecordSets`.

## Other issuer types
- `ca:` with a `secretName` holding `tls.crt` and `tls.key` (CA certs need `isCA` true) — internal PKI.
- `selfSigned:` — only to bootstrap a CA Certificate (`isCA: true`).
- `vault:` — Vault PKI; see the Vault issuer docs for the supported auth methods.

## Verify
- [ ] `kubectl get clusterissuer` shows `READY True` (ACME account registered).
- [ ] `kubectl get certificate -A` all `True`; `notAfter` > now+30d and renewal scheduled.
- [ ] Alert on certificates nearing expiry using cert-manager's Prometheus metrics (see the metrics page for current names).

## Checked

Documentation release: cert-manager docs (cert-manager/website repo, commit 2026-10-23; cert-manager latest release v1.21.3), Let's Encrypt rate-limit and challenge-type docs.
Confirmed: Issuer vs ClusterIssuer and the Cluster Resource Namespace (defaults to `cert-manager`, flag `--cluster-resource-namespace`); ACME `server`, `privateKeySecretRef`, `solvers`, `selector.dnsZones`; staging and production directory URLs; `http01.ingress.ingressClassName` (added in 1.12); Ingress annotations; Gateway API enablement via `config.gatewayAPI.enabled`; Let's Encrypt limits (50 per registered domain per 7 days, 5 authorization failures per hour); HTTP-01 port 80 and no wildcards; Route53 IAM action; `--dns01-recursive-nameservers`; `cmctl status certificate` and `cmctl renew`; `selfSigned` with `isCA: true`.
Removed because current docs do not cover them: `--enable-gateway-api`, `--acme-http01-solver-nameservers`, the CAA cause, and the `certmanager_certificate_expiration_timestamp_seconds` alert expression.

Method: documentation only; no commands were run.
