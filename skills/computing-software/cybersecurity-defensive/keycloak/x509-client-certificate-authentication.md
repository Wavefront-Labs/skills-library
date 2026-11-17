---
id: computing-software.cybersecurity-defensive.keycloak.x509-client-certificate-authentication
name: x509-client-certificate-authentication
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, x509, client-certificate, ocsp, crl]
level: practitioner
status: docs-checked
description: "Configure Keycloak X.509 client certificate login with CRL or OCSP checks, identity mapping, and correct reverse proxy validation."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/x509.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# x509 client certificate authentication
Keycloak supports logging in with an X.509 client certificate if the server is configured for mutual SSL. Workflow: the client sends the request over TLS; during the handshake both sides exchange x509/v3 certificates; the container validates the certificate PKIX path and expiration date; the Keycloak authenticator then checks revocation status (CRL or CRL Distribution Points, or OCSP), that the key and the extended key match the expected ones; any failed check fails authentication, otherwise the certificate identity is extracted and mapped to an existing user. In the Browser flow the server prompts users to confirm their identity or sign in with username and password; in the Direct Grant flow it signs the user in.

Important note from the docs: validating the PKIX path is the web container's responsibility. Keycloak's authenticator only adds checks of expiration, revocation status and key usage. Behind a reverse proxy, make sure the proxy validates the PKIX path.

Supported identity sources: match SubjectDN with a regular expression, X500 subject email attribute, subject email from the Subject Alternative Name (RFC822Name), SAN other name (typically the UPN), Common Name, match IssuerDN with a regular expression, serial number, serial number plus IssuerDN, SHA-256 thumbprint (lowercase hex), and full certificate in PEM format. Regex example: `emailAddress=(.*?)(?:,|$)`. The identity maps to a user's username, email or a custom attribute. Notes: disabling *Login with email* in realm settings applies to certificate authentication; serial number plus IssuerDN needs two custom attributes; full PEM is limited to attributes mapped to external federation such as LDAP because Keycloak cannot store certificates in its database.

Extended validation: revocation by CRL, CRL Distribution Point and OCSP/Responder URI, and Certificate KeyUsage validation.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/x509.adoc. Removed (not on the page read): the header-spoofing and stale CRL/OCSP gotchas, "enable only checks you can serve" advice, and the three-certificate Verify step.
Method: documentation only; no commands were run.
