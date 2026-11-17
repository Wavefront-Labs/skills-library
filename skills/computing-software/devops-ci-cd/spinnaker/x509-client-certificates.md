---
id: computing-software.devops-ci-cd.spinnaker.x509-client-certificates
name: x509-client-certificates
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [x509, authentication, client-certificates, openssl, roles, roleoid, gate]
level: advanced
status: docs-checked
description: "Issue X.509 client certificates for API and script access to Gate, and embed role names in an OID extension so Fiat can authorize the holder."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authentication/x509/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
X.509 client certificates authenticate non-UI or scripted clients without fetching OAuth bearer tokens or SAML assertions each time. They can be used alone or alongside another method.

**Basic certificate with a CA** (the same CA created in the SSL guide, or an external one):
1. `openssl genrsa -des3 -out client.key 4096`
2. `openssl req -new -key client.key -out client.csr` with a non-empty Common Name
3. `openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt`
4. optionally `openssl pkcs12 -export -clcerts -in client.crt -inkey client.key -out client.p12` for browser import.

**Roles.** These certificates prove identity only. If you use Fiat they are not enough for authorization, so roles must be encoded in an extension. The page uses OID `1.2.840.10070.8.1`, set as `role-oid` under `x509` in `gate-local.yml`; other OIDs work by editing `openssl.conf`. The extension line is:

```
1.2.840.10070.8.1 = ASN1:UTF8String:spinnaker-example0\nspinnaker-example1
```

Separate multiple groups with a newline (`\n`), which shows as `%0A` in the certificate. Put the line in a `v3_req` section of both `openssl.conf` (used to generate the CSR with `-config`) and an extension config applied when the CA signs the request.

Sign with the CA, then present the certificate to Gate. If the CA is external, they do the signing for you.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io X.509 client certificates page. Confirmed the openssl commands, role limitation, OID line, newline separation and the two config files. Corrected the OID setting from Halyard to `role-oid` in `gate-local.yml`.
