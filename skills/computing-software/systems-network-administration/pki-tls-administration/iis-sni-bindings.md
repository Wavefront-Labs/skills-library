---
id: computing-software.systems-network-administration.pki-tls-administration.iis-sni-bindings
name: iis-sni-bindings
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [iis-sni-bindings, pki-iis, iis, sni, web-hosting-store, netsh, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Host several HTTPS sites on one IIS IP with Server Name Indication and the Web Hosting certificate store, and inspect bindings with netsh."
sources:
  - https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-8/iis-80-server-name-indication-sni-ssl-scalability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS HTTPS bindings and SNI
Goal: multiple sites with their own certs on one IP.
- SNI was introduced in IIS 8.0 (Windows Server 2012); IIS 7.0 and 7.5 do not support it. It lets the host name, not just IP:port, identify the HTTPS endpoint, so many secure sites share one IP address. Clients must support SNI; Internet Explorer on Windows XP does not.
- SNI and the Web Hosting certificate store are part of the default IIS install; no extra feature is needed.
- Web Hosting store: the same tooling as the Personal store (import and export work the same way), designed to scale to many more certificates. In the certificates MMC snap-in for the local computer account, find "Web Hosting" and import certificates there. The IIS site binding dialog offers certificates from both the Personal and Web Hosting stores.
- Create the binding in IIS Manager: Add Website, type `https`, set the Host name (it can be set for SSL since IIS 8), tick "Use Server Name Indication" and choose the certificate. Make the host name match the certificate's CN to avoid a name mismatch error.
- Certificates are loaded into memory on demand in Windows Server 2012, so thousands of SNI sites use little memory; SNI and traditional IP:port bindings can coexist.
- Inspect with an elevated prompt: `netsh http show sslcert`. An SNI binding appears as `hostname:port` (for example `TAPTesting:443`), a traditional one as IP:port.
Gotcha: when traditional (IP:port) and SNI (hostname:port) bindings are configured on the same machine, IIS Manager can in corner cases remove an unintended SSL binding; confirm the real bindings with `netsh http show sslcert`.
Verify:
- [ ] `netsh http show sslcert` lists the expected `hostname:port` entries.
- [ ] A client using SNI (for example `openssl s_client -servername example.com`) receives the matching certificate.

## Checked
Confirmed 2026-11-08 against the IIS 8.0 SNI page on Microsoft Learn. Removed (the page does not cover them): PowerShell `New-WebBinding` and `SslFlags` values, the Centralized Certificate Store provider commands, renewal tooling, private key permissions and the catch-all binding advice.
Method: docs-only read of cited pages, 2026-11-08
