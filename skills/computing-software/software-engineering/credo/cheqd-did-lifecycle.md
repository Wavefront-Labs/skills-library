---
id: computing-software.software-engineering.credo.cheqd-did-lifecycle
name: cheqd-did-lifecycle
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, cheqd, did-cheqd, did-create, did-update, did-deactivate, did-resolve, did-linked-resources, did-document, kms, ed25519, issuer-did, cheqddidregistrar, cheqddidresolver, versionid, ssi]
level: practitioner
status: docs-checked
description: "Create, import, resolve, update and deactivate did:cheqd DIDs from a Credo 0.7 agent: option shapes, key mapping, DID URL forms for versions and resources, and the 0.5-tutorial traps."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/CheqdDidRegistrar.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/CheqdDidResolver.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/didCheqdUtil.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/anoncreds/utils/identifiers.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/CheqdApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/tests/cheqd-did-registrar.e2e.test.ts
  - https://docs.cheqd.io/product/llms-full.txt
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# did:cheqd lifecycle from Credo 0.7.x

**Goal:** an issuer DID on the cheqd network whose keys sit in the agent KMS, plus the ability to rotate its document,
deactivate it and resolve any `did:cheqd` (including versions and linked resources). Prerequisite: the module wiring and a
funded payer seed in `computing-software.software-engineering.credo.cheqd-module-setup`. General DID and KMS concepts are in
`computing-software.software-engineering.credo.dids-and-key-management`.

The cheqd docs' Credo tutorials (`agent.wallet.createKey`, `KeyType`, `secret: { verificationMethod }`,
`privateKeys` in `dids.import`) describe the 0.5 API. The 0.7.3 source below is what applies.

## Where it runs
Only the backend that owns the issuer identity creates, updates or deactivates DIDs (payer seed and signing keys stay
server-side). Web apps: the browser asks your Node service. Mobile wallets: resolve only. The `DidRecord` and KMS keys are
in the agent's Askar store, so back up the store and its key; without them you lose the ability to sign for the DID.

## Create (Credo generates the document)
```ts
import type { CheqdDidCreateOptions } from '@credo-ts/cheqd'

const res = await agent.dids.create<CheqdDidCreateOptions>({
  method: 'cheqd',
  options: {
    network: 'testnet',                                    // 'testnet' | 'mainnet'
    createKey: { type: { kty: 'OKP', crv: 'Ed25519' } },   // or { keyId: '<existing-kms-key-id>' }
    // methodSpecificIdAlgo?: default Uuid; versionId?: default random uuid; fee?, feeOptions?
  },
})
if (res.didState.state !== 'finished') throw new Error(res.didState.reason)
const issuerDid = res.didState.did      // did:cheqd:testnet:<uuid>
```
- Exactly one of `createKey` or `keyId`, and the key must be Ed25519 (`OKP`/`Ed25519`); other keys return `state: 'failed'`.
- The generated document uses verification method id `#key-1` of type `JsonWebKey2020` (the registrar hard-codes the JWK
  representation) and the Credo DID v1 context is added. The `DidRecord` is saved with role created and the key mapping
  `{ didDocumentRelativeKeyId: '#key-1', kmsKeyId }`, which is what later signs registry writes.
- The transaction is signed by every `authentication` verification method, then paid for by the payer seed. A rejected
  transaction returns `state: 'failed'`, `reason` starting `unknownError:` followed by the chain's raw log.
- Store `issuerDid` in your service config. It is also recoverable with `agent.dids.getCreatedDids({ method: 'cheqd' })`.

## Create from your own DID document
```ts
await agent.dids.create<CheqdDidCreateOptions>({
  method: 'cheqd',
  didDocument,                                  // a DidDocument instance with id did:cheqd:<network>:<uuid-or-base58>
  options: { keys: [{ didDocumentRelativeKeyId: '#key-1', kmsKeyId }] },
})
```
- `keys` is mandatory and must cover every `authentication` entry (all of them sign); otherwise it fails with a message
  about linking the document key ids to KMS key ids. Each listed relative id must exist in the document.
- The document is checked for spec compliance first; the DID's method-specific id must be a UUID or a base58 string
  that decodes to 16 bytes (`parseCheqdDid`), and the network must be `testnet` or `mainnet`.

## Import a DID you control elsewhere
`agent.dids.import({ did, keys: [{ didDocumentRelativeKeyId: '#key-1', kmsKeyId }], overwrite: true })` (see
`dids-and-key-management`). To use it as an AnonCreds issuer it must have a created-role `DidRecord`, because resource
writes look up `findCreatedDid`; an imported DID satisfies that, a merely resolved one does not.

