---
id: computing-software.software-engineering.credo.anoncreds-cheqd-issuer-backend
name: anoncreds-cheqd-issuer-backend
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, anoncreds, cheqd, did-cheqd, issuer, schema, credential-definition, revocation-registry, revocation-status-list, tails-file, tailsfileservice, cheqdanoncredsregistry, did-linked-resources, nodejs, backend, web-app, verifiable-credentials]
level: practitioner
status: docs-checked
description: "Register AnonCreds schemas, credential definitions, revocation registries and status lists on cheqd from a Credo 0.7 Node.js issuer backend: calls, resource ids, tails hosting, costs."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/anoncreds/services/CheqdAnonCredsRegistry.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/anoncreds/utils/identifiers.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/AnonCredsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/services/tails/TailsFileService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/services/tails/BasicTailsFileService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/AnonCredsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/tests/setupCheqdModule.ts
  - https://docs.cheqd.io/product/llms-full.txt
  - https://docs.cheqd.io/product/advanced/anoncreds.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AnonCreds on cheqd: the issuer backend (Credo 0.7.x, Node.js)

**Goal:** an issuer service that has published its schema, credential definition and (optionally) revocation registry and
status list as cheqd DID-Linked Resources, so any wallet or verifier can resolve them from the ids inside a credential. Runs
in a Node.js process only (it needs the payer seed, the issuer's private keys and the AnonCreds native binding); a web front
end triggers it through your own API. Prerequisites: `computing-software.software-engineering.credo.cheqd-module-setup` (wiring,
funded payer seed) and an issuer DID from `computing-software.software-engineering.credo.cheqd-did-lifecycle`. Holder and
verifier side: `computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier`.

## How cheqd stores AnonCreds objects
Each object is one cheqd DID-Linked Resource under the issuer DID, written by the registry through the DID registrar and
signed by the issuer DID's keys. The registry (`CheqdAnonCredsRegistry`, `methodName` cheqd) handles identifiers matching
`did:cheqd:(testnet|mainnet):<id>[/path][?query][#fragment]`.

| Object | resourceType | Resource name | Returned id |
|---|---|---|---|
| Schema | `anonCredsSchema` | `<schemaName>-Schema` (version = schema version) | `<issuerDid>/resources/<uuid>` |
| Credential definition | `anonCredsCredDef` | hex SHA-256 of `<schemaName>-<tag>` | `<issuerDid>/resources/<uuid>` |
| Revocation registry definition | `anonCredsRevocRegDef` | hex SHA-256 of `<credDefName>-<rrdTag>` | `<issuerDid>/resources/<uuid>` |
| Revocation status list | `anonCredsStatusList` | same name as its registry definition | (no id; looked up by name, type and time) |

Resource ids are fresh random UUIDs at each registration; registering "the same" schema twice creates two schemas with two
ids. Registration is therefore a deployment step you run once per environment and whose ids you store (config or database),
not something to call per request.

## Register (all through `agent.modules.anoncreds`)
```ts
const issuerId = '<ISSUER_DID>'    // did:cheqd:<network>:<uuid>, created by THIS agent

const s = await agent.modules.anoncreds.registerSchema({
  schema: { issuerId, name: 'Degree', version: '1.0.0', attrNames: ['name', 'degree', 'date'] },
  options: {},
})
if (s.schemaState.state !== 'finished') throw new Error(s.schemaState.reason)
const schemaId = s.schemaState.schemaId

const c = await agent.modules.anoncreds.registerCredentialDefinition({
  credentialDefinition: { issuerId, schemaId, tag: 'default' },
  options: { supportRevocation: true },        // false if no revocation
})
if (c.credentialDefinitionState.state !== 'finished') throw new Error(c.credentialDefinitionState.reason)
const credentialDefinitionId = c.credentialDefinitionState.credentialDefinitionId
```
- `issuerId` must be a DID this agent created or imported with keys, on a network configured in `CheqdModule`; the registrar
  signs the resource with the DID's mapped keys and looks up the created-role `DidRecord`. Otherwise `state: 'failed'`
  with reason `DID: ... not found` or `unknownError: ...`.
- The credential definition step first resolves the schema through the registry service, so the schema must be resolvable
  from the same network.
- The credential definition's private key material and key-correctness proof are stored in the agent's store. Back up
  the store and its key: without them you cannot issue under that credential definition again.

## Revocation
Needs `supportRevocation: true` on the credential definition and a tails file service that can upload.
```ts
const r = await agent.modules.anoncreds.registerRevocationRegistryDefinition({
  revocationRegistryDefinition: { issuerId, tag: 'rev-1', credentialDefinitionId, maximumCredentialNumber: 1000 },
  options: {},
})
const revocationRegistryDefinitionId = r.revocationRegistryDefinitionState.revocationRegistryDefinitionId

const sl = await agent.modules.anoncreds.registerRevocationStatusList({
  revocationStatusList: { issuerId, revocationRegistryDefinitionId },
  options: {},
})

// later: flip bits, writes a new status list resource each time
await agent.modules.anoncreds.updateRevocationStatusList({
  revocationStatusList: { revocationRegistryDefinitionId, revokedCredentialIndexes: [3], issuedCredentialIndexes: [] },
  options: {},
})
```
- Each registry definition holds `maximumCredentialNumber` credentials; plan a new registry (new tag) when one fills.
- Status lists are versions of one named resource; a verifier asks for the one in force at a timestamp, resolved as
  the resource of that name and type created closest at or before the timestamp. The registry reports the timestamp of a new list as "now"
  because the chain response does not return it.
- Every update is a paid resource write (see costs in `cheqd-module-setup`). Batch revocations into one update rather than one
  write per revoked credential, and serialise updates for a registry (each update reads the latest list first).
- Source files do not show how an Issue Credential v2 offer binds a credential to a revocation registry or how revoking a
  specific issued credential maps to an index; that lives in the DIDComm AnonCreds format service and was not read.
  Treat the end-to-end revocation flow as unconfirmed here and test it on testnet before promising revocation.

### Tails file service
The default `BasicTailsFileService` only downloads: its `uploadTailsFile` throws "BasicTailsFileService only supports tails
file downloading", so `registerRevocationRegistryDefinition` fails without your own `TailsFileService` in
`AnonCredsModule({ tailsFileService })`.
```ts
interface TailsFileService {
  getTailsBasePath(agentContext): string | Promise<string>
  uploadTailsFile(agentContext, { revocationRegistryDefinition, revocationRegistryDefinitionId? }): Promise<{ tailsFileUrl: string }>
  getTailsFile(agentContext, { revocationRegistryDefinition, revocationRegistryDefinitionId? }): Promise<{ tailsFilePath: string }>
}
```
- `registerRevocationRegistryDefinition` creates the tails file locally under `getTailsBasePath`, calls `uploadTailsFile`,
  then replaces the definition's `tailsLocation` with the returned `tailsFileUrl` before writing to cheqd. Extending
  `BasicTailsFileService` and overriding only `uploadTailsFile` keeps its hash-verified download in `getTailsFile`.
- Holders and verifiers download the file from that URL and the download is checked against the SHA-256 `tailsHash`, so the
  URL must be public, stable and reachable from phones and verifier servers. cheqd stores only the URL, not the file; the
  cheqd Credo docs say a tails server (they link bcgov/indy-tails-server) must be configured when revocation is on.
  Storage, upload protocol and hosting are your choice and not covered by the sources read.

## Backend shape for a web app
- Run registration as a CLI or startup migration script against the same agent configuration, not as a public endpoint.
- Expose only business endpoints (start issuance, check status, revoke); load `schemaId`, `credentialDefinitionId`,
  revocation ids from config.
- Resolution results are cached by the registry (`allowsCaching`), and the registry keeps local records of what you
  created, so the issuer's own reads are fast; status-list updates request the latest list with caching off.

## Failure modes
- `No registry found for issuerId`: the `issuerId` is not a `did:cheqd:testnet|mainnet` DID, or `CheqdAnonCredsRegistry` is
  missing from `registries`.
- `BasicTailsFileService only supports tails file downloading`: revocation without an uploading tails service.
- Credential definition fails with a schema-not-found reason: schema registered on another network or not yet readable.
- Registering with a DID imported without a key mapping: the registrar falls back to the legacy key id (base58 public key), which
  matches nothing in a 0.6+ KMS, so map keys explicitly on import.
- Schema or credential definition lost after a store wipe: the on-chain objects remain, but you cannot issue again; register
  a new credential definition (new id).

## Verify
- [ ] `agent.modules.anoncreds.getSchema(schemaId)` and `getCredentialDefinition(credentialDefinitionId)` return the objects
  on a second agent configured with only `networks: [{ network }]`.
- [ ] `getRevocationRegistryDefinition(id)` shows a `tailsLocation` that downloads and whose SHA-256 matches `tailsHash`.
- [ ] After `updateRevocationStatusList`, `getRevocationStatusList(revocationRegistryDefinitionId, <unix seconds now>)` shows
  the revoked index.

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Resource names, types, ids, metadata, "state/reason" shapes, status-list timestamp behaviour, cred-def name dependency: packages/cheqd/src/anoncreds/services/CheqdAnonCredsRegistry.ts. Resource type strings and identifier regex: anoncreds/utils/identifiers.ts.
- `registerSchema`, `registerCredentialDefinition` (`supportRevocation`), `registerRevocationRegistryDefinition` (`maximumCredentialNumber`, tails flow), `registerRevocationStatusList`, `updateRevocationStatusList` argument shapes and the `useCache: false` read: packages/anoncreds/src/AnonCredsApi.ts.
- Tails interface and the Basic service behaviour (download-only, hash-verified, error text): packages/anoncreds/src/services/tails/*.ts; `tailsFileService` option: AnonCredsModuleConfig.ts.
- cheqd docs (fetched 2026-10-28, llms-full.txt and advanced/anoncreds.md): schemas, credential definitions and status lists stored as DID-Linked Resources; tails server must be configured for revocation. Those pages show the 0.5 API (`credentialDefinition.value` omitted, `supportRevocation`, `revocation_registry_size`); the call shapes above are from 0.7.3 source.
- Not confirmed: DIDComm offer binding to a revocation registry and the revoke-credential call; any cheqd-provided tails hosting; read-after-write delay on the network. The legacy-key-id fallback is from `signPayload` in dids/CheqdDidRegistrar.ts; its consequence in a 0.6+ KMS follows the 0.5-to-0.6 guide cited in `dids-and-key-management`.

Method: documentation only; no commands were run.
