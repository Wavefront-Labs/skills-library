---
id: computing-software.software-engineering.credo.upgrading-between-versions
name: upgrading-between-versions
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, aries-framework-javascript, upgrade, migration, update-assistant, storage-migration, breaking-changes, semver, credo-0-6, credo-0-7, askar, tenants, drizzle, native-bindings]
level: advanced
status: docs-checked
description: "Upgrade a Credo agent across minor versions (0.5 to 0.6 to 0.7): breaking code changes, storage version checks, UpdateAssistant API, tenants, backups now on you."
sources:
  - https://credo.js.org/guides/updating
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
  - https://credo.js.org/guides/updating/versions/0.6-to-0.7
  - https://credo.js.org/guides/updating/update-assistant
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/storage/migration/UpdateAssistant.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/storage/migration/updates.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/agent/Agent.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/tenants/src/TenantsApi.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Credo between versions

**Rule of thumb:** Credo is pre-1.0, so a change in the **second** number (0.6 to 0.7) is a breaking release and needs
the migration guide; a change in the third number (0.7.2 to 0.7.3) is meant to be safe. Breaking releases can change
code (APIs) and storage (record formats). Current release when this was written: **0.7.3**.

## 1. Plan
- Move one minor at a time (0.4 to 0.5 to 0.6 to 0.7), reading each guide on credo.js.org under Updating.
- Bump every `@credo-ts/*` package together, and the native bindings with them. For 0.7:
  `@openwallet-foundation/askar-*` `^0.6.0`, `@hyperledger/anoncreds-*` `^0.4.0`, `@hyperledger/indy-vdr-*`
  `^0.3.0`. Pin them with `resolutions`/`overrides`. Extension packages from third parties are not updated for you.
- **Back up first.** Credo 0.6 removed its automatic backup; export the Askar store (`agent.modules.askar.exportStore`,
  see `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`) or back up the Postgres
  database yourself. The update-assistant docs page still describes Credo-made backups and a
  `createBackupBeforeUpdate` option; neither exists in 0.7.3.

## 2. Code changes by release
**0.5 to 0.6 (large):**
- ESM-only; Node 18 dropped. DIDComm moved to `@credo-ts/didcomm` with `DidComm`-prefixed classes and events, APIs
  under `agent.didcomm.*`, transports registered on `DidCommModule` or `agent.didcomm`.
- `walletConfig` moved to `AskarModule({ store })`; `label`/`connectionImageUrl` removed from config (pass per
  invitation); Askar bindings renamed to `@openwallet-foundation/askar-*`.
- Wallet API replaced by `agent.kms`; `Key`/`Jwk` replaced by `PublicJwk`; signing DIDs need a `DidRecord` with key ids.
- `credentialRecordId`/`proofRecordId` became `credentialExchangeRecordId`/`proofExchangeRecordId`;
  `record.credential` became `record.firstCredential`; `storeCredential()` became `store({ record })`.
- did:peer:4 default for DID Exchange; BBS+ and linked attachments removed; Express 5.
- OpenID4VC: one `OpenId4VcModule`; SIOPv2 removed; OID4VP `responseMode` default `direct_post.jwt`.
- Deprecated (still shipped in 0.7.3): connection protocol v1, issue-credential v1, present-proof v1, legacy Indy formats.

**0.6 to 0.7 (small):**
- New native bindings without `ffi-napi`/`ref-napi`; Node.js 22 and 24 supported (20 unsupported).
- `Buffer` no longer exported from core; `TypedArrayEncoder.fromString` became `fromUtf8String`, `toBase64URL`/
  `fromBase64URL` became `toBase64Url`/`fromBase64Url`; `JsonEncoder.fromBuffer`/`toBuffer` became
  `fromUint8Array`/`toUint8Array`; `fromBase64` no longer accepts base64url.
