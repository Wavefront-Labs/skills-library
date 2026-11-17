---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-certificate-management
name: pan-os-certificate-management
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [certificate-management, pan-os, csr, ocsp, crl, trusted-ca, certificate-profile, pki]
level: practitioner
status: draft
description: "Generate CSRs, import certificates and keys, build certificate profiles with OCSP/CRL, and track expiry on PAN-OS."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/certificate-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: certificates for management HTTPS, GlobalProtect, SAML, decryption and VPN, with revocation checking and renewals planned.

Tasks (Device > Certificate Management > Certificates)
- Generate a CSR for a public-CA signed cert, then import the signed leaf plus chain.
- Import PKCS12 or PEM with a passphrase (set via the GUI form; do not paste passphrases into scripts).
- Mark roles on the cert: forward trust, forward untrust, trusted root CA, SSL/TLS service profile usage.
- Certificate Profile: list CA certs, enable CRL and/or OCSP, choose behaviour when status is unknown or the responder times out.

CLI listing:
```
show sys info
request certificate show-usage-info (confirm; availability varies)
```
Use the XML API to list certificates for inventory:
```
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/?type=config&action=get&xpath=/config/shared/certificate"
```

Gotchas
- SSL/TLS service profiles bind a cert and protocol range to a service (management, GlobalProtect); changing the cert without updating the profile leaves the old cert in use.
- A certificate profile with "block if status unknown" and no reachable OCSP responder locks out users.
- Expired intermediate CAs break chains; always import the full chain.
- Track expiry yourself: system logs raise alarms late.

## Verify
Browse to the service and inspect the served chain, then check expiry dates in the GUI list or the XML output above.
