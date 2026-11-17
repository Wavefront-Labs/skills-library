---
id: computing-software.software-engineering.credo.dids-and-key-management
name: dids-and-key-management
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, did, did-key, did-peer, did-jwk, did-web, did-indy, did-sov, did-cheqd, did-hedera, did-webvh, did-resolver, did-registrar, kms, key-management, agent-kms, did-record, decentralized-identifiers]
level: practitioner
status: docs-checked
description: "Create, import and resolve DIDs with Credo 0.7 (did:key, did:jwk, did:peer, did:web, did:indy, did:cheqd) and manage their keys through agent.kms and DidRecord key mappings."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/dids/DidsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/dids/DidsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/dids/methods/key/KeyDidRegistrar.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/kms/options/KmsCreateKeyOptions.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/CheqdDidRegistrar.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/indy-vdr/src/dids/IndyVdrIndyDidRegistrar.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Faber.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo-openid/src/BaseAgent.ts
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DIDs, registrars, resolvers and keys in Credo (0.7.x)

**Goal:** the agent can resolve other parties' DIDs and create or import its own DIDs whose private keys it controls.
Since 0.6, keys live in the KMS (`agent.kms`) under a key id, and a DID is only usable for signing if a `DidRecord`
maps its verification methods to those key ids.

## Methods available (0.7.3)
| Method | Resolve | Create | Where |
|---|---|---|---|
| did:key | yes | yes | core (always registered) |
| did:peer (0, 1, 2, 4) | yes | yes | core (always registered); DIDComm uses did:peer:4 by default |
| did:jwk | yes | yes | core default |
| did:web | yes | no registrar in core | core default resolver |
| did:indy / did:sov | `IndyVdrIndyDidResolver`, `IndyVdrSovDidResolver` | `IndyVdrIndyDidRegistrar` | `@credo-ts/indy-vdr` |
| did:cheqd | `CheqdDidResolver` | `CheqdDidRegistrar` | `@credo-ts/cheqd` |
| did:hedera | `HederaDidResolver` | `HederaDidRegistrar` | `@credo-ts/hedera` |
| did:webvh | package `@credo-ts/webvh` | | listed in the README |

## Configure the DIDs module
```ts
import { DidsModule, WebDidResolver, KeyDidRegistrar, JwkDidRegistrar } from '@credo-ts/core'
import { CheqdDidRegistrar, CheqdDidResolver } from '@credo-ts/cheqd'
import { IndyVdrIndyDidResolver } from '@credo-ts/indy-vdr'

dids: new DidsModule({
  resolvers: [new WebDidResolver(), new IndyVdrIndyDidResolver(), new CheqdDidResolver()],
  registrars: [new KeyDidRegistrar(), new JwkDidRegistrar(), new CheqdDidRegistrar()],
}),
```
**Gotcha:** passing `resolvers` or `registrars` **replaces** the defaults. Credo re-adds only the did:key and did:peer
ones, so list `WebDidResolver` (and `JwkDidResolver`/`JwkDidRegistrar`) yourself if you still need them.
`publicDidMethods` (default `web, indy, sov, cheqd, hedera, webvh`) controls which documents may be cached across
tenants.

## Keys first: the KMS
```ts
const { keyId, publicJwk } = await agent.kms.createKey({ type: { kty: 'OKP', crv: 'Ed25519' } })
// EC: { kty: 'EC', crv: 'P-256' }; RSA: { kty: 'RSA', modulusLength: 2048 }
const key = await agent.kms.createKeyForSignatureAlgorithm({ algorithm: 'ES256' })   // pick by JWA alg
const { keyId: imported } = await agent.kms.importKey({ privateJwk })                 // e.g. from transformPrivateKeyToPrivateJwk (@credo-ts/askar)
```
The 0.5-to-0.6 migration guide shows `createKey({ type: 'ed25519' })`; the 0.7.3 type is the JWK-style object above.
Askar is the default KMS backend: supported key types, import, delete, store key rotation and backups are in
`computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`; store set-up in
`computing-software.software-engineering.credo.askar-module-store-config`.

