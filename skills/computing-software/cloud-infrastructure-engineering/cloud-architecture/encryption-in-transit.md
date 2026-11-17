---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.encryption-in-transit
name: encryption-in-transit
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, encryption-in-transit, tls, tls-1-3, certificate-management, acm, private-ca, cert-manager, mtls, hsts, certificate-expiry]
level: practitioner
status: draft
description: "Encrypt all traffic in transit: TLS policy at edges and internally, managed and private certificates, automated renewal, mTLS, and alerts before expiry."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/protecting-data-in-transit.html", "https://cert-manager.io/docs/", "https://ssl-config.mozilla.org/", "https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encryption in transit and certificate management

## Policy
- External: TLS 1.2 minimum, prefer TLS 1.3; modern cipher suites (Mozilla "intermediate" profile);
  HSTS on web domains. Set via LB/CDN security policies (e.g. ALB `ELBSecurityPolicy-TLS13-1-2-2021-06`,
  Front Door/App Gateway TLS policy, GCLB SSL policies).
- Internal: encrypt service-to-service and to data stores too (zero trust) — enforce TLS on DB
  connections (`rds.force_ssl=1`, Azure SQL enforces TLS, `sslmode=verify-full` on clients),
  Redis TLS, Kafka TLS.
- Deny unencrypted access at resource policies (S3 bucket policy `aws:SecureTransport=false` → Deny).

## Certificates
- Public: managed certificates (ACM, App Service/Front Door managed certs, Google-managed certs)
  with automatic renewal via DNS validation.
- Kubernetes: **cert-manager** with ACME (Let's Encrypt) or private issuers.
- Private PKI for internal names/mTLS: AWS Private CA, Azure Key Vault + CA integration, Google CAS;
  short-lived certs (days) issued automatically beat long-lived manual ones.
- Service mesh issues and rotates workload certificates for mTLS automatically.

## Expiry
Inventory all certificates (incl. those uploaded manually, on appliances, in client trust stores);
alarm at 30/14/7 days (ACM `DaysToExpiry` metric, cert-manager metrics, external TLS monitors).

## Verify
- [ ] External endpoints score A on SSL Labs / testssl.sh; no TLS < 1.2.
- [ ] DB clients verify server certificates (not just encrypt).
- [ ] No certificate expires without an alert firing 30 days prior.
