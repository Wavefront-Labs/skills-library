---
id: computing-software.systems-network-administration.cisco-networking.ikev2-certificate-authentication
name: ikev2-certificate-authentication
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ipsec-certificates, crypto-pki, ikev2, pki-trustpoint, rsa-sig, certificate-map, scep, vpn]
level: practitioner
status: draft
description: "Authenticate IKEv2 tunnels with certificates on IOS XE: trustpoints, enrolment (terminal/SCEP), certificate maps in IKEv2 profiles, and revocation checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_pki/configuration/xe-16/sec-pki-xe-16-book.html
  - https://www.cisco.com/c/en/us/support/docs/security/flexvpn/116089-configure-flexvpn-00.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Certificate authentication for IKEv2

## Why
Pre-shared keys do not scale (one key everywhere, or N keys to manage) and cannot be revoked per
device. Certificates give per-device identity and revocation.

## Trustpoint and enrolment
```
crypto key generate rsa label VPN-KEY modulus 2048
crypto pki trustpoint VPN-CA
 enrollment url http://10.0.0.60:80          ! SCEP; or 'enrollment terminal'
 subject-name CN=spoke1.example.net,O=Example
 subject-alt-name spoke1.example.net
 revocation-check crl none                   ! try CRL, accept if unreachable
 rsakeypair VPN-KEY
 auto-enroll 80 regenerate                   ! renew at 80% of lifetime
crypto pki authenticate VPN-CA                ! accept CA fingerprint (verify out of band)
crypto pki enroll VPN-CA
```
Clock must be correct (NTP) or certificates appear not yet valid/expired.

## IKEv2 profile
```
crypto pki certificate map HUB-MAP 10
 subject-name co hub.example.net
crypto ikev2 profile CERT-PROF
 match certificate HUB-MAP                   ! or match identity remote fqdn ...
 identity local dn
 authentication remote rsa-sig
 authentication local rsa-sig
 pki trustpoint VPN-CA
```
Spokes and hub can mix `authentication local rsa-sig` with `authentication remote pre-share`
during migration.

## Revocation
- `revocation-check crl`: router downloads CRL from the CDP in the cert; the CDP URL must be reachable.
- `revocation-check ocsp` for real-time checks.
- `none` disables checks: acceptable only in labs.

## Gotchas
- Certificate too large for one IKE packet: IKEv2 fragmentation (`crypto ikev2 fragmentation mtu 1360`).
- The hub needs the full chain (intermediate CA trustpoint).
- `identity local dn` vs fqdn must match what the peer's profile expects.

## Verify
```
show crypto pki certificates VPN-CA
show crypto pki trustpoints status
show crypto ikev2 sa detailed              ! Auth sign: RSA, Auth verify: RSA
debug crypto pki transactions
```
