---
id: computing-software.cloud-infrastructure-engineering.google-cloud.certificate-manager-and-load-balancer-tls
name: certificate-manager-and-load-balancer-tls
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-manager, managed-certificates, google-managed-ssl, ssl-certificates, tls, ssl-policies, certificate-maps, dns-authorization, load-balancer-authorization, wildcard-certificates, self-managed-certificates, certificate-issuance-config, acme, tls-1-2, tls-1-3, mtls-load-balancer, trust-config, frontend-mtls, http3-quic]
level: practitioner
status: docs-checked
description: "Terminate TLS on Google load balancers: Certificate Manager with DNS authorization and certificate maps, wildcard managed certs, SSL policies, frontend mTLS."
sources: ["https://cloud.google.com/certificate-manager/docs/overview", "https://cloud.google.com/certificate-manager/docs/deploy-google-managed-dns-auth", "https://cloud.google.com/certificate-manager/docs/maps", "https://cloud.google.com/load-balancing/docs/ssl-certificates", "https://cloud.google.com/load-balancing/docs/ssl-policies-concepts", "https://cloud.google.com/load-balancing/docs/mtls", "https://cloud.google.com/certificate-manager/docs/trust-configs", "https://cloud.google.com/certificate-manager/docs/quotas", "https://cloud.google.com/certificate-manager/docs/troubleshooting", "https://cloud.google.com/load-balancing/docs/use-ssl-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate Manager and load balancer TLS

**Goal:** every public hostname on a Google load balancer has a Google-managed certificate
that renews itself, TLS policy rejects legacy protocols, and adding a hostname is a DNS record plus one command.

## 1. Which certificate mechanism
| Mechanism | Use |
|---|---|
| **Certificate Manager** (`gcloud certificate-manager`) with certificate **maps** | anything new: wildcards (DNS authorization only), up to 100 certificates per proxy, regional LBs |
| Classic `compute ssl-certificates --domains` (load-balancer-authorized managed certs) | legacy; no wildcards; a proxy references at most 15 of them, and not a mix with Certificate Manager certificates |
| Self-managed (`--certificate --private-key`) | certs from your own CA/vendor; you own renewal |

## 2. Managed cert via DNS authorization (the pattern)
```bash
gcloud certificate-manager dns-authorizations create example-com-auth --domain=example.com
gcloud certificate-manager dns-authorizations describe example-com-auth --format='value(dnsResourceRecord)'
# → add CNAME _acme-challenge.example.com → <token>.authorize.certificatemanager.goog in Cloud DNS
gcloud certificate-manager certificates create example-wild --domains='example.com,*.example.com' \
  --dns-authorizations=example-com-auth
gcloud certificate-manager maps create web-certs
gcloud certificate-manager maps entries create example-entry --map=web-certs --hostname='*.example.com' --certificates=example-wild
gcloud certificate-manager maps entries create example-apex --map=web-certs --hostname=example.com --certificates=example-wild
gcloud compute target-https-proxies update web-proxy --certificate-map=web-certs
```
- Each map entry binds a hostname to certificates, so certs can be swapped per hostname without touching the proxy.
- State goes `PROVISIONING` → `ACTIVE`; if it stays in `PROVISIONING`, read `managed.provisioningIssue` and `managed.authorizationAttemptInfo`. CAA records must permit `pki.goog` (Google Trust Services).
- `PROVISIONING` also covers renewal; keep the DNS authorization CNAME in place.
- Regional external Application LBs use regional certificates (`--location=europe-west1`).

## 3. SSL policy
```bash
gcloud compute ssl-policies create modern --profile=MODERN --min-tls-version=1.2   # COMPATIBLE is broadest; RESTRICTED targets stricter compliance
gcloud compute target-https-proxies update web-proxy --ssl-policy=modern
```
Without an SSL policy the minimum TLS version can be 1.0, so set one explicitly. A minimum of 1.3 requires the `RESTRICTED` profile; `RESTRICTED` cipher suites exclude TLS 1.0 and 1.1.

## 4. Frontend mTLS (client certificates)
```bash
gcloud certificate-manager trust-configs import partner-trust --source=trust.yaml   # trustStores with trustAnchors (root PEM) and intermediateCas
gcloud network-security server-tls-policies import partner-mtls --location=global --source=policy.yaml
# policy.yaml: mtlsPolicy: {clientValidationMode: REJECT_INVALID | ALLOW_INVALID_OR_MISSING_CLIENT_CERT, clientValidationTrustConfig: projects/P/locations/global/trustConfigs/partner-trust}
gcloud compute target-https-proxies update web-proxy --server-tls-policy=partner-mtls
```
Use `ALLOW_INVALID_OR_MISSING_CLIENT_CERT` first and pass validation results to the backend with custom headers (the mTLS page lists the fields available, such as `client_cert_present`, `client_cert_chain_verified`, `client_cert_error`, `client_cert_sha256_fingerprint`, `client_cert_serial_number` and `client_cert_dnsname_sans`) so the app can enforce per route. Then switch to `REJECT_INVALID`.

## 5. Observe
- `gcloud certificate-manager certificates list --format='table(name,expireTime,managed.state,managed.domains)'`.

## Gotchas
- Wildcard Google-managed certificates are supported only by Certificate Manager with DNS authorization; configure the authorization for the parent domain.
- Verify a certificate is `ACTIVE` before deploying it to a load balancer; it can take several minutes.
- CAA records on the domain must allow `pki.goog`.

## Verify
- [ ] `openssl s_client -connect example.com:443 -servername api.example.com` shows the expected certificate.
- [ ] `openssl s_client -tls1` fails (policy enforced).
- [ ] Certificate `managed.state: ACTIVE`.
- [ ] mTLS: a request without a client cert is rejected with `REJECT_INVALID`; with `ALLOW_INVALID_OR_MISSING_CLIENT_CERT` the backend sees the validation result in the custom headers.

## Checked
2026-10-28. Confirmed on the Certificate Manager overview, DNS authorization, maps, trust-configs, quotas and troubleshooting pages and the load balancer SSL certificates, SSL policies and mTLS pages: wildcard support only with DNS authorization, 15 Compute Engine vs 100 Certificate Manager certificates per proxy, `_acme-challenge` CNAME to `authorize.certificatemanager.goog`, PROVISIONING/ACTIVE states and diagnostic fields, `pki.goog` CAA, profile names, RESTRICTED requirement for minimum TLS 1.3, `--min-tls-version` values, trustStores/trustAnchors/intermediateCas, client validation modes, client certificate field names. gcloud commands and flags passed check_commands. Fixed: header variable names (`client_cert_valid` does not exist), dead map and issuance-config links. Removed: FAILED_* state names, CA Service issuance-config row, renewal timing, metric and log field names, QUIC and keep-alive flags, propagation and chain-format remarks.
Method: documentation only; no commands were run.