## Create a DID
```ts
import type { KeyDidCreateOptions } from '@credo-ts/core'
const res = await agent.dids.create<KeyDidCreateOptions>({
  method: 'key',
  options: { createKey: { type: { kty: 'OKP', crv: 'Ed25519' } } },   // or { keyId } for an existing key
})
if (res.didState.state !== 'finished') throw new Error(res.didState.reason)
const did = res.didState.did
```
- did:cheqd: `options: { network: 'testnet', methodSpecificIdAlgo?, createKey | keyId }` (Ed25519 only); to write, the
  `CheqdModule` network entry needs a `cosmosPayerSeed` for the paying account
  (`networks: [{ network, cosmosPayerSeed, rpcUrl? }]`).
- did:indy: `options: { endorserDid, endorserMode: 'internal' | 'external', ... }`. `internal` means the endorser DID's
  key is in this wallet; `external` saves the DID record and returns `didState.state: 'action'` with
  `action: 'endorseIndyTransaction'` and the prepared `nymRequest` for the endorser to sign and submit.
- did:key cannot be updated or deactivated; registrars return `state: 'failed'` with `notSupported`.
- `update()` and `deactivate()` exist on `agent.dids` for methods whose registrar supports them.

## Import a DID you already control
```ts
await agent.dids.import({
  did: 'did:cheqd:testnet:<id>',
  keys: [{ didDocumentRelativeKeyId: '#key-1', kmsKeyId: keyId }],
  overwrite: true,               // update an existing record instead of throwing
})
```
If `didDocument` is omitted it is resolved. Each `didDocumentRelativeKeyId` must exist in the document. Without
`keys`, Credo assumes the pre-0.6 key id format (base58 public key).

## Resolve
- `agent.dids.resolve(didUrl)` returns the full resolution result (document plus resolution metadata, following the
  W3C DID Resolution interface); check the metadata for errors.
- `agent.dids.resolveDidDocument(didUrl)` returns just the document and throws if it cannot be resolved.
- `agent.dids.getCreatedDids({ method })` lists your own DIDs.

## did:cheqd in depth
Create, update, deactivate and resolve forms: `computing-software.software-engineering.credo.cheqd-did-lifecycle`; module wiring
and payer seed: `computing-software.software-engineering.credo.cheqd-module-setup`.

## Failure modes
- did:web stops resolving after you add a ledger resolver: defaults were replaced (see gotcha).
- Signing with a DID created elsewhere fails: import it with the key mapping first.
- did:indy writes fail with an endorser DID whose key is not in the wallet while using `internal` mode.

## Verify
- [ ] `resolveDidDocument(did)` returns a document whose verification method ids match your `keys` mapping.
- [ ] `getCreatedDids({ method: 'key' })` includes the new DID after a restart.
- [ ] A test credential or JWS signed with the DID verifies on another agent.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Default resolvers/registrars, forced did:key/did:peer, `publicDidMethods`: packages/core/src/modules/dids/DidsModuleConfig.ts.
- `create`/`update`/`deactivate`/`resolve`/`resolveDidDocument`/`getCreatedDids`/`import` behaviour: DidsApi.ts. did:key options and not-supported update/deactivate: methods/key/KeyDidRegistrar.ts. Peer DID numalgo values: methods/peer/didPeer.ts.
- KMS create-key option shape: packages/core/src/modules/kms/options/KmsCreateKeyOptions.ts; `importKey`, `createKeyForSignatureAlgorithm`, `transformPrivateKeyToPrivateJwk`: demo-openid/src/BaseAgent.ts, demo-openid/src/Holder.ts, demo/src/Faber.ts.
- did:cheqd options: packages/cheqd/src/dids/CheqdDidRegistrar.ts; cheqd network config: packages/cheqd/src/CheqdModuleConfig.ts. did:indy endorser options: packages/indy-vdr/src/dids/IndyVdrIndyDidRegistrar.ts. Resolver/registrar class names: demo/src/BaseAgent.ts.
- Method list (did:web, did:webvh, did:key, did:jwk, did:peer, did:sov, did:indy, did:cheqd, did:hedera): repository README. DidRecord requirement and legacy key id fallback: credo.js.org 0.5-to-0.6 guide.

Method: documentation only; no commands were run.
