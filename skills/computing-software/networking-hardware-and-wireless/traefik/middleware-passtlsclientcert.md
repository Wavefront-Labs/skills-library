---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-passtlsclientcert
name: middleware-passtlsclientcert
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, passtlsclientcert, mtls, client-certificate, x-forwarded-tls-client-cert, middleware]
level: practitioner
status: docs-checked
description: "Forward a verified client certificate or selected fields to the backend with passTLSClientCert after mTLS termination."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/passtlsclientcert.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware passtlsclientcert
`passTLSClientCert` adds selected data from the client TLS certificate to request headers. It can add two headers: `X-Forwarded-Tls-Client-Cert` (the PEM, when `pem: true`) and `X-Forwarded-Tls-Client-Cert-Info` (the selected details as an escaped string suitable for a URL query).

```yaml
http:
  middlewares:
    test-passtlsclientcert:
      passTLSClientCert:
        pem: true
        info:
          notAfter: true
          notBefore: true
          sans: true
          subject:
            commonName: true
          issuer:
            commonName: true
```
`info` options (all default false): `serialNumber`, `notAfter`, `notBefore`, `sans`, `subject.*` and `issuer.*` (`country`, `province`, `locality`, `organization`, `commonName`, `serialNumber`, `domainComponent`; `subject` also has `organizationalUnit`). With several certificates, values are separated by a comma.

Gotchas: only certificates matching the `clientAuth.clientAuthType` policy of the MutualTLS configuration are passed. The PEM header can exceed a web server's header size limit (commonly 4kb-8kb); if that happens, set `pem` to false and select only the needed `info` parts.

## Checked
2026-11-03. Confirmed against the Traefik passTLSClientCert reference page (docs/content/reference/routing-configuration/http/middlewares/passtlsclientcert.md): headers, pem, info options (including issuer), clientAuthType rule, multi-cert separator, header size note. Removed: "header is empty otherwise", the advice to strip client-supplied copies, and the curl Verify step.
Method: documentation only; no commands were run.
