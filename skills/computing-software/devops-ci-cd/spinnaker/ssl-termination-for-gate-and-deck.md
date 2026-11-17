---
id: computing-software.devops-ci-cd.spinnaker.ssl-termination-for-gate-and-deck
name: ssl-termination-for-gate-and-deck
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [ssl, tls, gate, deck, load-balancer, redirect-uri, certificates, keytool]
level: advanced
status: docs-checked
description: "Choose load-balancer or Gate-terminated SSL, set X-Forwarded headers, the gate-local.yml SSL block and Deck's Apache certificate, and do SSL before authentication."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/ssl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The SSL page covers traffic between outside parties and Spinnaker: browser to Deck, Deck to Gate, and any other client to Gate. Internal service-to-service traffic is outside it.

**Do SSL first.** Operators often get authentication working before HTTPS, but the transition is not smooth. The page recommends implementing at least a temporary SSL solution first.

**Load balancer-terminated SSL** is fully supported, but it changes authentication: during some flows Gate builds a `redirect_uri` for itself and may guess wrongly. The page says to set the URLs by hand: `gateHost` in Deck's `settings.js`, and `services.deck.baseUrl` in `spinnaker.yaml` (which enables the redirect after login); see your authentication method for the redirect setting. To pass protocol and IP information down, add to `gate-local.yml`: `server.tomcat.protocolHeader: X-Forwarded-Proto`, `remoteIpHeader: X-Forwarded-For`, `internalProxies: .*`, and, only if your environment needs it, `httpsServerPort: X-Forwarded-Port`.

**Server-terminated SSL** (terminating in Gate) is described as the de-facto way, with or without a load balancer in front. The guide generates a self-signed certificate authority with `openssl` (`ca.key`, `ca.crt`), signs server certificates for Deck (`deck.key`, `deck.crt`) and Gate, converts the Gate certificate to PKCS12 (`gate.p12`, alias `gate`) and imports it with `keytool` into `gate.jks` together with the CA certificate (alias `ca`). `keytool -list` should show `gate` as a PrivateKeyEntry and `ca` as a trustedCertEntry. Gate assumes the keystore password and key password are the same. An external CA reduces browser configuration but is optional.

Then configure Gate in `gate-local.yml` with `server.ssl.enabled: true`, `key-store`, `key-store-type: PKCS12` and `key-store-password` (`crlFile` optional). Deck is plain Apache: mount a config at `/etc/apache2/sites-enabled/spinnaker.conf` with `SSLEngine on`, `SSLCertificateFile` and `SSLCertificateKeyFile` for a VirtualHost on port 9000, with the certs in a secret volume. Deck does not support encrypted secrets.

For a custom CA used by internal communications, the page copies the system Java `cacerts`, imports the certificate with keytool, stores it as a Kubernetes secret and mounts it over `/etc/ssl/certs/java/cacerts` for the service.

## Checked

2026-11-04. The scope, SSL-first warning, load balancer settings and headers, the server-terminated procedure, gate-local.yml and Deck configuration and custom CA section were confirmed on the SSL page. Removed: the `hal config security authn ... --pre-established-redirect-uri` command (not on the page).

Method: documentation only; no commands were run.