## Update
```ts
import type { CheqdDidUpdateOptions } from '@credo-ts/cheqd'

const doc = (await agent.dids.resolveDidDocument(issuerDid))     // modify a copy: add a service, rotate a key, ...
const upd = await agent.dids.update<CheqdDidUpdateOptions>({
  did: issuerDid,
  didDocument: doc,                    // the COMPLETE new document
  options: { /* versionId?, fee?, feeOptions?, keys?, createKey | keyId */ },
})
```
- The DID must exist on chain, not be deactivated, and have a created-role `DidRecord` in this agent; else
  `state: 'failed'`, reason "Did not found".
- Key records for verification methods that no longer exist in the new document are dropped from the `DidRecord`; entries in
  `options.keys` are merged in. The transaction is signed by the `authentication` methods of the NEW document (the source
  carries a TODO that removed authentication entries are not signed).
- Source quirk to test before relying on it: with `options.createKey` or `keyId` the registrar creates or looks up a key and
  records the mapping, but the line that appends the new verification method to the document calls `concat` without
  assigning the result. Add the verification method to `didDocument` yourself and pass the mapping through `options.keys`.
- Each update is a paid write and creates a new document version (`versionId`, default a random uuid).

## Deactivate
```ts
import type { CheqdDidDeactivateOptions } from '@credo-ts/cheqd'
await agent.dids.deactivate<CheqdDidDeactivateOptions>({ did: issuerDid, options: { /* versionId? */ } })
```
Requires a created-role `DidRecord` and a non-deactivated DID; signed by the document's `authentication` keys. cheqd docs: the
DID stays resolvable with `deactivated: true` in its metadata, and deactivation is permanent. Credentials, schemas and
credential definitions under a deactivated DID should be treated as unusable for new issuance; plan a replacement DID
and re-registration (`anoncreds-cheqd-issuer-backend`) before you deactivate.

## Resolve
- `agent.dids.resolve(didUrl)` / `resolveDidDocument(did)` use `CheqdDidResolver`. The result's `didDocumentMetadata`
  includes `linkedResourceMetadata` (the DID's resources: id, name, resourceType, version, created).
- DID URL forms the resolver handles:
  - `did:cheqd:<network>:<id>`: current document;
  - `.../version/<versionId>`: a specific document version; `.../versions`: metadata of all versions;
  - `.../metadata`: the DID's linked-resource list; `.../resources/<resourceId>/metadata`: one resource's metadata.
- Resource content (not a DID document) is resolved by `agent.modules.cheqd.resolveResource(url)` (a thin wrapper over
  the resolver; `createResource(did, options)` likewise wraps the registrar). Accepted URLs:
  - `did:cheqd:<network>:<id>/resources/<resourceUuid>`;
  - `did:cheqd:<network>:<id>?resourceName=<n>&resourceType=<t>`, optionally with `&version=<v>` or
    `&resourceVersionTime=<unix seconds>` (picks the newest version created at or before that time). The cheqd tutorial shows an ISO date for
    `resourceVersionTime`, but the 0.7.3 resolver multiplies the value by 1000 as a number, so pass seconds.
- Resolution failures come back as `didResolutionMetadata.error` (e.g. `notFound`), not as exceptions, from `resolve`;
  `resolveDidDocument` throws.

## Failure modes
- Create fails with "Provide a didDocument or provide createKey or keyId in options": neither input was given.
- Create with your own document fails the authentication/key mapping check: add the missing entries to `options.keys`.
- Update or deactivate says "Did not found" for a DID that resolves: the agent has no created-role record for it
  (different agent or store, or the DID was imported as resolved only).
- Wrong or unfunded payer: reason text from the chain; see `cheqd-module-setup`.

## Verify
- [ ] `res.didState.state === 'finished'` and `getCreatedDids({ method: 'cheqd' })` lists the DID after a restart.
- [ ] A second agent resolves it and sees `#key-1`.
- [ ] After an update, `.../versions` lists one more version than before.
- [ ] After a deactivation, resolution metadata shows `deactivated: true` and a further update returns `failed`.

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Create/update/deactivate option shapes, defaults (`versionId` uuid, Uuid algo), JWK `#key-1`, Ed25519-only check, authentication-key signing, `DidRecord` handling, error messages, the `concat` line and the TODO: packages/cheqd/src/dids/CheqdDidRegistrar.ts.
- Resolver URL forms, `resourceName`/`resourceType`/`version`/`resourceVersionTime` handling, `linkedResourceMetadata`: dids/CheqdDidResolver.ts. DID id and network parsing: anoncreds/utils/identifiers.ts. `CheqdApi` wrappers: src/CheqdApi.ts.
- cheqd docs (fetched 2026-10-28, llms-full.txt): deactivation permanence and resolvable-after-deactivation; the 0.5-era examples named above.
- Not confirmed: the `methodSpecificIdAlgo` values other than the default Uuid (they are an enum in `@cheqd/sdk`, which was not read); runtime behaviour of the update-with-new-key path.

Method: documentation only; no commands were run.
