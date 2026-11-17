---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-proxying-scoping
name: saml-proxying-scoping
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-proxying-scoping, saml-advanced-profiles, proxy, scoping, proxycount, proxyrestriction, hub-and-spoke, idplist, identity-protocols]
level: sme
status: docs-checked
description: "Build SAML proxies and hubs: Scoping/ProxyCount, IDPList, ProxyRestriction, ProxyCountExceeded and what the proxy must carry forward."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IdP proxying, Scoping and ProxyRestriction

Goal: route SSO through an intermediary without breaking the constraints the requester and upstream IdP set.

Method: an IdP that receives an AuthnRequest may proxy it to another IdP (it then acts as a requester upstream). Two controls exist:
- Requester side, `samlp:Scoping` in the AuthnRequest: `ProxyCount` (indirections permitted between the receiving IdP and the IdP that finally authenticates; 0 means no proxying, omitted means no restriction), an advisory `IDPList` of acceptable IdPs, and `RequesterID` (zero or more, the chain of requesters being acted for).
- Assertion side, `saml:Conditions/ProxyRestriction`: `Count` (maximum indirections from this assertion to any assertion issued from it) and optional `Audience` elements limiting who may receive derived assertions. Count 0 forbids issuing further assertions on its basis. Only one ProxyRestriction is allowed per Conditions.

Proxy processing rules (core 3.4.1.5.1):
- Proxy only if ProxyCount is absent or greater than zero. An IdP MUST NOT proxy at ProxyCount 0; unless it can authenticate the user itself it returns second-level status `urn:oasis:names:tc:SAML:2.0:status:ProxyCountExceeded`.
- The new upstream AuthnRequest must carry equivalent or stricter versions of the original request's information (for example authentication context policy). It may choose its own NameIDPolicy.
- The new request's ProxyCount must be at most one less than the original; if the original had none, the new one SHOULD set one.
- If the original had an IDPList, the new request must have one too; the proxy may append IdPs but not remove any.
- The proxy builds a new assertion on its own behalf, copying relevant data; its Subject identifier must satisfy the original requester's NameIDPolicy. Any ProxyRestriction on the upstream assertion must not be violated by the assertions the proxy issues (reduced Count, subset of Audiences).

Gotchas:
- Downstream SPs trust the proxy, not the upstream IdP, so the proxy decides which attributes it re-asserts.
- Test logout and session mapping across hops explicitly; the spec text above covers only authentication.

Verify: send an AuthnRequest with ProxyCount="0" to a proxy that cannot authenticate locally and confirm it returns ProxyCountExceeded rather than forwarding.

## Checked

Method: 2026-11-09 docs-only; read SAML 2.0 core (OASIS PDF, text via pdftotext) sections 2.5.1.6, 3.4.1.2 and 3.4.1.5.1 in full; the profiles PDF does not cover proxying so it was dropped as a source. Practice statements about SLO and per-attribute authority are advice, not spec text.
