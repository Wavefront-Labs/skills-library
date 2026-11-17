---
id: computing-software.networking-hardware-and-wireless.strongswan.hash-and-url-certificates
name: hash-and-url-certificates
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, hash-and-url, cert-uri-base, fragmentation, certificates]
level: practitioner
status: docs-checked
description: "Avoid IKE fragmentation by sending certificate hash and URL pairs: enabling charon.hash_and_url, setting cert_uri_base in authorities, and hosting DER certificates."
sources:
  - https://docs.strongswan.org/docs/latest/features/hashAndUrl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hash and url certificates
IKEv2 can send a SHA1 hash and a URL for each X.509 certificate in IKE_AUTH instead of the DER blob, to avoid fragmenting UDP datagrams. charon supports sending and receiving; receiving needs no configuration except enabling the feature.

**Enable.** It is off by default, because accepting URLs from unauthenticated peers and downloading whatever is there carries security concerns:

```
charon {
  hash_and_url = yes
}
```

**Base URL.** In `swanctl.conf`, add `cert_uri_base` to the `authorities` section of the CA that issued the certificate to be sent this way:

```
authorities {
  strongswan {
    cacert = strongswanCert.pem
    cert_uri_base = http://winnetou.strongswan.org/certs/
  }
}
```

The URL sent is the base with the SHA1 hash of the DER encoded certificate appended. The peer still needs the certificates locally.

**Prepare certificates.** The web server must serve DER files named by that hash. Convert PEM first:

```
openssl x509 -in carolCert.pem -inform PEM -out carolCert.der -outform DER
```

The page's example uses a web server hosting certificates for roadwarriors and a gateway issued by one CA.

## Checked
2026-11-04. Confirmed against the strongSwan Hash and URL page: SHA1 hash plus URL in IKE_AUTH, charon.hash_and_url disabled by default, cert_uri_base in authorities, PEM to DER conversion. Nothing removed.

Method: documentation only; no commands were run.
