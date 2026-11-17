---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.zero-trust
name: zero-trust
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-security-architecture, zero-trust, nist-sp-800-207, identity-aware-proxy, mtls, device-posture, ztna, beyondcorp, continuous-verification]
level: advanced
status: draft
description: "Apply zero trust to cloud workloads: NIST SP 800-207 tenets, identity-aware access for users, mTLS and workload identity between services, incremental adoption."
sources: ["https://csrc.nist.gov/pubs/sp/800/207/final", "https://www.cisa.gov/zero-trust-maturity-model", "https://cloud.google.com/beyondcorp"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero trust architecture

No implicit trust from network location: every access request is authenticated, authorised and
evaluated per session using identity, device and context (NIST SP 800-207).

## Components
- **Policy decision/enforcement points**: identity-aware proxies (Google IAP, AWS Verified Access,
  Azure Entra Application Proxy / Global Secure Access, Cloudflare Access, Zscaler) in front of apps
  instead of VPN-to-network.
- **Strong identity**: phishing-resistant MFA (FIDO2/passkeys) for workforce; workload identity
  (SPIFFE/SPIRE, cloud workload identities) for services.
- **Device posture**: managed/compliant device signals in access policies (conditional access).
- **Service-to-service**: mTLS with per-service identities (service mesh) + authorisation policies
  (Istio `AuthorizationPolicy`), not "anything inside the VPC can call".
- **Micro-segmentation**: default-deny network policies; segmentation reduces blast radius but
  isn't the trust decision.
- **Telemetry**: all decisions logged and analysed (feeding risk signals back into policy).

## Adoption path (CISA maturity model pillars: identity, devices, networks, apps/workloads, data)
1. Inventory apps and access paths; start with admin and high-value apps behind an identity-aware proxy.
2. Enforce phishing-resistant MFA and conditional access.
3. Replace broad VPN access app by app.
4. Introduce mTLS/workload identity inside the platform; default-deny network policy.
5. Data-level controls (classification-aware access, DLP).

## Gotchas
- "Zero trust" products alone don't change authorisation design — least privilege still needed.
- Break-glass paths must still exist and be monitored.

## Verify
- [ ] Admin interfaces reachable only via identity-aware access with MFA and device checks.
- [ ] Service-to-service calls without valid identity are rejected (test).
