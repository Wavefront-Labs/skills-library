---
id: computing-software.systems-network-administration.apache-guacamole.saml-sso
name: saml-sso
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, saml, sso, single-sign-on, saml-idp-metadata-url, saml-entity-id, saml-callback-url, saml-strict, saml-group-attribute, identity-provider]
level: practitioner
status: docs-checked
description: "Set up SAML 2.0 SSO in Guacamole: saml-idp-metadata-url or saml-idp-url, saml-entity-id, saml-callback-url, strict mode, group attribute, request signing and compression."
sources:
  - https://guacamole.apache.org/doc/gug/saml-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML SSO

Install: `saml/guacamole-auth-sso-saml-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `SAML_ENABLED=true`.

Properties (Docker uppercase):
| Property | Default / notes |
|---|---|
| `saml-idp-metadata-url` | IdP metadata XML via `https://` or `file://`; if set, `saml-idp-url` is ignored |
| `saml-idp-url` | required without metadata |
| `saml-entity-id` | required unless metadata supplies it; usually the Guacamole URL |
| `saml-callback-url` | required; IdP POSTs the assertion here (POST only) |
| `saml-strict` | `true`; use `false` only for non-production tests |
| `saml-debug` | `false` |
| `saml-compress-request`, `saml-compress-response` | `true` |
| `saml-group-attribute` | `groups` |
| `saml-x509-cert-path` | unset: requests unsigned |
| `saml-private-key-path` | unset: requests unencrypted |

Login behaviour: `extension-priority: saml` for auto-redirect, `*, saml` for form plus link.

On the IdP, register Guacamole as a Service Provider with the entity ID and callback URL above; configuring the IdP is beyond the scope of the manual and varies by IdP.

The manual says group attributes are most useful when layered with other authentication modules (apache-guacamole.database-auth-overview, apache-guacamole.mfa-overview-sso).

Verify: the browser redirects to the IdP and the assertion POST to the callback logs you in; enable `saml-debug` if not.

## Checked

2026-11-04. Confirmed against the Guacamole manual page saml-auth: jar name and location, SAML_ENABLED, every property and default in the table, metadata overriding saml-idp-url, POST-only callback, strict mode advice, request signing and encryption paths, extension-priority forms for redirect versus login form, and the Tomcat restart. Changed: replaced two unsupported statements (no SP metadata export; SAML authenticates only, MFA best at the IdP) with the page's own wording.

Method: documentation only; no commands were run.
