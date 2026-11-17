---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.certificate-expiry-and-renewal
name: certificate-expiry-and-renewal
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, csr, certificate-renewal, cert-expiry]
level: practitioner
status: draft
description: "Create a CSR on BIG-IP, install the issued certificate and chain, and monitor expiring certificates with tmsh."
sources:
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-ssl-administration.html
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate and key lifecycle: CSR, install, expiry

```
tmsh create sys crypto key www.example.com key-size 2048 gen-certificate country US state CA locality SF organization Ex common-name www.example.com subject-alternative-name "DNS:www.example.com,DNS:example.com"
tmsh create sys crypto csr www.example.com key www.example.com common-name www.example.com subject-alternative-name "DNS:www.example.com"
tmsh install sys crypto cert www.example.com from-local-file /var/tmp/www_new.crt
tmsh list sys crypto cert www.example.com
tmsh show sys crypto cert | grep -E "Name|Expiration"
```
- CSR with SAN entries: modern browsers ignore the CN, so the SAN must hold all names. Use a key size of 2048 or ECC (`key-type ec-private curve-name prime256v1`).
- Renewal in place: installing a new cert under the *same name* as an existing one (`tmsh install sys crypto cert www.example.com from-local-file new.crt`) updates every profile that references that name; no profile edits needed. Keep the key unchanged on renewal or install the new key with the same name.
- Chain: install intermediates as separate certs and set `chain` in the client SSL profile's `cert-key-chain`; use `ca-bundle` objects for client trust. Include only intermediates, not the root.
- Expiry watching: BIG-IP raises an alert at 30 days before (`/var/log/ltm`, `Certificate ... will expire`; confirm exact). Also use `tmsh list sys crypto cert one-line` in a script and `openssl x509 -enddate`.
- Gotcha: expired default certs such as `default.crt` and `ca-bundle.crt` can cause monitors and iQuery to fail after expiry; replace/renew the self-signed management cert `tmsh run sys crypto ...` as needed.

Verify: `echo | openssl s_client -connect vip:443 -servername www.example.com 2>/dev/null | openssl x509 -noout -enddate -subject -ext subjectAltName`.
