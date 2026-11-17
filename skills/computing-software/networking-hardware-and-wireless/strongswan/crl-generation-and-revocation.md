---
id: computing-software.networking-hardware-and-wireless.strongswan.crl-generation-and-revocation
name: crl-generation-and-revocation
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, crl, revocation, signcrl, cache-crls]
level: practitioner
status: docs-checked
description: "Generate and update CRLs with pki --signcrl, revoke certificates by file or serial, deploy CRLs to x509crl, and cache fetched CRLs with charon.cache_crls."
sources:
  - https://docs.strongswan.org/docs/latest/pki/pkiQuickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crl generation and revocation
Empty CRL signed by the CA:

```
pki --signcrl --cacert strongswanCert.pem --cakey strongswanKey.pem \
    --lifetime 30 > strongswan.crl
```

The default lifetime is 15 days. Revoke a certificate by passing the previous CRL:

```
pki --signcrl --cacert strongswanCert.pem --cakey strongswanKey.pem \
    --lifetime 30 --lastcrl strongswan.crl \
    --reason key-compromise --cert moonCert.pem > new.crl
```

Use `--serial` instead of `--cert` to name the certificate by serial number; `--reason` is optional and `pki --signcrl --help` lists the reasons. Inspect with `pki --print --type crl --in new.crl`.

Publish the CRL on an HTTP or LDAP server, or place it (DER or PEM) in `/etc/swanctl/x509crl`, from where `swanctl --load-creds` loads it.

Caching of dynamically fetched CRLs:

```
charon {
  cache_crls = yes
}
```

Copies are stored in `/etc/swanctl/x509crl` named by the issuer subjectKeyIdentifier plus `.crl`, so the CRL is available right after startup. A stale copy is refetched from a distribution point during the next IKEv2 authentication.

## Checked
2026-11-04. Confirmed against the Certificates Quickstart page: the signcrl commands, default lifetime, `--serial` and `--reason`, publishing locations, and `cache_crls` behaviour.

Method: documentation only; no commands were run.
