---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-ssl-forward-proxy-decryption
name: pan-os-ssl-forward-proxy-decryption
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [ssl-forward-proxy, pan-os, ssl-decryption, decryption-policy, decryption-profile, no-decrypt, forward-trust]
level: practitioner
status: draft
description: "Deploy PAN-OS SSL forward proxy decryption with a forward trust CA, decryption profile, exclusions and a no-decrypt rule for sensitive categories."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/decryption/configure-ssl-forward-proxy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: inspect outbound TLS traffic by acting as a man-in-the-middle with an enterprise CA the clients trust.

Steps
1. Create or import an enterprise CA certificate on the firewall; mark it Forward Trust Certificate, and create a separate untrusted CA marked Forward Untrust Certificate.
2. Distribute the forward trust CA public certificate to clients (GPO / MDM).
3. Create a decryption profile (block unsupported versions, expired certs, untrusted issuers).
4. Add rules: no-decrypt first, decrypt after.

```
configure
set rulebase decryption rules no-decrypt-sensitive from trust to untrust source any destination any category [ financial-services health-and-medicine ] action no-decrypt type ssl-forward-proxy
set rulebase decryption rules decrypt-out from trust to untrust source any destination any service any action decrypt type ssl-forward-proxy profile DP-STD
commit
```

Gotchas
- Clients with certificate pinning (some apps, update clients) break; add them to the exclusion list or no-decrypt rule by application or hostname.
- Private key security: protect the forward trust CA key (HSM or restricted export) since it can mint trusted certs for any site.
- Legal and privacy: exclude categories your policy forbids decrypting, and document it.
- Capacity: decryption lowers throughput; size according to the datasheet number for "decrypted" sessions.

## Verify
```
show system setting ssl-decrypt memory
show session all filter ssl-decrypt yes
```
The traffic log Decrypted column should show yes for decrypted flows; browse an https site and view the certificate issuer to confirm it is your CA.
