---
id: computing-software.networking-hardware-and-wireless.opnsense.trust-certificates-and-settings
name: trust-certificates-and-settings
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [certificates, trust, certificate-authority, csr, intermediate]
level: practitioner
status: docs-checked
description: "Manage certificates in System > Trust on OPNsense: certificate types, CSR, store intermediate, CRL storage, legacy provider and constraints."
sources: ["https://docs.opnsense.org/manual/certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trust: certificates and settings

System > Trust > Certificates creates and manages certificates, so you rarely need the openssl command line. Components using them include OpenVPN, IPsec, Captive Portal and the web proxy. Types you can generate: Client, Server, Combined Client/Server, and Certificate Authority; you can also create a Certificate Signing Request for an external CA.

Choose the type carefully; clients reject wrong types. For the web interface use a server or a combined client/server certificate, not a CA or client one.

System > Trust > Settings:
- Store intermediate: allow locally defined intermediate CAs in the local trust store. Off by default. Cross-signed intermediates can break things if one expires later in the chain. When you add a certificate that needs an intermediate and the store option is off, include the intermediates in the certificate you insert, or the GUI will report validation problems.
- Store CRL's: put all configured revocation lists in the default trust store.
- Auto fetch CRL's: hourly job that downloads CRLs from the distribution points of CAs in the store.
- Enable legacy: enable OpenSSL legacy providers (ciphers scheduled for removal).
- Configuration constraints: set default ciphers and protocols for the default OpenSSL context. Be careful, many firewall applications use it and might break. Applications are not forced to use the standard context, so effects vary.

For chain-building examples see the self-signed chain how-to.

## Checked

2026-11-03. Confirmed against the OPNsense Trust manual page: certificate types, CSR, type warning, Store intermediate warning, Store CRL's, Auto fetch CRL's, Enable legacy, Configuration constraints. Nothing removed.

Method: documentation only; no commands were run.
