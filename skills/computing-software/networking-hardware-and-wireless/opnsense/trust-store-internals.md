---
id: computing-software.networking-hardware-and-wireless.opnsense.trust-store-internals
name: trust-store-internals
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [trust-store, certctl, openssl, ca-bundle]
level: advanced
status: docs-checked
description: "How OPNsense deploys trusted CA certificates and CRLs to system directories with certctl.py, with the paths used by base system and ports applications."
sources: ["https://docs.opnsense.org/manual/certificates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trust store internals

Certificates and revocation lists are staged by a tool named certctl.py. It gathers sources from three places: /usr/share/certs/trusted (default certificates shipped with the base system), /usr/local/share/certs (application-specific certificates and CRLs) and /usr/share/certs/untrusted (certificates that must no longer be trusted).

It then creates links in target directories, each entry holding one certificate or CRL, named by hash so OpenSSL can locate it by subject (for example ef954a4e.0, or ef954a4e.r0 for a CRL):

- /etc/ssl/certs: primary location for the base system.
- /etc/ssl/untrusted: the same for untrusted entries, which are ignored.
- /usr/local/openssl/certs: same as the base location, the default for applications built from ports.
- /usr/local/etc/ssl/cert.pem: combined bundle for applications needing a single file.

If /etc/ssl/cert.pem or /usr/local/etc/ssl/cert.pem exists it takes preference over the hashed links; starting with 25.1 these files are removed when present. Default OpenSSL settings are kept in /usr/local/openssl/openssl.cnf (ports) and /etc/ssl/openssl.cnf (base), both managed by OPNsense, so do not hand-edit them.

In System > Trust > Settings, Store intermediate is disabled by default (no intermediates are deployed to this store), Store CRL's puts configured CRLs in the default trust store, and Auto fetch CRL's schedules an hourly download.

## Checked

2026-11-03. Confirmed against the OPNsense Trust manual page, section Internal organisation and Settings: source and target directories, hash naming, cert.pem precedence and the 25.1 removal, openssl.cnf locations, Settings options. Removed: the unsupported troubleshooting advice, replaced by what the page states.

Method: documentation only; no commands were run.
