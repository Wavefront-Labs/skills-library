---
id: computing-software.cloud-infrastructure-engineering.contour.contour-httpproxy-tls-termination
name: contour-httpproxy-tls-termination
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [tls-termination, httpproxy, secretname, sni, permitinsecure, minimumprotocolversion, kubernetes-io-tls]
level: practitioner
status: docs-checked
description: "HTTPProxy TLS termination: tls.secretName, SNI binding to Host header, secure-first 301 redirect, permitInsecure routes, minimumProtocolVersion, cross-namespace secrets."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/tls-termination.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy TLS termination

Set `spec.virtualhost.tls.secretName` to a Secret of type `kubernetes.io/tls` with PEM `tls.crt` and `tls.key`. Chain CAs may be appended to `tls.crt` (serving cert first, intermediates in issuing order). If several proxies share a Secret, its certificate needs a SAN for each fqdn.

```yaml
spec:
  virtualhost:
    fqdn: foo2.bar.com
    tls:
      secretName: testsecret          # or "somenamespace/somesecret"
      minimumProtocolVersion: "1.3"   # 1.2 is the default
  routes:
  - services: [{name: s1, port: 80}]
```

Behaviour:
- Clients must send SNI; vhosts are strongly bound to SNI names, so the HTTP Host header must equal the SNI name from the handshake.
- "Secure first": once TLS is on for a vhost, plain HTTP requests get a 301 redirect to HTTPS.
- Override per route with `permitInsecure: true`, e.g. a `/blog` route that serves HTTP directly while `/` still redirects. Setting `disablePermitInsecure: true` in the Contour config file ignores this field globally.
- A secretName containing a slash (`ns/secret`) reads the certificate from another namespace; this requires a TLSCertificateDelegation.

Reuse of one certificate across hosts works only when it covers each fqdn's SAN. For a Secret in another namespace, see TLS Certificate Delegation.

## Checked

2026-11-08: read the Contour docs config/tls-termination (TLS Termination and Permitting Insecure Requests) and configuration (disablePermitInsecure). Confirmed: kubernetes.io/tls Secret with tls.crt and tls.key, chain ordering, SAN per fqdn, SNI binding to the Host header, 301 secure-first redirect, permitInsecure per route, minimumProtocolVersion 1.3 or 1.2 (default), namespace/secret form subject to delegation. Removed: the wildcard-certificate remark.

Method: documentation only; no commands were run.
