---
id: computing-software.cloud-infrastructure-engineering.google-cloud.compute-ssl-certificates-and-classic-managed-certs
name: compute-ssl-certificates-and-classic-managed-certs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-manager-tls, compute-ssl-certificates, classic-managed-certificates, target-https-proxy, self-managed-certificates]
level: practitioner
status: docs-checked
description: "Use Compute Engine SSL certificate resources on load balancers: Google-managed vs self-managed certs, attaching to target proxies, zero-downtime rotation, and limits."
sources: ["https://cloud.google.com/load-balancing/docs/ssl-certificates", "https://cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs", "https://cloud.google.com/load-balancing/docs/ssl-certificates/self-managed-certs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute SSL certificates and classic managed certs

Compute Engine SSL certificates (`compute.sslCertificates`, "classic" certificates) are referenced
directly by the target HTTPS/SSL proxy. They remain supported, but Google recommends Certificate Manager
as the primary tool. A target proxy can reference up to 15 Compute Engine SSL certificates, or up to 100
Certificate Manager certificates directly, not a mix of both.

## Google-managed
```bash
gcloud compute ssl-certificates create www-cert --domains=www.example.com,example.com --global
gcloud compute target-https-proxies update web-proxy --ssl-certificates=www-cert --global
gcloud compute ssl-certificates describe www-cert --global
```
The cert stays PROVISIONING until it is attached to a load balancer's target proxy and DNS A (IPv4) and
AAAA (IPv6) records for every domain point only at the load balancer forwarding rule IP; then status
becomes ACTIVE. Provisioning can take up to 60 minutes after DNS propagates.
Issuing CAs are Google's `pki.goog` and `letsencrypt.org`: a CAA record, if you have one, must allow
them (with no CAA record both are allowed). The domain list of an existing managed cert cannot be modified.

## Self-managed
```bash
gcloud compute ssl-certificates create api-cert-2026 --certificate=fullchain.pem --private-key=key.pem --global
```
Key types: ECDSA P-256 is the recommended default; RSA-2048 is available for legacy clients, and ECDSA
P-384, RSA-3072 and RSA-4096 can be used for compliance needs.

## Rotation without downtime
Attach old and new together, then remove old:
```bash
gcloud compute target-https-proxies update web-proxy --ssl-certificates=www-cert,www-cert-v2 --global
# after the new cert is ACTIVE and serving
gcloud compute target-https-proxies update web-proxy --ssl-certificates=www-cert-v2 --global
gcloud compute ssl-certificates delete www-cert --global
```
Certificate selection uses SNI against CN and SAN. With no SNI, or no match, the first certificate in the
proxy's list is served. After a replacement, allow about 15 minutes for it to reach all Google Front Ends.

## Regional LBs
Regional external and internal Application Load Balancers take regional certificates, created with
`--region` and attached with `gcloud compute target-https-proxies update ... --region=<R> --ssl-certificates-region=<R>`.
The certificate region must match the load balancer region; scope cannot be changed after creation.

## Verify
- [ ] A TLS client check (for example `openssl s_client -servername www.example.com`) against the VIP shows the expected chain and expiry.

## Checked
Date: 2026-10-31. Confirmed in the load-balancing pages ssl-certificates, google-managed-certs and
self-managed-certs: 15 and 100 certificate limits, recommendation of Certificate Manager, key types, SNI and
first-certificate rules, DNS A/AAAA and PROVISIONING to ACTIVE behaviour, 60 minute provisioning, CAA and
CA names, immutable domain list, 15 minute propagation, regional flags. Commands were checked against the
gcloud reference by the review tooling. Removed unconfirmed claims: 100 SANs per cert, "full chain"
requirement, "managed regional via Certificate Manager only", and the managed.status format projection.
Method: documentation only; no commands were run.
