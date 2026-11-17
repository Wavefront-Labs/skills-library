---
id: computing-software.software-engineering.credo.openid4vc-issuer-holder-verifier
name: openid4vc-issuer-holder-verifier
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, openid4vc, oid4vci, oid4vp, openid4vci, openid4vp, sd-jwt-vc, dc-sd-jwt, mdoc, mso-mdoc, dcql, presentation-exchange, credential-offer, pre-authorized-code, digital-credentials-api, issuer, verifier, holder, express]
level: advanced
status: docs-checked
description: "Issue, hold and verify credentials over OpenID4VCI and OpenID4VP with Credo 0.7's OpenId4VcModule: issuer metadata, offers, mapper, holder binding, DCQL requests, events."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/openid4vc/src/OpenId4VcModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/openid4vc/src/OpenId4VcApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/openid4vc/src/openid4vc-verifier/OpenId4VpVerifierServiceOptions.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo-openid/src/Issuer.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo-openid/src/Holder.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo-openid/src/Verifier.ts
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
  - https://credo.js.org/guides/features/openid4vc
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenID4VC with Credo: issuer, holder, verifier (0.7.x)

**Goal:** issue credentials with OpenID for Verifiable Credential Issuance (OID4VCI) and request presentations with
OpenID for Verifiable Presentations (OID4VP), using HTTPS instead of DIDComm. Package `@credo-ts/openid4vc`, written
against **Credo 0.7.3**. No DIDComm module is needed.

## One module, three roles
Since 0.6 a single `OpenId4VcModule` replaces the separate holder/issuer/verifier modules:
```ts
import express from 'express'
import { OpenId4VcModule } from '@credo-ts/openid4vc'

const app = express()
openid4vc: new OpenId4VcModule({
  app,                                                    // optional; created for you when issuer/verifier is set
  issuer: { baseUrl: 'https://issuer.example.com/oid4vci', credentialRequestToCredentialMapper },
  verifier: { baseUrl: 'https://issuer.example.com/oid4vp' },
}),
// after agent.initialize(): app.listen(port) yourself, then add your own routes
```
- `agent.openid4vc.holder` is always there; `.issuer` and `.verifier` exist only when configured.
- Credo registers its routes (including `.well-known` metadata) on `app`; you start the server and expose it on a
  public HTTPS URL. Register your own middleware after `initialize()` so it does not shadow Credo's routes. Express 5.
- A holder-only module (no `issuer`/`verifier`) creates no Express app, which is what a mobile wallet uses; the
  package.json maps its Express router module to a React Native variant.
- `allowInsecureHttpUrls: true` in the agent config permits `http://` URLs for local development only.

## Issuer
1. Describe what you issue (keys are configuration ids):
```ts
const credentialConfigurationsSupported = {
  'degree-sd-jwt': {
    format: OpenId4VciCredentialFormatProfile.SdJwtDc,          // 'dc+sd-jwt'
    vct: 'https://issuer.example.com/vct/degree',
    cryptographic_binding_methods_supported: ['jwk'],
    credential_signing_alg_values_supported: ['ES256', 'EdDSA'],
    proof_types_supported: { jwt: { proof_signing_alg_values_supported: ['ES256', 'EdDSA'] } },
  },
} satisfies OpenId4VciCredentialConfigurationsSupportedWithFormats
const issuer = await agent.openid4vc.issuer!.createIssuer({ credentialConfigurationsSupported })
```
   Format profiles: `jwt_vc_json`, `jwt_vc_json-ld`, `ldp_vc`, `vc+sd-jwt` (older SD-JWT VC media type), `dc+sd-jwt`,
   `mso_mdoc`.
2. Create an offer and show it as a QR code or link:
```ts
const { credentialOffer, issuanceSession } = await agent.openid4vc.issuer!.createCredentialOffer({
  issuerId: issuer.issuerId,
  credentialConfigurationIds: ['degree-sd-jwt'],
  preAuthorizedCodeFlowConfig: { txCode: { input_mode: 'numeric', length: 4 } },   // optional PIN sent out of band
})
```
   The authorization-code flow uses `authorizationCodeFlowConfig` with an external authorization server listed in
   `authorizationServerConfigs` on the issuer, and can require a presentation during issuance.
3. Sign in the mapper. It receives the verified `holderBinding` (did or jwk keys), the configuration and the
   issuance session, and returns `{ type: 'credentials', format, credentials: holderBinding.keys.map(...) }`. For
   `ClaimFormat.SdJwtDc` each entry has `payload`, `holder`, `issuer` (`{ method: 'did', didUrl }` or
   `{ method: 'x5c', x5c, issuer }`) and an optional `disclosureFrame: { _sd: [...] }`. The demo's mdoc entries
   pass `issuerCertificate`, `holderKey`, `namespaces`, `docType` and `validityInfo`.
4. Track progress with `OpenId4VcIssuerEvents.IssuanceSessionStateChanged` (states from `OfferCreated` through
   `AccessTokenCreated`, `CredentialRequestReceived` to `Completed` or `Error`).

