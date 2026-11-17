---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.mtls-client-to-apisix
name: mtls-client-to-apisix
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, mtls, client-certificate, ssl, admin-api-mtls, tls]
level: advanced
status: docs-checked
description: "Require client certificates on APISIX: an SSL object with client.ca and depth, a client-cert curl test, and Admin API mTLS settings under admin_api_mtls."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS from client to APISIX

Add a `client` block to the SSL object:

```json
{
  "cert": "<SERVER_CERT_PEM>",
  "key": "<SERVER_KEY_PEM>",
  "snis": ["admin.apisix.dev"],
  "client": { "ca": "<CLIENT_CA_PEM>", "depth": 10 }
}
```

Send it with PUT to `/apisix/admin/ssls/1` with the `X-API-KEY` header.

Test with a client certificate:

```shell
curl --resolve 'mtls.test.com:<APISIX_HTTPS_PORT>:<APISIX_URL>' \
  "https://<APISIX_URL>:<APISIX_HTTPS_PORT>/hello" -k \
  --cert ./client.pem --key ./client.key
```

The verbose handshake should include `SSL certificate verify ok.` The SNI must match the certificate's domain.

mTLS for the Admin API itself, in `config.yaml`:

```yaml
admin_listen:
  ip: 127.0.0.1
  port: 9180
https_admin: true

admin_api_mtls:
  admin_ssl_ca_cert: "/path/to/mtls_ca.crt"
  admin_ssl_cert: "/path/to/mtls_server.crt"
  admin_ssl_cert_key: "/path/to/mtls_server.key"
```

## Checked

2026-11-04. Confirmed against the APISIX mTLS page: the SSL object with client.ca and client.depth, the PUT to /apisix/admin/ssls/1, the curl test and the SSL certificate verify ok line, the SNI note, and the admin_api_mtls settings. Nothing removed.

Method: documentation only; no commands were run.
