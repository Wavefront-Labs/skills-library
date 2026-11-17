---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.ssl-certificate-sni
name: ssl-certificate-sni
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, ssl, certificate, sni, wildcard, tls, ssls]
level: practitioner
status: docs-checked
description: "Serve TLS certificates in APISIX through the ssls Admin API: cert, key, snis, wildcard SNI, extra certs and keys arrays, and a curl --resolve check."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/certificate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSL certificates and SNI

SSL object attributes:
- `cert` and `key`: PEM public certificate and private key.
- `snis`: hostnames or wildcards such as `*.test.com` bound to the certificate.
- `certs` and `keys`: extra PEM pairs (for example an ECC cert beside RSA), matched by index and of equal length.

Create with PUT to `/apisix/admin/ssls/1` and `X-API-KEY`:

```json
{ "cert": "<CERT_PEM>", "key": "<KEY_PEM>", "snis": ["test.com"] }
```

Add the matching hostname to the route, for example `"hosts": ["test.com"]`. For several domains list them in the `snis` array (for example `["www.test.com","mail.test.com"]`). For a wildcard use `"*.test.com"` in both `snis` and the route `hosts`.

Check:

```shell
curl --resolve 'test.com:9443:127.0.0.1' https://test.com:9443/get -k -vvv
```

Expected output includes `SSL connection using TLSv1.3`, a server certificate whose subject has `CN=test.com`, and `GET /get HTTP/2`.

Trusted CA setting shown on the page: `apisix.ssl.ssl_trusted_certificate: /path/to/ca-bundle` in `config.yaml`.

## Checked

2026-11-04: read the Certificate page; cert, key, snis, certs and keys (equal length, paired by index), the single and wildcard SNI examples, the curl --resolve check and its sample output, and the ssl_trusted_certificate setting match. Removed the unstated claim that multiple domains must also be listed in the route hosts.

Method: documentation only; no commands were run.
