---
id: computing-software.networking-hardware-and-wireless.strongswan.authorities-section
name: authorities-section
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, authorities, crl-uris, ocsp-uris, cert-uri-base]
level: practitioner
status: docs-checked
description: "Use the swanctl.conf authorities section to attach CRL, OCSP and Hash and URL certificate URIs to a CA certificate, from a file, token handle or the x509ca directory."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# authorities section
The `authorities` section defines complementary attributes for certification authorities, each in an uniquely named subsection `<name>`.

Identify the CA certificate with exactly one of:
- `cacert`: relative path from `swanctl/x509ca` or an absolute path
- `file`: absolute path, passed as-is to the daemon so it must be readable by it
- `handle`: hex-encoded CKA_ID or handle of the certificate on a token or TPM 2.0

Optional `slot` (token slot) and `module` (PKCS#11 module name) apply to token certificates.

Attributes:
- `crl_uris`: comma-separated CRL distribution points (ldap, http or file URI)
- `ocsp_uris`: comma-separated OCSP URIs
- `cert_uri_base`: base URI for the IKEv2 Hash and URL feature; the certificate URI is the base with the SHA1 hash of the DER encoded certificate appended

Load with `swanctl --load-authorities`.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl.conf reference (authorities section: cacert, file, handle, slot, module, cert_uri_base, crl_uris, ocsp_uris) and the swanctl load-all page (--load-authorities). Nothing removed.

Method: documentation only; no commands were run.
