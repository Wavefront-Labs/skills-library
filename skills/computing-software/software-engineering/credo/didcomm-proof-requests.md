---
id: computing-software.software-engineering.credo.didcomm-proof-requests
name: didcomm-proof-requests
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, didcomm, present-proof-v2, rfc-0454, proof-request, presentation, anoncreds, predicates, zero-knowledge, dif-presentation-exchange, presentation-definition, verifier, holder, selective-disclosure]
level: practitioner
status: docs-checked
description: "Request and answer proofs over DIDComm Present Proof v2 with Credo 0.7: AnonCreds attributes and predicates, DIF Presentation Exchange, credential selection, verification state."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Faber.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Alice.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/proofs/DidCommProofsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/proofs/DidCommProofEvents.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/formats/AnonCredsDidCommProofFormat.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/models/exchange.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/proofs/formats/dif-presentation-exchange/DidCommDifPresentationExchangeProofFormat.ts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proof requests and presentations over DIDComm (Credo 0.7.x)

**Goal:** a verifier asks a connected holder to prove claims; the holder picks matching credentials and presents; the
verifier checks the result. Protocol: Present Proof 2.0 (Aries RFC 0454). The credentials must already be held
(`computing-software.software-engineering.credo.didcomm-credential-issuance`).

## Register proof formats
Like credentials, the proofs sub-module defaults to `DidCommProofV2Protocol` with **no** formats:
```ts
import { DidCommProofV2Protocol, DidCommAutoAcceptProof,
         DidCommDifPresentationExchangeProofFormatService } from '@credo-ts/didcomm'
import { AnonCredsDidCommProofFormatService } from '@credo-ts/anoncreds/didcomm'

proofs: {
  autoAcceptProofs: DidCommAutoAcceptProof.ContentApproved,     // default Never
  proofProtocols: [new DidCommProofV2Protocol({
    proofFormats: [new AnonCredsDidCommProofFormatService(), new DidCommDifPresentationExchangeProofFormatService()],
  })],
},
```
Format keys: `anoncreds` (AnonCreds proofs), `presentationExchange` (DIF Presentation Exchange over W3C credentials),
and the deprecated `indy` (`LegacyIndyDidCommProofFormatService`).

## Verifier: request (AnonCreds)
```ts
await agent.didcomm.proofs.requestProof({
  connectionId, protocolVersion: 'v2',
  proofFormats: { anoncreds: {
    name: 'age-and-degree', version: '1.0',
    requested_attributes: { degree: { name: 'degree', restrictions: [{ cred_def_id: credentialDefinitionId }] } },
    requested_predicates: { adult: { name: 'age', p_type: '>=', p_value: 18,
                                     restrictions: [{ cred_def_id: credentialDefinitionId }] } },
    // nonce: optional since 0.7.0; a secure random one is generated if omitted
  } },
})
```
- `requested_attributes` entries take `name` or `names` (several attributes from one credential), `restrictions`
  and `non_revoked`. Predicates support `>=`, `>`, `<=`, `<` against a numeric `p_value` and reveal only that the
  condition holds.
- Always put `restrictions` (for example `cred_def_id`, `issuer_id`, `schema_id`) on what matters; without them any
  credential with that attribute name satisfies the request, including self-issued ones.
- `non_revoked: { from?, to? }` (numeric timestamps) asks for proof of non-revocation in that interval.

## Verifier: request (DIF Presentation Exchange)
```ts
proofFormats: { presentationExchange: {
  presentationDefinition: { id: 'degree', input_descriptors: [ /* constraints on W3C credential fields */ ] },
  options: { challenge: '<random>', domain: 'verifier.example.com' },
} }
```

## Holder: respond
```ts
import { DidCommProofEventTypes, DidCommProofState, type DidCommProofStateChangedEvent } from '@credo-ts/didcomm'

agent.events.on<DidCommProofStateChangedEvent>(DidCommProofEventTypes.ProofStateChanged, async ({ payload }) => {
  const r = payload.proofRecord
  if (r.state !== DidCommProofState.RequestReceived) return
  const selected = await agent.didcomm.proofs.selectCredentialsForRequest({ proofExchangeRecordId: r.id })
  await agent.didcomm.proofs.acceptRequest({ proofExchangeRecordId: r.id, proofFormats: selected.proofFormats })
})
```
- `selectCredentialsForRequest` picks automatically; for a wallet UI call `getCredentialsForRequest` to list every
  candidate, let the user choose, and pass the choice in `proofFormats`.
- `declineRequest({ proofExchangeRecordId, ... })` refuses; `negotiateRequest` sends a counter-proposal.
- Note the event enum key is `ProofStateChanged` (value `DidCommProofStateChanged`) and the payload field is
  `proofRecord`, unlike the credential event's `credentialExchangeRecord`.

## Verifier: check the result
On `presentation-received` (or `done` with auto-accept) read `proofRecord.isVerified` and `errorMessage`, then
`acceptPresentation({ proofExchangeRecordId })` to send the ack. Use `getFormatData(id)` to read the revealed
attribute values and predicate results for your business logic. States: `request-sent/received`,
`presentation-sent/received`, `done`, `declined`, `abandoned` (plus `proposal-*`).

## Connectionless proofs
`createRequest({ protocolVersion, proofFormats })` returns the message and record; embed the message in an out-of-band
invitation with `handshake: false` for a one-shot QR verification.

## Failure modes
- Requests fail on both sides when one side lacks the format service.
- Missing restrictions: the proof verifies cryptographically but proves nothing about who issued the credential.
- Trusting `state === 'done'` alone: always check `isVerified`.
- Using 0.5 names (`proofRecordId`, `agent.proofs`): now `proofExchangeRecordId` and `agent.didcomm.proofs`.

## Verify
- [ ] Verifier record ends `done` with `isVerified === true`.
- [ ] A request for a predicate the holder cannot meet (for example `>= 200`) does not produce a verified proof.
- [ ] `getFormatData` shows only the requested attributes, not the whole credential.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Empty default proof formats and V2 default: DidCommProofsModule.ts. `autoAcceptProofs` default Never: DidCommProofsModuleConfig.ts. Event enum key, value and `proofRecord` payload: DidCommProofEvents.ts. States: models/DidCommProofState.ts. `isVerified`/`errorMessage`: repository/DidCommProofExchangeRecord.ts.
- API methods (`requestProof`, `createRequest`, `selectCredentialsForRequest`, `getCredentialsForRequest`, `acceptRequest`, `declineRequest`, `negotiateRequest`, `acceptPresentation`, `getFormatData`) and option names: DidCommProofsApi.ts and DidCommProofsApiOptions.ts.
- AnonCreds request shape, optional nonce, attribute/predicate fields and predicate operators: packages/anoncreds/src/formats/AnonCredsDidCommProofFormat.ts and models/exchange.ts; format key: AnonCredsDidCommProofFormatService.ts. Caller-supplied nonce added in v0.7.0 release notes.
- DIF PE format key and request shape: DidCommDifPresentationExchangeProofFormat.ts and its service.
- Request and accept flow: demo/src/Faber.ts and demo/src/Alice.ts.
- The restriction advice follows from the request model (restrictions are optional filters); it is guidance, not a quoted doc statement.

Method: documentation only; no commands were run.
