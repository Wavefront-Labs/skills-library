---
id: computing-software.cybersecurity-defensive.nessus.nessus-custom-tls-certificate
name: nessus-custom-tls-certificate
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-ssl-certificate, tls-certificates, nessuscli, pki, nessus-deployment]
level: practitioner
status: draft
description: "Replace the self-signed Nessus web server certificate with a CA-issued one using nessuscli import-certs or file placement, including chain, key format and verification."
sources: ["https://docs.tenable.com/nessus/Content/CustomSSLCertificates.htm", "https://docs.tenable.com/nessus/Content/NessusCLI.htm", "https://docs.tenable.com/nessus/Content/CreateANewServerCertificateAndCA.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Custom TLS certificate for the Nessus web server

The default self-signed cert trains users to click through warnings and breaks API clients that
verify TLS. Use an internal-CA certificate.

## Prepare
- Key: RSA 2048+ or ECDSA, PEM, unencrypted (Nessus cannot prompt for a passphrase).
- Cert: PEM, SAN containing the DNS name users and agents use (`nessus.example.internal`).
- Chain: intermediate(s) and root CA in PEM.

## Install (Nessus 10.x)
```
nessuscli import-certs --serverkey=server.key --servercert=server.pem --cacert=ca-chain.pem
# then
systemctl restart nessusd        # Windows: net stop "Tenable Nessus" && net start "Tenable Nessus"
```
Manual alternative: place files as `servercert.pem`/`serverkey.pem` in the Nessus `CA` directory
(Linux `/opt/nessus/com/nessus/CA/`, Windows `<NESSUS_DATA>\nessus\CA\`), and the CA as `cacert.pem`,
then restart.

## Nessus Manager and agents/linked scanners
Agents and linked scanners pin the manager's certificate at link time in some versions; after
replacing the manager cert, confirm agents still communicate (Agents page last-connect time). If
you use a custom CA, add it to agents with `nessuscli fix --secure --set ...` or relink.

## Optional hardening
- `nessuscli fix --set ssl_mode=tls_1_2` (or `tls_1_3`) and `ssl_cipher_list=strong`.
- Client-certificate authentication for users: `nessuscli fix --set force_pubkey_auth=yes` with user
  certs signed by the configured CA.

## Gotchas
- Wrong file permissions on Linux (must be readable by the nessus service user/root only).
- Including the root in `servercert.pem` instead of `cacert.pem` can cause chain errors in some clients.
- Certificates expire silently; monitor expiry (scan your own scanner with plugin 15901 "SSL
  Certificate Expiry").

## Verify
`openssl s_client -connect nessus.example.internal:8834 -servername nessus.example.internal -showcerts`
shows your chain and `Verify return code: 0`; browsers show no warning.
