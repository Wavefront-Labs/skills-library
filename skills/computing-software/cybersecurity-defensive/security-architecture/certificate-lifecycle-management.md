---
id: computing-software.cybersecurity-defensive.security-architecture.certificate-lifecycle-management
name: certificate-lifecycle-management
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, certificate-lifecycle-management, certificate-inventory, acme, cert-manager, certificate-expiry-monitoring, 47-day-certificates, automated-renewal, clm]
level: practitioner
status: draft
description: "Run certificate lifecycle management: discover and inventory certificates, automate issuance and renewal (ACME, cert-manager), monitor expiry and plan for shorter TLS lifetimes."
sources: ["CompTIA Security+ SY0-701 objective 1.4 (certificates)", "RFC 8555 ACME protocol", "CA/Browser Forum ballot SC-081 (TLS certificate validity reduction schedule to 47 days)", "cert-manager documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate lifecycle management

**Goal:** no outage from an expired certificate, no unknown certificates, and renewal that is
automatic before public TLS validity drops to 47 days.

## Context
CA/Browser Forum ballot SC-081 reduces maximum public TLS certificate validity in steps:
200 days from March 2026, 100 days from March 2027 and 47 days from March 2029 (with
shorter domain-validation reuse). Manual renewal will not scale.

## Steps
1. **Discover**: scan networks for TLS endpoints (e.g. `nmap --script ssl-cert -p 443,8443 <ranges>`),
   query Certificate Transparency logs for your domains (crt.sh), export from CAs, cloud
   certificate managers and load balancers, and internal CA databases.
2. **Inventory**: subject/SANs, issuer, expiry, key type, location (host, LB, app), owner, renewal method.
3. **Automate**:
   - Public: ACME clients (certbot, lego, acme.sh, Caddy built-in) with DNS-01 for wildcards/internal hosts.
   - Kubernetes: cert-manager `Certificate` resources with ACME or internal CA issuers.
   - Cloud: AWS ACM, Azure Key Vault auto-renew, Google-managed certificates on load balancers.
   - Internal: ACME on the internal CA (step-ca, AD CS via third-party ACME), autoenrolment for Windows.
4. **Deploy** renewed certs automatically (reload services); renewal without deployment still expires.
5. **Monitor**: alert at 30/14/7 days before expiry from the inventory, plus external probes of actual served certificates.

## Policies
Allowed CAs (CAA DNS records for public domains: `example.com. CAA 0 issue "letsencrypt.org"`),
key types, maximum validity, wildcard rules (limit use), owners required.

## Gotchas
- Certificates pinned in mobile apps or IoT devices break with renewal if the key or CA changes.
- Intermediate CA changes break clients that bundle chains incorrectly; serve the full chain.
- Monitoring the inventory but not what is actually served misses forgotten load balancers.
- Private keys copied around for "easy renewal" are a leak risk: generate keys where they are used.

## Verify
- [ ] No certificate in inventory expires within 14 days without an open renewal task.
- [ ] Spot-check: renewal happens automatically on a test service end to end.
