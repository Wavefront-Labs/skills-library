---
id: computing-software.cloud-infrastructure-engineering.contour.contour-client-certificate-validation
name: contour-client-certificate-validation
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [mtls, clientvalidation, casecret, crlsecret, optionalclientcertificate, skipclientcertvalidation, xfcc, forwardclientcertificate]
level: advanced
status: docs-checked
description: "HTTPProxy mutual TLS: clientValidation caSecret, optional client certs, skipClientCertValidation for ext authz, CRL checks, and XFCC forwardClientCertificate."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/tls-termination.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Client certificate validation (mTLS)

Add `clientValidation` under the vhost `tls` block to require valid client certificates; Envoy checks expiry and chain of trust.

```yaml
tls:
  secretName: secret
  clientValidation:
    caSecret: client-root-ca
    optionalClientCertificate: false
    crlSecret: client-crl
    crlOnlyVerifyLeafCert: true
    forwardClientCertificate:
      subject: true
      cert: true
      chain: true
      dns: true
      uri: true
```

- `caSecret`: Opaque Secret with only a `ca.crt` key (PEM bundle of trusted CAs); `tls.crt`/`tls.key` entries are ignored.
- `optionalClientCertificate: true` requests a cert but lets clients without one continue; presented certs are still verified.
- `skipClientCertValidation: true` requires/asks for certs but ignores validation failures (incrementing the `fail_verify_error` listener stat), so an external authorization server can decide. Omitting `caSecret` requests but does not require certs.
- `crlSecret`: Opaque Secret with `crl.pem` (concatenated PEM CRLs, limited by the 1MiB Secret size). CRLs must exist for all CAs including intermediates or clients are denied; `crlOnlyVerifyLeafCert: true` checks only the leaf.
- `forwardClientCertificate` selects which parts go in the `x-forwarded-client-cert` header. Contour always drops any client-supplied XFCC first, then adds its own only when configured and a cert was presented.

## Checked

2026-11-04. Confirmed against the Contour TLS termination page (config/tls-termination.md, client validation): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
