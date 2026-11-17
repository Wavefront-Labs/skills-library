---
id: computing-software.cybersecurity-defensive.network-defence.radius-server-hardening
name: radius-server-hardening
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [radius-server-hardening, radius, freeradius, cisco-ise, nps, radsec, blastradius, network-access-control]
level: practitioner
status: docs-checked
description: "Harden RADIUS servers (NPS, ISE, FreeRADIUS): Message-Authenticator for BlastRADIUS, RadSec transport, unique shared secrets, EAP choices and logging."
sources: ["https://www.blastradius.fail/", "https://datatracker.ietf.org/doc/html/rfc6614"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RADIUS server hardening

RADIUS is the trust anchor for 802.1X, VPN and device admin (TACACS+ alternative). Its UDP transport
authenticates responses with an ad hoc MD5-based construction and a fixed shared secret. CVE-2024-3596
(Blast-RADIUS, also VU#456537) lets a man-in-the-middle between client and server forge an Access-Accept in
response to a failed authentication. It affects RADIUS over UDP using non-EAP authentication methods; the
attacker does not learn credentials or the shared secret.

## Transport and integrity
- **Require Message-Authenticator**: the short-term mitigation is that clients and servers always send and
  require Message-Authenticator in all requests and responses, placed as the first attribute in Access-Accept
  and Access-Reject. A server is vulnerable if it does not require it in every client request; a client is
  vulnerable if it does not require it in every server response. The setting names are vendor-specific:
  consult your RADIUS vendor (FreeRADIUS, Microsoft NPS, ISE and NAD vendors all shipped patches).
- Long-term mitigation is RADIUS inside an encrypted and authenticated channel. **RadSec** (RFC 6614) carries
  RADIUS over TCP with TLS. If all Access-Requests go over RadSec, the attack is blocked.
- A separate management VLAN reduces exposure but does not remove the risk if the network is misconfigured or
  compromised; the Blast-RADIUS authors say not to rely on it alone.

## Triage by exposure (from the Blast-RADIUS FAQ)
- Accounting only, EAP-only authentication, or RadSec for all requests: the attack does not appear practical,
  but still upgrade.
- Servers handling only local requests (no proxying): upgrade servers first, then clients and NAS equipment.
- Everyone else: upgrade servers immediately, then clients where possible, and set the flags on both sides to
  require Message-Authenticator.
- EAP methods are protected because RFC 2869 mandates a Message-Authenticator (an HMAC-MD5 over the packet).

## Shared secrets
- Unique per NAD (or per site at minimum), long and random; never reuse a default or test secret.
- Rotate on device decommission and staff changes.

## EAP
- Prefer certificate-based EAP (EAP-TLS) over password-based methods; use a server certificate from a CA
  dedicated to RADIUS and have clients validate it (see the server-certificate-validation skill).

## Server hardening
- Patch, minimal services, admin via MFA, HA pair.
- Limit RADIUS clients to known NAD IPs.
- Logs: accounting and authentication logs to SIEM; alerts on bursts of failures and unknown clients.

## Gotchas
- Requiring Message-Authenticator may not be backward compatible with old clients or servers that cannot send
  it; including it in every packet is backward compatible, so inventory NAD firmware and roll out in stages.
- Detection: look for Access-Accept packets at the client carrying Proxy-State attributes made of random
  bytes; end clients should not receive Proxy-State. Confirming needs the matching Access-Reject in server logs.

## Verify
- [ ] All clients and servers configured to require Message-Authenticator; packet capture shows the attribute present.
- [ ] Unique shared secret per NAD in the inventory.

## Checked
Checked 2026-11-09 against the Blast-RADIUS site (attack description, affected scope, mitigation, FAQ
triage, backward compatibility, detection) and RFC 6614 (RADIUS over TLS on TCP). Removed as unconfirmed:
FreeRADIUS option names, the NPS KB5040268 setting names (KB page returned 404 and the FreeRADIUS page is a
landing page), RADIUS over IPsec, the 22-character secret length and default secret name, EAP-MD5/LEAP/PEAP
advice, and the EKU detail.
Method: docs-checked 2026-11-09 against blastradius.fail and RFC 6614.
