---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-ecp-profile
name: saml-ecp-profile
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-ecp-profile, saml-advanced-profiles, ecp, paos, non-browser, soap, enhanced-client, identity-protocols]
level: sme
status: docs-checked
description: "Use the SAML ECP profile for non-browser clients with PAOS bindings: HTTP headers, SOAP header blocks and the seven-step flow."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced Client or Proxy (ECP) profile

Goal: do SAML SSO from a command-line or thick client that can speak PAOS (reverse SOAP) and knows how to reach the right IdP.

Flow (profiles 4.2.3):
1. The ECP requests a resource at the SP with `Accept: text/html; application/vnd.paos+xml` and `PAOS: ver='urn:liberty:paos:2003-08' ; 'urn:oasis:names:tc:SAML:2.0:profiles:SSO:ecp'` (PAOS version plus the ECP service value).
2. If the SP needs a security context it answers HTTP 200 with one SOAP envelope: an AuthnRequest in the body, a PAOS request header block and an ECP Request header block (both targeted at the ECP with actor `http://schemas.xmlsoap.org/soap/actor/next`), and optionally an ECP RelayState block. The ECP Request block carries things like the acceptable IdP list (IDPList), whether the ECP may interact with the principal, and the SP's display name.
3. The ECP determines the IdP (implementation-dependent; it MAY use the IdP discovery profile).
4. The ECP MUST strip the PAOS, ECP RelayState and ECP Request header blocks and send the AuthnRequest to the IdP using a modified SAML SOAP binding. The IdP MAY answer with presentation-oriented HTTP (for example a login form) and a sequence of exchanges may follow, but must finally complete the SOAP exchange.
5. The IdP establishes the principal's identity by any means subject to the request (ForceAuthn true forces fresh authentication; RequestedAuthnContext applies).
6. The IdP returns a SAML Response (or SOAP fault) in a SOAP message with a mandatory ECP Response header block and optional ECP RelayState block.
7. The ECP removes those header blocks, MAY add a PAOS Response block and an ECP RelayState block, and forwards the response to the SP over PAOS. If the SP's PAOS request block had a messageID, the PAOS Response block is required. If a RelayState was supplied by either party the ECP MUST return an identical block; the SP's value takes precedence.

The SP then processes the Response by the same rules as browser SSO with HTTP POST.

Gotchas:
- The IdP side needs an ECP-capable SOAP endpoint; check the IdP's metadata and documentation, since support varies by product.
- The IdP may authenticate by any means, so credentials may pass through the client; use only trusted clients.

Verify: send step 1 with curl and the two headers above to a test SP and confirm the 200 response contains a SOAP envelope with the PAOS and ECP header blocks and an AuthnRequest.

## Checked

Method: 2026-11-09 docs-only; read SAML 2.0 profiles (OASIS PDF, text via pdftotext) section 4.2.3 steps 1-8 in full. Removed unsourced claims about cloud IdPs and OIDC device flow; schema detail of 4.2.4 was only skimmed.
