---
id: computing-software.networking-hardware-and-wireless.check-point.sic-trust-reset
name: sic-trust-reset
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, sic, trust-reset, secure-internal-communication]
level: practitioner
status: draft
description: "Fix Secure Internal Communication problems between Check Point management and gateways using cpconfig reset and ICA checks."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SIC trust: establish, reset and troubleshoot

```
cp_conf sic state                   # on the gateway: Trust established / not established
cp_conf sic init <one-time-pass> norestart
cpconfig                            # Secure Internal Communication -> Reset
cpstop ; cpstart
# management side:
cpca_client lscert -kind SIC -stat Valid
cpca_client revoke_cert -n "CN=gw1 VPN Certificate,O=mgmt..y9x6dt"   # (confirm DN)
```
- SIC uses certificates issued by the management server's **Internal CA (ICA)** on port 18211 (CPD), 18190/18191 for the management, and `18210` for ICA pull. Firewalls between management and gateways must allow these.
- Typical errors: "Trust state: Uninitialized", "Certificate validation error" (clock skew: certificates are time-bound; keep NTP in sync), "SIC failed: ... wrong key" (one-time password mismatch), "Gateway not reachable".
- Reset procedure: on the gateway run `cpconfig` > SIC > Reset > new OTP; in SmartConsole open the gateway > Communication > **Reset** > enter the same OTP > Initialize. If the gateway still has an old certificate on the management, revoke it with `cpca_client` before the reinitialisation.
- After a gateway re-IP, the certificate name stays the same, but connectivity is by the new IP; update the object's main IP.
- Gotcha: the SIC DN contains the object name, so renaming a gateway object does not break trust, but a name collision with an old revoked object can.

Verify: SmartConsole Communication status `Trust established`; `cp_conf sic state` shows `Trust established`; install policy succeeds.