## Holder (wallet)
```ts
const offer = await agent.openid4vc.holder.resolveCredentialOffer(offerUri)
const token = await agent.openid4vc.holder.requestToken({ resolvedCredentialOffer: offer, txCode })
const { credentials } = await agent.openid4vc.holder.requestCredentials({
  resolvedCredentialOffer: offer, ...token,
  credentialConfigurationIds: Object.keys(offer.offeredCredentialConfigurations),
  credentialBindingResolver: async ({ supportedDidMethods, supportsAllDidMethods, proofTypes }) => {
    const key = await agent.kms.createKeyForSignatureAlgorithm({
      algorithm: proofTypes.jwt?.supportedSignatureAlgorithms[0] ?? 'EdDSA' })
    return { method: 'jwk', keys: [Kms.PublicJwk.fromPublicJwk(key.publicJwk)] }   // or { method: 'did', didUrls }
  },
})
for (const c of credentials) await agent.sdJwtVc.store({ record: c.record })   // or w3cCredentials / w3cV2Credentials / mdoc
```
- The binding resolver is called once per request (since 0.6) and may return several keys for batch issuance.
- Authorization-code offers: `resolveOpenId4VciAuthorizationRequest(offer, { clientId, redirectUri, scope })`, then
  `requestToken` with `code`, `clientId`, `codeVerifier`, `redirectUri`.
- Presenting: `resolveOpenId4VpAuthorizationRequest(requestUri)` gives `dcql` or `presentationExchange` matches; send
  with `acceptOpenId4VpAuthorizationRequest({ authorizationRequestPayload, dcql: { credentials:
  holder.selectCredentialsForDcqlRequest(resolved.dcql.queryResult) } })` (or the presentation-exchange equivalent).

## Verifier
```ts
const verifier = await agent.openid4vc.verifier!.createVerifier()
const { authorizationRequest, verificationSession } = await agent.openid4vc.verifier!.createAuthorizationRequest({
  verifierId: verifier.verifierId,
  requestSigner: { method: 'did', didUrl: verificationMethodId },   // or x5c, or { method: 'none' }
  dcql: { query: { credentials: [{ id: 'degree', format: 'dc+sd-jwt',
                                   meta: { vct_values: ['https://issuer.example.com/vct/degree'] } }] } },
})
// show authorizationRequest as QR; wait for OpenId4VcVerifierEvents.VerificationSessionStateChanged -> ResponseVerified
const result = await agent.openid4vc.verifier!.getVerifiedAuthorizationResponse(verificationSession.id)
```
- `version` defaults to `v1`, which does **not** allow `presentationExchange`; use DCQL, or choose `v1.draft24` /
  `v1.draft21` for presentation-definition requests (`v1.draft21` is the one aligned with ISO 18013-7 remote mdoc).
- `responseMode` defaults to `direct_post.jwt` (encrypted). `direct_post` is plain; `dc_api` / `dc_api.jwt` are for
  requests passed through the W3C Digital Credentials API in a browser, where you submit the response yourself with
  `verifyAuthorizationResponse`.
- x509 signers default to the `x509_san_dns` client id prefix; `x509_hash` is the alternative. Creating
  `x509_san_uri` requests was removed in 0.6.
- Trust: supply trusted issuers through the agent config callback `getTrustedIssuersForVerification` (0.7.1+); the
  X.509 module's `getTrustedCertificatesForVerification` callback still works but is deprecated.

## Breaking changes to remember
SIOPv2 was removed in 0.6 (`Siop*` classes became `OpenId4Vp*`; the repository README still mentions SIOPv2). OID4VCI
version identifiers changed; the 0.7.3 type is `'v1.draft11-14' | 'v1.draft15' | 'v1'` with final `v1` the default
(the 0.6 migration guide prints `v1.draft11-15`; trust the type). Draft 15 is incompatible with earlier drafts. The default SD-JWT VC `typ` became `dc+sd-jwt`. PEX results expose `claimFormat` instead of `type`.

## Verify
- [ ] `agent.openid4vc.issuer.getIssuerMetadata(issuerId)` shows your public `credential_issuer` URL and configurations.
- [ ] A test wallet completes an offer and the issuance session reaches `Completed`.
- [ ] A verification session reaches `ResponseVerified`, and a tampered or wrong-issuer credential ends in `Error`.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Module options, auto-created Express app, route ordering note: packages/openid4vc/src/OpenId4VcModuleConfig.ts. Role getters: OpenId4VcApi.ts. React Native/browser router remap: packages/openid4vc/package.json.
- Format profile values: shared/models/OpenId4VciCredentialFormatProfile.ts. Issuer setup, offers, mapper return shapes, auth servers: demo-openid/src/Issuer.ts. Holder token/credential/binding/store/present calls: demo-openid/src/Holder.ts. Verifier calls: demo-openid/src/Verifier.ts.
- Request signer options, `x509_san_dns` default, response modes and DC API note, `version` default `v1` and its PEX restriction, return shape: openid4vc-verifier/OpenId4VpVerifierServiceOptions.ts.
- Session states and event names: OpenId4VcIssuanceSessionState.ts, OpenId4VcIssuerEvents.ts, OpenId4VcVerificationSessionState.ts, OpenId4VcVerifierEvents.ts. `getVerifiedAuthorizationResponse`: OpenId4VcVerifierApi.ts.
- Module consolidation, SIOPv2 removal, draft renames, `typ` default, `claimFormat`, `x509_san_uri` removal, once-per-request binding resolver: credo.js.org 0.5-to-0.6 guide. Trusted-issuer callback: packages/core/CHANGELOG.md 0.7.1 and src/types.ts.
- Optional `issuerId` and optional `authorizationServerUrl`/`txCode` on the pre-authorized flow, OID4VCI version type: openid4vc-issuer/OpenId4VcIssuerServiceOptions.ts. `getIssuerMetadata`: demo-openid/src/Issuer.ts.

Method: documentation only; no commands were run.
