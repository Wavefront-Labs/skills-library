---
id: computing-software.networking-hardware-and-wireless.strongswan.pki-ca-and-end-entity-certs
name: pki-ca-and-end-entity-certs
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, pki, ca-certificate, certificates, pki-tool]
level: practitioner
status: docs-checked
description: "Create a strongSwan CA and end entity certificates with pki --gen, --self, --req and --issue, with SAN entries, serverAuth EKU, CRL distribution points and install directories."
sources:
  - https://docs.strongswan.org/docs/latest/pki/pkiQuickstart.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pki ca and end entity certs
```
pki --gen --type ed25519 --outform pem > strongswanKey.pem
pki --self --ca --lifetime 3652 --in strongswanKey.pem \
    --dn "C=CH, O=strongSwan, CN=strongSwan Root CA" --outform pem > strongswanCert.pem
pki --print --in strongswanCert.pem
```

Key types: ed25519, ed448, ecdsa, rsa (e.g. `--type rsa --size 3072`). Not all implementations support EdDSA; use RSA or ECDSA for best compatibility (Windows restricts ECDSA). Never keep the CA private key on an Internet-facing host such as a gateway. Omit `--outform pem` for binary DER.

End entity:

```
pki --req --type priv --in moonKey.pem \
    --dn "C=CH, O=strongswan, CN=moon.strongswan.org" \
    --san moon.strongswan.org --outform pem > moonReq.pem
pki --issue --cacert strongswanCert.pem --cakey strongswanKey.pem \
    --type pkcs10 --in moonReq.pem --serial 01 --lifetime 1826 --outform pem > moonCert.pem
```

`--san` can be repeated: FQDN, email, IPv4 or IPv6. Including the gateway hostname as a SAN is strongly recommended. Add `--flag serverAuth` for clients that require the TLS server EKU, and `--crl <uri>` for crlDistributionPoints (http or ldap). Omitted `--serial` gives a random one.

CA certs go in `/etc/swanctl/x509ca`, end entity certs in `/etc/swanctl/x509`, keys in the ecdsa, rsa, pkcs8 or private subdirectory of `/etc/swanctl`.

## Checked
2026-11-04. Confirmed against the Certificates Quickstart page: pki --gen, --self, --print, --req, --issue commands and options, key types, SAN forms, serverAuth, `--crl`, random serials and directories.

Method: documentation only; no commands were run.
