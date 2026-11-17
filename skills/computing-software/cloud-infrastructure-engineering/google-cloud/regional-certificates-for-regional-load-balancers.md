---
id: computing-software.cloud-infrastructure-engineering.google-cloud.regional-certificates-for-regional-load-balancers
name: regional-certificates-for-regional-load-balancers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-manager, regional-certificates, regional-lb-tls, internal-load-balancer, dns-authorization]
level: advanced
status: docs-checked
description: "Attach TLS to regional external and internal Application Load Balancers: regional Certificate Manager certs, DNS authorization and CA Service issuance."
sources: ["https://cloud.google.com/certificate-manager/docs/deploy-google-managed-regional", "https://cloud.google.com/certificate-manager/docs/certificates", "https://cloud.google.com/load-balancing/docs/ssl-certificates", "https://cloud.google.com/load-balancing/docs/ssl-certificates/self-managed-certs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Regional certificates for regional load balancers

Regional ALBs (external and internal) take **regional** Certificate Manager certificates referenced
directly by the target HTTPS proxy with `--certificate-manager-certificates`, or regional Compute
Engine SSL certificates. Google recommends Certificate Manager as the primary tool.

## 1. Google-managed regional cert (public names)
```bash
gcloud certificate-manager dns-authorizations create auth-app --domain=app.example.com \
  --location=europe-west1 --type=PER_PROJECT_RECORD
gcloud certificate-manager dns-authorizations describe auth-app --location=europe-west1   # add the CNAME it shows
gcloud certificate-manager certificates create app-cert --location=europe-west1 \
  --domains=app.example.com --dns-authorizations=auth-app
gcloud compute target-https-proxies create app-proxy --region=europe-west1 \
  --url-map=app-um --url-map-region=europe-west1 \
  --certificate-manager-certificates=projects/<P>/locations/europe-west1/certificates/app-cert
```
A regional Google-managed cert needs a regional DNS authorization in the same region as the cert;
global DNS authorizations do not work with it. One DNS authorization covers a single domain name.
Load balancer authorization is not available for regional certificates.

## 2. Private issuance (CA Service)
Certificate Manager can issue Google-managed certs through CA Service: create a certificate issuance
config that references a CA pool, then `gcloud certificate-manager certificates create ... --issuance-config=<NAME>`.
For a regional cert the CA pool must be in the same region as the certificate.

## 3. Cross-region internal ALB
Certificates for a cross-region internal Application Load Balancer are created with the
`all-regions` scope.

## Gotchas
- The DNS authorization CNAME must be the only record for its DNS name, or issuance and renewal can fail; keep it in place.
- A regional Compute Engine SSL certificate must be in the same region as the regional target proxy; its scope cannot be changed after creation.

## Verify
- [ ] `gcloud certificate-manager certificates describe app-cert --location=europe-west1` shows the cert active; a TLS client check against the VIP shows the expected issuer and SANs.

## Checked
Date: 2026-10-31. Confirmed in the Certificate Manager pages deploy-google-managed-regional and
certificates (regional DNS authorization rules, no load balancer authorization for regional, CA Service
regional CA pool rule, `all-regions` scope for cross-region internal ALB, proxy flag
`--certificate-manager-certificates`) and the load-balancing ssl-certificates pages (Certificate Manager
recommended, regional certificate region match, scope immutable). Commands were checked against the gcloud
reference by the review tooling. Removed unconfirmed claims: "no certificate maps", public CAs cannot issue
internal names, global scope for cross-region certs, and the lack of managed issuance for Compute certificates.
Method: documentation only; no commands were run.
