---
id: computing-software.devops-ci-cd.spinnaker.saml-authentication
name: saml-authentication
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [saml, authentication, gate, keystore, metadata, idp, gate-local]
level: practitioner
status: docs-checked
description: "Set up SAML 2.0 login for Gate: IdP metadata, login URL, entity ID, a Java keystore from keytool, and the gate-local.yml saml block with signing credentials."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authentication/saml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SAML delivers a cryptographically signed XML assertion with the user's identity and group membership to Gate. Gate verifies the signature using a metadata file and, on success, treats the user as authenticated.

**At the identity provider:**
1. Download `metadata.xml` (some providers expose a URL usable directly, if Gate can reach it).
2. Create a Spinnaker SAML application.
3. Set the login URL to `https://<gate address>:8084/saml/SSO` (the page uses localhost).
4. Choose a unique entity ID (the page uses `spinnaker.test`).
5. Enable the users who may access Spinnaker.

**Keystore.** Generate one with `keytool -genkey -v -keystore saml.jks -alias saml -keyalg RSA -keysize 2048 -validity 10000`.

**Gate configuration.** The page describes a SAML integration introduced with Spinnaker 2025.x.x, replacing legacy configuration. It applies to IdPs that support signing credentials (the page says Okta is not one) and is required for Keycloak and a few others. Put the files in a ConfigMap (the page uses `kubectl create configmap configmap-saml --from-file=...` for the keystore, metadata XML, certificate PEM and private key PEM), or use encryptedFile secret references, then add to `gate-local.yml`:

```yaml
saml:
  enabled: true
  issuerId: <Client>
  metadataUrl: file:/opt/spinnaker/saml/<your_cert>.xml
  keyStore: file:/opt/spinnaker/saml/saml.jks
  keyStorePassword: <from jks creation>
  keyStoreAliasName: <alias>
  keyStoreType: jks
  sign-requests: true
  signing-credentials:
  - certificate-location: file:/opt/spinnaker/saml/<your_cert>.pem
    private-key-location: file:/opt/spinnaker/saml/<your_priv>.pem
```

- `metadataUrl` can instead be the IdP's metadata URL; Gate then refreshes it at startup and every 15 minutes.
- The page notes the key store password and alias are optional, the alias defaults to "mykey" with keytool, and says PKCS12 is newer and should be used instead of `jks`.
- For network architecture and SSL termination the page points to the SSL documentation.

**Flows.** In the service-provider flow Deck calls `GET /auth/user`, then Gate redirects to the IdP with `SAMLRequest`, `SigAlg` and `Signature` query parameters. In the IdP-initiated flow the IdP POSTs a `SAMLResponse` to `/saml/SSO`; providers may return a self-submitting HTML form because browsers will not re-POST on a 302.

## Checked

2026-11-04. Confirmed against the SAML 2.0 page: IdP steps, keytool command, gate-local.yml block, refresh interval, login flows. Removed: the `hal config security authn saml` commands (not on the page, which now configures gate-local.yml) and the fixed-at-login role note (from a different page, not re-fetched here).

Method: documentation only; no commands were run.
