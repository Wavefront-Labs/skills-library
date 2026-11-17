---
id: computing-software.software-engineering.methods.credo-web-issuer-verifier-service
name: credo-web-issuer-verifier-service
category: computing-software
field: software-engineering
product: methods
tags: [method, recipe, credo, credo-ts, issuer, verifier, web-app, nodejs, backend, didcomm, openid4vc, oid4vci, oid4vp, qr-code, digital-credentials-api, decentralized-identity, production-tier]
level: advanced
status: draft
description: "Recipe: a web issuer/verifier service with a Credo 0.7 Node.js backend and a browser front end, via DIDComm or OpenID4VC, with skills in order and gates per phase."
sources:
  - https://credo.js.org/guides/concepts/platform-and-environment
  - https://github.com/openwallet-foundation/credo-ts/tree/v0.7.x/demo
  - https://github.com/openwallet-foundation/credo-ts/tree/v0.7.x/demo-openid
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/openid4vc/src/openid4vc-verifier/OpenId4VpVerifierServiceOptions.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Method: web issuer and verifier service on a Credo backend (production tier)

## Outcome
A web application where an organisation issues credentials to users' wallets and verifies presentations. The browser
front end never runs Credo: Credo's docs list only Node.js and React Native as runtimes, so the agent runs in a Node.js
backend and the web page shows QR codes or links and polls or subscribes for results. Two channels are possible and can
coexist: DIDComm (connection-based, AnonCreds or W3C formats) and OpenID4VC (HTTPS, SD-JWT VC, mdoc, W3C).

## Ingredients
| Phase | Skill ids |
|---|---|
| 1. Backend agent | `computing-software.software-engineering.credo.agent-setup-nodejs` |
| 2. Issuer identity | `computing-software.software-engineering.credo.dids-and-key-management`, `computing-software.software-engineering.credo.askar-module-store-config`, `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup` |
| 3a. DIDComm path | `computing-software.software-engineering.credo.didcomm-connections-out-of-band`, `computing-software.software-engineering.credo.didcomm-credential-issuance`, `computing-software.software-engineering.credo.didcomm-proof-requests` |
| 3b. OpenID4VC path | `computing-software.software-engineering.credo.openid4vc-issuer-holder-verifier` |
| 3c. AnonCreds on cheqd (if you register on cheqd) | `computing-software.software-engineering.credo.cheqd-module-setup`, `computing-software.software-engineering.credo.cheqd-did-lifecycle`, `computing-software.software-engineering.credo.anoncreds-cheqd-issuer-backend`, `computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier` |
| 4. Web front end and API | `computing-software.software-engineering.api-design.long-running-operations`, `computing-software.web-development.node-express.migrating-express-4-to-5`, `computing-software.web-development.node-express.keeping-secrets-and-pii-out-of-logs` |
| 5. Operations and upgrades | `computing-software.software-engineering.credo.upgrading-between-versions` |

## Ordering law
The agent and its storage exist before anything can be signed. The issuer DID (or X.509 certificate for mdoc and
x5c-signed SD-JWT) must be published and resolvable before the first offer, because holders and verifiers resolve it
during the exchange (since 0.7.3 a JSON-LD DIDComm offer even resolves it at offer time). The channel is chosen per
credential format and wallet population before the front end is built, because it decides what the page displays
(an out-of-band invitation versus an OID4VCI offer or OID4VP request) and which events the backend forwards.

## Phases and gates
1. **Backend agent.** Askar store on Postgres (or SQLite for a single instance), keys from a secret manager, public
   HTTPS URL configured as the DIDComm endpoint and/or OpenID4VC `baseUrl`. Gate: the agent restarts without losing
   records and the public URL answers from outside the network.
2. **Issuer identity.** Gate: the issuer DID resolves from a different machine and its verification method maps to a
   key in the agent's KMS (`agent.dids.import` with `keys`, or created by the agent).
3. **Channel.**
   - 3a DIDComm: the page shows an out-of-band invitation (optionally with an attached offer or proof request); the
     backend reacts to connection, credential and proof state events. Gate: a reference wallet completes connect,
     issue and verify, and the verifier checks `isVerified` plus restrictions on issuer.
   - 3b OpenID4VC: the backend creates issuer and verifier records, offers and authorization requests, and listens to
     issuance and verification session events. Gate: a reference wallet completes pre-authorized issuance (with a
     transaction code if used) and a DCQL presentation that reaches `ResponseVerified`.
   - Same-browser option: OID4VP `responseMode: 'dc_api'` / `'dc_api.jwt'` lets the page pass the request to the W3C
     Digital Credentials API and post the response back for `verifyAuthorizationResponse`. Gate: works in the browsers
     your users run; keep the QR flow as fallback.
4. **Front end.** The page asks the backend to create an offer or request, renders the returned URI as a QR code and
   link, and learns the outcome from the backend (polling or a push channel keyed by session or out-of-band id). Gate:
   abandoned or expired sessions show a clear state; no credential data beyond what the business needs reaches the
   browser.
5. **Operations.** Gate: two backend instances share one database with only one running storage updates; a Credo
   patch upgrade is rehearsed on a copy of production data; the DIDComm mediator queue or OpenID4VC session records
   survive a restart.

## Acceptance criteria
- At least one independent wallet completes every flow you offer, on each channel you offer.
- Verification decisions check issuer trust (AnonCreds restrictions, trusted DIDs or X.509 chains), not only signatures.
- Secrets live outside source control; logs contain no credential payloads.
- Upgrade rehearsal passed for the Credo version in production.

## Failure modes this method prevents
- Trying to run the agent in the browser bundle.
- Offers that fail because the issuer DID was not resolvable yet.
- Verifiers that accept any well-formed presentation regardless of issuer.
- Session state lost on restart because in-memory queues or a single SQLite file were used behind a load balancer.

## Verify
Run the five gates per release. This method is a draft: it has not been executed end to end, and the gates are the
author's recommended thresholds rather than figures from the Credo docs.
