---
id: computing-software.cybersecurity-defensive.network-defence.eap-tls-certificate-authentication
name: eap-tls-certificate-authentication
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [wireless-security, eap-tls, certificate-authentication, scep, pkcs, intune-certificate-profile, radius-server-certificate, freeradius, nps]
level: advanced
status: draft
description: "Deploy EAP-TLS for Wi-Fi and wired: device certificates via Intune/GPO, RADIUS server certificate, client trust settings, revocation and common failure diagnosis."
sources: ["RFC 5216 The EAP-TLS Authentication Protocol (and RFC 9190 EAP-TLS 1.3)", "Microsoft Learn - Configure certificate profiles in Intune (SCEP/PKCS)", "FreeRADIUS documentation (EAP module)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EAP-TLS certificate authentication

**Goal:** network authentication by device (and optionally user) certificates, with no
passwords to phish or brute force.

## Components
1. **Internal CA** issuing client certificates (AD CS, cloud PKI such as Microsoft Cloud PKI, SCEPman).
2. **Distribution**: Intune SCEP/PKCS certificate profiles, AD CS autoenrolment via GPO, Jamf for macOS.
3. **RADIUS server** with its own server certificate (from a CA the clients trust; internal CA is fine).
4. **Client network profile** specifying EAP-TLS, the trusted root CA, and the RADIUS server name.

## Certificate details
- Client certificate: EKU Client Authentication; subject or SAN containing a device identifier the RADIUS policy can map (device name, Intune device ID).
- Server certificate: EKU Server Authentication; SAN with the RADIUS server name configured in client profiles.
- Validity: 1 year for client certs with automatic renewal.

## RADIUS policy
- Check certificate chain to your CA and revocation (CRL/OCSP) - stolen device certificates must be revocable.
- Authorise based on certificate attributes plus directory/MDM lookup (device enabled, compliant).

FreeRADIUS `mods-enabled/eap` (excerpt):
```
eap {
  default_eap_type = tls
  tls-config tls-common {
    private_key_file = ${certdir}/radius.key
    certificate_file = ${certdir}/radius.pem
    ca_file = ${cadir}/corp-root.pem
    check_crl = yes
    tls_min_version = "1.2"
  }
  tls { tls = tls-common }
}
```

## Diagnose failures
| Symptom | Likely cause |
|---|---|
| Client never sends certificate | Wrong certificate store, missing EKU, profile references a different CA |
| RADIUS rejects "unknown CA" | Intermediate CA not on RADIUS server |
| Client drops after server hello | Client does not trust the RADIUS server cert or name mismatch |
| Works then fails after months | Certificate or CRL expired |
NPS logs: event 6273 with reason codes; FreeRADIUS `radiusd -X` debug.

## Gotchas
- Certificates with exportable private keys can be copied to rogue devices: use TPM-protected, non-exportable keys.
- CRL not reachable by the RADIUS server blocks everyone if CRL checking is hard-fail.
- Supplicant fallback to PEAP if both configured; remove PEAP once migrated.

## Verify
- [ ] RADIUS logs show EAP-TLS authentications with expected certificate subjects.
- [ ] Revoking a test device certificate blocks its next connection.
