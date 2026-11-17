---
id: computing-software.networking-hardware-and-wireless.check-point.https-inspection
name: https-inspection
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, https-inspection, ssl-inspection, bypass-rules]
level: practitioner
status: draft
description: "Configure Check Point HTTPS Inspection with an outbound CA certificate, bypass rules for sensitive categories, and inbound inspection."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ThreatPrevention_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTPS Inspection (outbound and inbound)

- Outbound: the gateway acts as a proxy and re-signs server certificates with a CA that clients must trust. Enable via the gateway object > HTTPS Inspection > **Create** (generate a certificate for the gateway) and **Export certificate** for deployment by GPO/MDM. Mark the blade on.
```
mgmt_cli -r true show https-rulebase --format json  # (confirm object names on your version)
```
- HTTPS Inspection Policy has its own rulebase. Typical order: **Bypass** rules first (banking, health, update sites, categories "Financial Services", "Health"), then an **Inspect** rule for the internal network to Internet, then a catch-all Bypass or Inspect decision.
- Inbound inspection: the server's real certificate and private key are installed on the gateway (Servers certificate), used for incoming traffic towards internal web servers.
- Certificates and failures: pinned apps (mobile apps, some update clients) break when inspected; add their domains to bypass. Certificate errors in browsers mean the CA is not trusted; the gateway-generated CA must be deployed to all clients.
- Performance: inspecting TLS 1.3 and high concurrent sessions costs CPU; check `fw ctl pstat` and `cpview`. Validate "Certificate Validation": block untrusted server certificates, expired and revoked ones (CRL/OCSP require connectivity).
- Gotcha: URL Filtering "SSL bypass" updates arrive via the Check Point updates; keep them current.

Verify: browse https://example.org from a trusted client; the certificate issuer is the gateway's CA and logs show `HTTPS Inspection` action `Inspect`; a bypass site shows the original issuer.
