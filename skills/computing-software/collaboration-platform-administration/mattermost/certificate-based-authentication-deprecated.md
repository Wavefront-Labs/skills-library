---
id: computing-software.collaboration-platform-administration.mattermost.certificate-based-authentication-deprecated
name: certificate-based-authentication-deprecated
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [certificate-based-auth, client-side-cert, experimental-settings, deprecation]
level: advanced
status: docs-checked
description: "Experimental Mattermost certificate-based authentication with ClientSideCertEnable and ClientSideCertCheck primary or secondary, deprecated from v11.0."
sources: ["https://docs.mattermost.com/administration-guide/onboard/certificate-based-authentication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Certificate-based authentication (deprecated)

Important: experimental certificate-based authentication (CBA) is deprecated from Mattermost v11.0, and from v11 you must disable the feature (the documentation points to the client-side certificate setting in experimental configuration settings). Treat this as a migration note for older servers.

Before v11, CBA identified a user or device before granting access, adding a layer of security. It requires a licensed Enterprise server, Mattermost installed behind NGINX with SSL and HTTP/2, and a valid SSL certificate. Certificate distribution and lifecycle for personal devices can be handled by a service such as OpenSSL tooling.

Setup:
1. Set up mutual TLS (SSL client certificates) for the web app first.
2. In the ExperimentalSettings block of config.json, set ClientSideCertEnable to true and ClientSideCertCheck to either primary or secondary.
   - primary: after the client certificate is verified, the user's email is read from the certificate and the user logs in without a password.
   - secondary: after verification, the certificate email is matched against the email the user supplies; if they match the user logs in with regular email and password credentials.
3. Restart the Mattermost server.
4. Browse to the site and log in; the server requires the X.509 certificate to have an emailAddress equal to the Mattermost user's email.

On v11 and later, disable the setting, because enabling it stops the server from starting, and plan an alternative such as SAML or OpenID Connect.

## Checked

Confirmed against the Certificate-based authentication (Experimental) page: the v11.0 deprecation and startup block, Enterprise licence, NGINX with SSL and HTTP/2 prerequisite, ClientSideCertEnable and ClientSideCertCheck values, restart and the emailAddress requirement. Replaced the unsourced closing advice about proxy mutual TLS.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/certificate-based-authentication page (source rst from the mattermost/docs repo).
