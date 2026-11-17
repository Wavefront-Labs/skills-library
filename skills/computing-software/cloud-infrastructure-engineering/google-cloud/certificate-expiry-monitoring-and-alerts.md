---
id: computing-software.cloud-infrastructure-engineering.google-cloud.certificate-expiry-monitoring-and-alerts
name: certificate-expiry-monitoring-and-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, certificate-manager, certificate-monitoring, certificate-expiry-alerts, uptime-checks, tls]
level: practitioner
status: docs-checked
description: "Catch expiring or failed-renewal TLS certificates on GCP: list expiry in Certificate Manager and SSL certs, uptime-check SSL alerts, and managed cert provisioning failures."
sources: ["https://docs.cloud.google.com/monitoring/uptime-checks/ssl-cert-expiry", "https://certificatemanager.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate expiry monitoring and alerts

## 1. Inventory expiries
```bash
gcloud certificate-manager certificates list --location=global \
  --format='table(name.basename(),managed.state,expireTime,sanDnsnames.list())'
gcloud compute ssl-certificates list --format='table(name,type,managed.status,expireTime)'
```
Certificate Manager provisions and renews managed certificates automatically, so self-managed certificates are the
main expiry risk; watch managed ones for provisioning failures (section 3).

## 2. Uptime check SSL alert
Create an HTTPS uptime check per public hostname with **Validate SSL certificates** on (uptime checks fail when the certificate
is invalid, for example expired). Build an alerting policy on the metric
`monitoring.googleapis.com/uptime_check/time_until_ssl_cert_expires`; see "Sample policies: Uptime-check policy" in the
Cloud Monitoring docs for a ready-made condition. Certificates with AIA extensions are not supported by the validation, so
validation must be disabled for them (and expiry is then not checked this way).

## 3. Managed cert renewal failures
- Certificate Manager managed certs: `managed.state` is `PROVISIONING`, `ACTIVE` or `FAILED` (`FAILED` means Certificate Manager gave up;
  delete and recreate to retry). `managed.authorizationAttemptInfo[]` gives per-domain `state` (`AUTHORIZING`, `AUTHORIZED`, `FAILED`),
  `failureReason` (`CONFIG` for DNS or load balancer configuration, `CAA` for a CAA record forbidding issuance, `RATE_LIMITED`) and `details`.
- A scheduled script can flag any managed cert whose `managed.state` is not `ACTIVE`.

## Gotchas
- Endpoints not reachable by public uptime checkers need another check, such as a scheduled job that reads the certificate with `openssl s_client`.

## Verify
- [ ] Alert fires for a test hostname with a short-lived cert; all managed certs report ACTIVE.

## Checked
2026-10-28. Confirmed against the Cloud Monitoring SSL-certificate uptime-check page and the Certificate Manager API v1 discovery document
(`ManagedCertificate.state`, `AuthorizationAttemptInfo.state` and `failureReason`, `Certificate.expireTime`, `sanDnsnames`). Corrected: the
failure values `FAILED_NOT_VISIBLE`, `FAILED_CAA_FORBIDDEN` and `FAILED_RATE_LIMITED` do not exist. Removed: alert YAML and 21-day threshold,
CAA issuer names, `_acme-challenge` claim, Cloud Asset Inventory export, intermediate-pinning note.
Method: documentation only; no commands were run.
