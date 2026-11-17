---
id: computing-software.devops-ci-cd.spinnaker.authentication-overview
name: authentication-overview
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [authentication, gate, deck, identity-provider, oauth2, saml, ldap, x509]
level: intro
status: docs-checked
description: "Understand Spinnaker's authentication flow (Deck, Gate, identity provider), the four supported methods, and the incognito-window routine for testing configuration changes."
sources:
  - https://spinnaker.io/docs/setup/other_config/security/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three systems take part in a login: your identity provider, Gate, and Deck. Changes are made to the identity provider or to Gate; Deck itself needs no changes. Deck is a single-page app (static HTML, JavaScript and CSS, usually served by Apache but any HTTP server works) and it talks to the identity provider that Gate is configured for. Gate is the API gateway through which all traffic flows, the point where authentication is confirmed and one place where authorization is enforced.

**Methods:** OAuth 2.0/OIDC (main examples Google and GitHub), SAML 2.0 (Okta is common), LDAP (Active Directory and others such as OpenLDAP), and X.509 client certificates. X.509 can run alongside any of the others or alone.

**Testing routine.** Getting authentication right rarely works first time, and each login creates a new session in Gate's session repository, which you do not want to reuse while testing. The page highly recommends Google Chrome's Incognito mode:
1. open a new Incognito window;
2. go to Deck's endpoint;
3. observe, change the configuration, restart the affected Spinnaker service;
4. close the window and repeat.

Incognito windows share one cookie jar, so close **all** of them before retesting or the old session cookie survives.

Next steps named on the page: set up authorization and configure SSL.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Authentication overview page. Confirmed the three-part flow, method list, X.509 combination rule and the incognito procedure.
