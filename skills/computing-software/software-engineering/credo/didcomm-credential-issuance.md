---
id: computing-software.software-engineering.credo.didcomm-credential-issuance
name: didcomm-credential-issuance
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, didcomm, issue-credential-v2, rfc-0453, anoncreds, indy-vdr, cheqd, hedera, schema, credential-definition, json-ld, data-integrity, rfc-0809, vc-sd-jwt, rfc-0881, w3c-vc, auto-accept, credential-exchange]
level: practitioner
status: docs-checked
description: "Issue and hold credentials over DIDComm Issue Credential v2 with Credo 0.7: format services, AnonCreds registries, schema and cred def, offer/accept flow, events, auto-accept."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/BaseAgent.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Faber.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/credentials/DidCommCredentialsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/credentials/DidCommCredentialsModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/credentials/DidCommCredentialEvents.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/AnonCredsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/CHANGELOG.md
  - https://credo.js.org/guides/tutorials/registering-schema-and-credential-definition
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Issuing and holding credentials over DIDComm (Credo 0.7.x)

**Goal:** an issuer agent sends a credential to a holder over an existing DIDComm connection
(`computing-software.software-engineering.credo.didcomm-connections-out-of-band`), and the holder stores it.
Protocol: Issue Credential 2.0 (Aries RFC 0453), carrying one or more attachment formats.

## 1. Register formats (nothing works without this)
The credentials sub-module defaults to `DidCommCredentialV2Protocol` with an **empty** format list, so you must list
the formats both sides will use:
```ts
import { DidCommModule, DidCommCredentialV2Protocol, DidCommAutoAcceptCredential,
         DidCommJsonLdCredentialFormatService } from '@credo-ts/didcomm'
import { AnonCredsDidCommCredentialFormatService } from '@credo-ts/anoncreds/didcomm'

new DidCommModule({
  credentials: {
    autoAcceptCredentials: DidCommAutoAcceptCredential.ContentApproved,   // default Never
    credentialProtocols: [new DidCommCredentialV2Protocol({
      credentialFormats: [new AnonCredsDidCommCredentialFormatService(), new DidCommJsonLdCredentialFormatService()],
    })],
  },
})
```
| Format service (key used in `credentialFormats`) | Package | Credential |
|---|---|---|
| `AnonCredsDidCommCredentialFormatService` (`anoncreds`) | `@credo-ts/anoncreds/didcomm` | AnonCreds (needs `AnonCredsModule`) |
| `DidCommJsonLdCredentialFormatService` (`jsonld`) | `@credo-ts/didcomm` | W3C VC 1.1 with linked-data proof (`options.proofType`) |
| `DidCommDataIntegrityCredentialFormatService` (`dataIntegrity`) | `@credo-ts/didcomm` (moved from anoncreds in 0.7.1) | W3C VC (RFC 0809); VCDM 2.0 with a `cryptosuite` such as `eddsa-jcs-2022` since 0.7.1 |
| `DidCommW3cV2SdJwtCredentialFormatService` (`w3cV2SdJwt`) | `@credo-ts/didcomm` (0.7.2+) | W3C VC 2.0 secured as SD-JWT (RFC 0881), with `disclosureFrame` |
| `LegacyIndyDidCommCredentialFormatService` (`indy`) | `@credo-ts/anoncreds/didcomm` | deprecated since 0.6; only for old Indy agents |

The V1 credential protocol (`DidCommCredentialV1Protocol`) is deprecated since 0.6 but still shipped in 0.7.3. Since
0.7.2 import AnonCreds DIDComm classes from the `@credo-ts/anoncreds/didcomm` subpath (root exports still work but are
deprecated).

## 2. AnonCreds issuer prerequisites
```ts
import { AnonCredsModule } from '@credo-ts/anoncreds'
import { IndyVdrAnonCredsRegistry, IndyVdrModule } from '@credo-ts/indy-vdr'
import { CheqdAnonCredsRegistry } from '@credo-ts/cheqd/anoncreds'
import { NativeAnoncreds } from '@hyperledger/anoncreds-nodejs'
import { indyVdr } from '@hyperledger/indy-vdr-nodejs'

anoncreds: new AnonCredsModule({ registries: [new IndyVdrAnonCredsRegistry(), new CheqdAnonCredsRegistry()],
                                 anoncreds: NativeAnoncreds }),   // autoCreateLinkSecret defaults to true
indyVdr: new IndyVdrModule({ indyVdr, networks: [{ genesisTransactions, indyNamespace: '<namespace>',
                                                   isProduction: false, connectOnStartup: true }] }),
```
- The issuer needs a DID on the registry it writes to, with its key in the agent's KMS and a `DidRecord` mapping the
  key (`agent.dids.import({ did, keys: [{ didDocumentRelativeKeyId, kmsKeyId }] })`); see
  `computing-software.software-engineering.credo.dids-and-key-management`.
- Register once, then reuse the ids:
```ts
const { schemaState } = await agent.modules.anoncreds.registerSchema({
  schema: { name: 'Degree', version: '1.0.0', attrNames: ['name', 'degree'], issuerId },
  options: { endorserMode: 'internal', endorserDid: issuerId },   // Indy VDR options
})
const { credentialDefinitionState } = await agent.modules.anoncreds.registerCredentialDefinition({
  credentialDefinition: { schemaId: schemaState.schemaId, issuerId, tag: 'latest' },
  options: { supportRevocation: false, endorserMode: 'internal', endorserDid: issuerId },
})
// check state === 'finished' on both; 'failed' carries a reason
```
Revocation adds `registerRevocationRegistryDefinition`, `registerRevocationStatusList` and
`updateRevocationStatusList`; tails files need a `tailsFileService` that can upload (the default only downloads).

