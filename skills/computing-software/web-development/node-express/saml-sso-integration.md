---
id: computing-software.web-development.node-express.saml-sso-integration
name: saml-sso-integration
category: computing-software
field: web-development
product: node-express
tags: [saml-sso, saml, enterprise-sso, xml-signature-wrapping, node-saml, authentication]
level: advanced
status: docs-checked
description: "Integrating SAML 2.0 SSO as a service provider: metadata exchange, validating signed assertions, audience/recipient/time/InResponseTo checks, wrapping attacks and cert rotation."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html
  - https://github.com/node-saml/node-saml
  - https://github.com/SAML-Toolkits/ruby-saml/security/advisories
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML SSO integration

## 1. Setup per customer IdP (Okta, Entra ID, Google Workspace, ADFS)
- You publish SP metadata: `entityID` (e.g. `https://app.example.com/saml/acme`), ACS URL (`.../saml/acme/acs`, HTTP-POST binding), NameID format (persistent preferred over email), signing requirements.
- They give IdP metadata: SSO URL, entityID, signing certificate(s). Store per tenant; support two active certs for rotation.

## 2. Use a maintained library
Node `@node-saml/node-saml` (`@node-saml/passport-saml` wraps it for Passport), Python `python3-saml`/`pysaml2`, Ruby `ruby-saml` (keep patched: several signature-bypass CVEs were fixed in 2024-2025), Java OpenSAML/Spring Security. Never hand-roll XML signature validation.
```js
const saml = new SAML({
  callbackUrl: "https://app.example.com/saml/acme/acs",
  entryPoint: idp.ssoUrl, issuer: spEntityId, idpCert: idp.certs,
  wantAssertionsSigned: true, wantAuthnResponseSigned: false,
  audience: spEntityId, acceptedClockSkewMs: 120000,
  validateInResponseTo: "always", requestIdExpirationPeriodMs: 300000,
});
const { profile } = await saml.validatePostResponseAsync(req.body);
```
node-saml defaults: `wantAssertionsSigned` and `wantAuthnResponseSigned` are both `true`, `audience` defaults to `issuer`, `acceptedClockSkewMs` to 0, `validateInResponseTo` to `"never"` (set it explicitly) and `requestIdExpirationPeriodMs` to 8 hours. The snippet relaxes the response-level signature requirement, so the assertion itself must be signed.

## 3. Checks that must pass
- Signature valid over the **assertion** you read from (XML signature wrapping attacks insert a second unsigned assertion).
- `Audience` = your entityID; `Recipient`/`Destination` = your ACS URL; `NotBefore`/`NotOnOrAfter` with small skew.
- `InResponseTo` matches a request you issued (store request ids); reject replays by caching assertion IDs until expiry.
- `Issuer` = the tenant's IdP; the cert belongs to that tenant (no cross-tenant cert confusion).
- Prefer disabling IdP-initiated SSO (an unsolicited response has no request id to match `InResponseTo` against); if required, accept only for specific tenants.
- `RelayState` is attacker-controllable: validate as a relative redirect.

## 4. Lifecycle
- JIT provisioning from attributes (email, name, groups) mapped per tenant; require verified domain ownership before allowing a tenant to claim users of a domain.
- Deprovisioning: SAML login alone does not remove users; add SCIM or short app sessions with re-auth.
- Enforce SSO per tenant (disable password login for those users) and keep a break-glass admin.

## Verify
- [ ] Test suite with tampered signature, wrong audience, expired assertion, replayed assertion and unsolicited response: all rejected.

## Checked

2026-10-25 against the node-saml README and types (node-saml/node-saml main), the ruby-saml security advisories and OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24). Confirmed: node-saml option names callbackUrl, entryPoint, issuer, idpCert, audience, wantAssertionsSigned, wantAuthnResponseSigned, acceptedClockSkewMs, validateInResponseTo and requestIdExpirationPeriodMs, and validatePostResponseAsync; node-saml defaults: both signature requirements true, audience defaults to issuer, clock skew 0, validateInResponseTo never, request id lifetime 8 hours; ruby-saml had SAML authentication bypass advisories in 2024 and 2025; the OWASP SAML cheat sheet covers signature wrapping and InResponseTo.

Method: documentation only; no commands were run.
