---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-managed-certificate-provisioning
name: troubleshooting-managed-certificate-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-manager-tls, managed-cert-provisioning-failures, failed-not-visible, caa-records, dns-authorization]
level: practitioner
status: docs-checked
description: "Fix Google-managed certificates stuck in PROVISIONING or FAILED: domain status codes, DNS and CAA checks, LB vs DNS authorization, rate limits, and GKE ManagedCertificate."
sources: ["https://cloud.google.com/load-balancing/docs/ssl-certificates/troubleshooting", "https://cloud.google.com/certificate-manager/docs/troubleshooting", "https://cloud.google.com/kubernetes-engine/docs/how-to/managed-certs", "https://cloud.google.com/certificate-manager/docs/deploy-google-managed-dns-auth"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting managed certificate provisioning

## Read the per-domain status
```bash
gcloud compute ssl-certificates describe <CERT> --global --format="get(managed.domainStatus)"
gcloud certificate-manager certificates describe <CERT> --location=global --format="get(managed.authorizationAttemptInfo)"
```
Classic (Compute Engine) certificates, per-domain `managed.domainStatus`:

| Status | Meaning | Fix |
|---|---|---|
| `FAILED_NOT_VISIBLE` | DNS A and AAAA do not resolve only to the load balancer IP (a stray AAAA triggers it); or propagation (up to 72 hours) is incomplete; cert not attached to the target proxy; forwarding rule lacks port 443; or a Certificate Manager certificate map on the proxy takes precedence | fix DNS, attach the cert, add a 443 forwarding rule, or detach the map |
| `FAILED_CAA_CHECKING` / `FAILED_CAA_FORBIDDEN` | CAA record misconfigured, or does not allow the CA Google needs | fix the CAA record as in "Specify the CAs that can issue your Google-managed certificate" |
| `FAILED_RATE_LIMITED` | the CA rate-limited signing requests | provision a new certificate, switch to it, delete the old one, or contact Support |

Managed (certificate-level) status: `PROVISIONING` can take up to 60 minutes after DNS and load balancer changes propagate; if it stays, check the right certificate is on the target proxy. `PROVISIONING_FAILED` is retried; `PROVISIONING_FAILED_PERMANENTLY` is not (create a replacement and delete the failed one). `RENEWAL_FAILED` means a domain no longer points at the load balancer by A/AAAA record; the existing certificate keeps serving until it expires.

Certificate Manager certificates: state `PROVISIONING`, `ACTIVE` or `FAILED` (not retried; delete and recreate after fixing). Per-domain `authorizationAttemptInfo.state` is `AUTHORIZING`, `AUTHORIZED` or `FAILED`; `failureReason` is `CONFIG`, `CAA` or `RATE_LIMITED`. For `CONFIG` read `authorizationAttemptInfo.troubleshooting`: `CNAME_MISMATCH` (DNS authorization CNAME missing or wrong; get the expected record with `gcloud certificate-manager dns-authorizations describe`) and `RESOLVED_TO_NOT_SERVING` (load balancer authorization; A/AAAA must point only at the load balancer).

## Checks
```bash
dig +short www.example.com A; dig +short www.example.com AAAA
dig +short example.com CAA
```
- CAA: for per-project DNS authorizations (including all regional certificates) Certificate Manager uses Google Trust Services only, so allow `pki.goog`; other DNS authorizations and load balancer authorizations can use `pki.goog` and `letsencrypt.org`.
- Load balancer authorization needs the domain to resolve to the load balancer serving the certificate; a proxy or CDN in front hides it, so use DNS authorization instead.
- Overlapping domain sets in a short span are not processed in parallel, and Google issues one managed certificate per domain at a time; attempts with incorrectly configured domains time out after 30 minutes.

## GKE ManagedCertificate
`kubectl describe managedcertificate <name>` shows status; provisioning can take up to 60 minutes. The Ingress needs the
`networking.gke.io/managed-certificates` annotation (comma-separated list) and a reserved static external IP is recommended. GKE managed certificates support up to
100 non-wildcard domains; for wildcards use the Gateway API with Certificate Manager.

## Gotchas
- Deleting and recreating restarts provisioning and can hit CA rate limits.
- Wildcard domains: configure the DNS authorization on the parent domain (Certificate Manager).

## Verify
- [ ] Status ACTIVE for every domain; the certificate then takes up to about 30 more minutes to be usable by a load balancer.

## Checked
Date: 2026-10-28. Confirmed against the load balancer SSL certificate troubleshooting, Certificate Manager troubleshooting, GKE managed certificates and Certificate Manager DNS authorization pages: status values and meanings, 60-minute and 72-hour figures, 30-minute timeout, CAA rules for `pki.goog` and `letsencrypt.org`, `networking.gke.io/managed-certificates` annotation, 100-domain GKE limit, wildcard handling, gcloud commands and flags. Removed: `AUTHORIZATION_ISSUE` and the exact `_acme-challenge` record name (use the value returned by `dns-authorizations describe`), the `curl ... acme-challenge` test, the Cloud Armor and `openssl` remarks.
Method: documentation only; no commands were run.