## 3. The exchange
Issuer:
```ts
await agent.didcomm.credentials.offerCredential({
  connectionId, protocolVersion: 'v2',
  credentialFormats: { anoncreds: { credentialDefinitionId, attributes: [
    { name: 'name', value: 'Alice' }, { name: 'degree', value: 'Computer Science' } ] } },
})
```
Holder (and issuer, if not auto-accepting) react to state changes:
```ts
import { DidCommCredentialEventTypes, DidCommCredentialState,
         type DidCommCredentialStateChangedEvent } from '@credo-ts/didcomm'

agent.events.on<DidCommCredentialStateChangedEvent>(DidCommCredentialEventTypes.DidCommCredentialStateChanged,
  async ({ payload: { credentialExchangeRecord: r } }) => {
    if (r.state === DidCommCredentialState.OfferReceived)
      await agent.didcomm.credentials.acceptOffer({ credentialExchangeRecordId: r.id })     // holder
    if (r.state === DidCommCredentialState.RequestReceived)
      await agent.didcomm.credentials.acceptRequest({ credentialExchangeRecordId: r.id })   // issuer
    if (r.state === DidCommCredentialState.CredentialReceived)
      await agent.didcomm.credentials.acceptCredential({ credentialExchangeRecordId: r.id }) // holder ack
  })
```
States run `offer-sent/received`, `request-sent/received`, `credential-issued/received`, `done`; also `declined` and
`abandoned`. Inspect what was offered with `getFormatData(id)` before accepting in a wallet UI; refuse with
`declineOffer({ credentialExchangeRecordId, sendProblemReport: true })`.

- **Auto-accept:** `Always` accepts every step; `ContentApproved` needs one manual acceptance and then automates the
  rest if nothing changes; `Never` (default) requires every call. Override per exchange with `autoAcceptCredential`.
- **Connectionless:** `createOffer({ protocolVersion, credentialFormats })` returns `{ message, credentialExchangeRecord }`;
  attach `message` to `agent.didcomm.oob.createInvitation({ messages: [message] })` (not allowed with multi-use).
- **JSON-LD in 0.7.3:** offers now check up front that the issuer verification method belongs to a DID the agent
  created and suits the proof type, so the issuer DID (for example `did:web`) must resolve at offer time. Failures throw
  `W3cJsonLdCredentialSigningNotSupportedError`.

## cheqd as the registry
Wiring, funding and the issuer-side registration calls are in `computing-software.software-engineering.credo.cheqd-module-setup`
and `computing-software.software-engineering.credo.anoncreds-cheqd-issuer-backend`; holder and verifier side in
`computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier`.

## Failure modes
- Offer or accept fails for a format: that format service is not registered on one side (both need it).
- Issuer DID imported without `keys`: Credo then assumes the legacy key id (base58 public key), the pre-0.6 key id
  format; keys created or imported through `agent.kms` get other ids, so map them explicitly.
- Calling `offerCredential` with 0.5 names (`credentialRecordId`, `agent.credentials`): renamed to
  `credentialExchangeRecordId` and `agent.didcomm.credentials` in 0.6.

## Verify
- [ ] Both exchange records reach `done`.
- [ ] Holder: `agent.modules.anoncreds.getCredentials()` (AnonCreds) or `agent.w3cCredentials` lists the credential.
- [ ] `getFormatData` on the holder shows the same attribute values the issuer sent.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Empty default format list and default protocol: DidCommCredentialsModule.ts. `autoAcceptCredentials` default Never: DidCommCredentialsModuleConfig.ts. Auto-accept meanings: models/DidCommCredentialAutoAcceptType.ts. States: models/DidCommCredentialState.ts. Event name and payload: DidCommCredentialEvents.ts.
- API methods and option names (`credentialExchangeRecordId`, `declineOffer` options, `createOffer` return shape): DidCommCredentialsApi.ts and DidCommCredentialsApiOptions.ts. Multi-use plus messages restriction: DidCommOutOfBandApi.ts.
- Format keys and services: formats/*/DidComm*CredentialFormatService.ts; AnonCreds key and module wiring, registries, Indy VDR network fields, schema/cred def calls and endorser options: demo/src/BaseAgent.ts and demo/src/Faber.ts. AnonCreds module options and `autoCreateLinkSecret` default, tails default: packages/anoncreds/src/AnonCredsModuleConfig.ts. AnonCreds API method names: AnonCredsApi.ts.
- Legacy key id fallback for DIDs without key mapping: credo.js.org 0.5-to-0.6 guide ("DID signing requires DidRecord").
- Data Integrity move and VCDM 2.0 (0.7.1), RFC 881 handler and subpath imports (0.7.2), JSON-LD preflight (0.7.3), protocol deprecations (0.6.0): packages/didcomm/CHANGELOG.md and packages/core/CHANGELOG.md on v0.7.x.

Method: documentation only; no commands were run.
