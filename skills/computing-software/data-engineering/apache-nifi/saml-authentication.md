---
id: computing-software.data-engineering.apache-nifi.saml-authentication
name: saml-authentication
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, saml, sso, authentication, identity-provider, nifi-properties]
level: practitioner
status: docs-checked
description: "SAML single sign-on for NiFi: IdP metadata URL, SP entity id, identity and group attributes, signing options, 12 hour expiry, single logout and HTTP client settings."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML in nifi.properties

- `nifi.security.user.saml.idp.metadata.url`: `http(s)://` or `file://`.
- `nifi.security.user.saml.sp.entity.id`: used as the Issuer.
- `nifi.security.user.saml.identity.attribute.name`: optional; falls back to Subject NameID.
- `nifi.security.user.saml.group.attribute.name`: optional.
- `nifi.security.user.saml.request.signing.enabled`: false.
- `nifi.security.user.saml.want.assertions.signed`: true.
- `nifi.security.user.saml.signature.algorithm`: default `http://www.w3.org/2001/04/xmldsig-more#rsa-sha256`.
- `nifi.security.user.saml.authentication.expiration`: 12 hours.
- `nifi.security.user.saml.single.logout.enabled`: false.
- `nifi.security.user.saml.http.client.truststore.strategy`: `JDK` or `NIFI`.
- `nifi.security.user.saml.http.client.connect.timeout` and `.read.timeout`: 30 secs.

Verify: SP-initiated login completes and the resulting identity matches the configured attribute or NameID.

## Checked

Checked against the NiFi Administration Guide, SAML property table: every key, default (false, true, 12 hours, false, 30 secs), the `JDK` / `NIFI` truststore strategy and the http, https or file metadata URL forms match. The signature algorithm default was written out in full as the page states it. The SP metadata is generated at `nifi-api/access/saml/metadata`.

Method: docs-only read of cited pages, 2026-11-08