- `LogLevel` keys are PascalCase (`LogLevel.Debug`); numeric values unchanged.
- Patch releases since 0.7.0 add deprecations rather than breaks, for example AnonCreds DIDComm imports moving to
  `@credo-ts/anoncreds/didcomm` (0.7.2) and SD-JWT `disclosedPayload` giving way to `disclosedPaths` (0.7.1).

## 3. Storage
- The storage version lives in the store. On `initialize()`, an outdated store aborts start-up with an error naming the
  current and required version, unless `autoUpdateStorageOnStartup: true` is set in the agent config.
- In 0.7.3 the framework storage version is still **0.5** (the last update script is 0.4 to 0.5). Stores already on
  0.5 need no storage migration for 0.6 or 0.7; stores on 0.4 or older do.
- Manual control (recommended when several instances share one database):
```ts
import { UpdateAssistant } from '@credo-ts/core'
const ua = new UpdateAssistant(agent, { v0_1ToV0_2: { mediationRoleUpdateStrategy: 'recipientIfEndpoint' } })
await ua.initialize()                       // throws if the agent is already initialised
if (!(await ua.isUpToDate())) await ua.update()   // optional { updateToVersion }
await agent.initialize()
```
  Also available: `getCurrentAgentStorageVersion()`, `getNeededUpdates()`, static `UpdateAssistant.frameworkStorageVersion`.
  If a store is older than the oldest script this release carries, `getNeededUpdates` throws and tells you to update
  with an older Credo first. The Indy SDK to Askar migration package was removed in 0.6, so migrate such wallets on
  0.5 first.
- Run updates from **one** instance only; several instances auto-updating the same database will race.
- **Tenants:** the assistant updates the root store. Tenant stores update on first open when auto-update is on, or
  explicitly with `agent.modules.tenants.getTenantsWithOutdatedStorage()` and `updateTenantStorage({ tenantId })`.
- Moving from Askar to Drizzle (SQL) storage is a separate, optional migration (`@credo-ts/askar-to-drizzle-storage-migration`).
  Drizzle storage adds SQL migrations even in non-breaking releases, so run its migrations on every deploy or pin the version.

## Failure modes
- Agent refuses to start after an upgrade: storage outdated and auto-update off. Run the assistant or roll back.
- Native crash or missing symbol after `npm install`: a transitive dependency pulled an older binding.
- Interop breaks with older agents after 0.6: they may not resolve did:peer:4; set
  `peerNumAlgoForDidExchangeRequests: PeerDidNumAlgo.GenesisDoc` in the connections config.

## Verify
- [ ] Type-check passes with no imports from `@credo-ts/core` that moved to `@credo-ts/didcomm`.
- [ ] `await new UpdateAssistant(agent).isUpToDate()` is `true` before go-live (on a copy of production data).
- [ ] Existing connections, credentials and proofs from before the upgrade still load and a new exchange completes.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3 (tag v0.7.3; npm `latest` 0.7.3); source read from branch `v0.7.x`.
- Versioning rule and code-versus-storage split: credo.js.org/guides/updating. 0.5-to-0.6 and 0.6-to-0.7 change lists and dependency versions: the two migration guides. Patch-level deprecations: packages/core and packages/didcomm CHANGELOG.md (0.7.1, 0.7.2).
- UpdateAssistant methods, `update({ updateToVersion })` only, too-old error, no backup code: packages/core/src/storage/migration/UpdateAssistant.ts. Storage versions and default update config: updates.ts. Start-up check and auto-update: packages/core/src/agent/Agent.ts; `autoUpdateStorageOnStartup` in src/types.ts.
- Tenant update methods: packages/tenants/src/TenantsApi.ts. Multi-instance caution: credo.js.org update-assistant page. Drizzle migration note: packages/drizzle-storage/README.md; migration package: packages/askar-to-drizzle-storage-migration/README.md.
- Stale docs noted: the update-assistant page's backup section predates 0.6.

Method: documentation only; no commands were run.
