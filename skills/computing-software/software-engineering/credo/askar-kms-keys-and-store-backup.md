---
id: computing-software.software-engineering.credo.askar-kms-keys-and-store-backup
name: askar-kms-keys-and-store-backup
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, askar, askar-kms, agent-kms, key-management, kms, create-key, import-key, delete-key, key-types, ed25519, p-256, secp256k1, x25519, rotate-store-key, rekey, export-store, import-store, wallet-backup, tenants, tenants-module, profile-per-wallet, database-per-wallet, mobile-keychain, secure-storage, askar-profile]
level: practitioner
status: docs-checked
description: "Manage keys through Credo 0.7 agent.kms on the Askar backend (types, import, delete, legacy ids), rotate the store key, export/import backups, and run tenants as profiles or stores."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/kms/AskarKeyManagementService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarApiOptions.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarStoreManager.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/tenants.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/utils/transformPrivateKey.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/tests/askar-store-api.test.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/kms/KeyManagementApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/kms/KeyManagementModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/kms/options/KmsCreateKeyOptions.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/modules/kms/legacy.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/tenants/src/TenantsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/tenants/src/TenantsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/CHANGELOG.md
  - https://github.com/openwallet-foundation/askar/blob/main/docs/storage.md
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Askar keys, store key rotation, backup and tenants in Credo (0.7.x)

**Goal:** create and import keys that never leave the Askar store, rotate the store key, take and restore a backup, and
run many wallets (tenants) with the right isolation. Written against **Credo 0.7.3**. Store set-up and error names:
`computing-software.software-engineering.credo.askar-module-store-config`.

## Which API is current
- **`agent.kms` is current** (class `KeyManagementApi`). `agent.wallet`, `KeyType` and `walletConfig` were removed in 0.6
  (0.5-to-0.6 guide). In 0.7.3 there is no wallet API to migrate to; any tutorial using `agent.wallet.createKey` is stale.
- Askar is one *backend* of the KMS, named `askar` (`AskarKeyManagementService.backend`), registered by
  `AskarModule` unless `enableKms: false`. Further backends (for example the secure-environment one on mobile, see
  `computing-software.software-engineering.credo.react-native-mobile-agent`) sit beside it.
- Keys are identified by a `keyId` you choose or a generated UUID, not by the public key. Pre-0.6 keys used the base58
  public key as their id (`legacyKeyIdFromPublicJwk`, and `publicJwk.legacyKeyId` in the migration guide).
- API methods: `createKey`, `createKeyForSignatureAlgorithm`, `importKey`, `getPublicKey`, `deleteKey`, `sign`, `verify`,
  `encrypt`, `decrypt`, `randomBytes`, `supportedBackendsForOperation`. There is **no export-private-key method**:
  private keys leave Askar only inside a store export.

## Create, import, delete
```ts
const { keyId, publicJwk } = await agent.kms.createKey({ type: { kty: 'OKP', crv: 'Ed25519' }, keyId: '<OPTIONAL_ID>' })
const pub = await agent.kms.getPublicKey({ keyId })                 // throws KeyManagementKeyNotFoundError if absent
const { keyId: copy } = await agent.kms.importKey({ privateJwk })   // kid in the JWK is used, else a UUID
const deleted: boolean = await agent.kms.deleteKey({ keyId })       // false when the key does not exist
// pin the backend explicitly:
await agent.kms.createKey({ backend: 'askar', type: { kty: 'EC', crv: 'P-256' } })
```
- Without `backend`, Credo uses the configured `defaultBackend` (else the first registered backend) when it supports the
  operation, and falls back to another backend that does, logging a warning. `new Kms.KeyManagementModule({ backends,
  defaultBackend })` sets it; an unknown `defaultBackend` id throws.
- Existing id: `Kms.KeyManagementKeyExistsError`. Unsupported type or algorithm:
  `Kms.KeyManagementAlgorithmNotSupportedError`; everything else wraps in `Kms.KeyManagementError` with a `cause`.
- Bring old raw material in with `transformPrivateKeyToPrivateJwk({ type, privateKey })` or
  `transformSeedToPrivateJwk({ type, seed })` (both from `@credo-ts/askar`, `EC` and `OKP` only), then `importKey`.
  Seeds and private keys are secrets: read them from a secret store, never log them.
- Deleting a key does not touch `DidRecord` key mappings; see
  `computing-software.software-engineering.credo.dids-and-key-management`.

## Key types on the Askar backend
| Operation | Supported |
|---|---|
| `createKey` | `EC` with `secp256k1`, `P-256`, `P-384`; `OKP` with `Ed25519`, `X25519`; `oct` with `algorithm: 'aes'` and `length` 128 or 256, and `oct` `C20P` |
| `importKey` | `EC` and `OKP` with those curves only (no `oct`, no RSA) |
| `sign` | `EdDSA`, `Ed25519`, `ES256K`, `ES256`, `ES384` |
| `verify` | the same, plus `ES512` (P-521, added in 0.7.3 using `@noble/curves`) |
| `encrypt` / `decrypt` | AES-GCM and AES-CBC-HMAC, `C20P`, `XC20P`, AES key wrap, `XSALSA20-POLY1305`, plus HPKE key agreement `HPKE-0`, `HPKE-3`, `HPKE-7` (0.7.1) |
Not on Askar: RSA, P-521 key creation, `hmac` keys. The core options type allows more (RSA, `hmac`, AES 192/512); the
Askar backend reports them unsupported, and the API then picks another backend if one supports them, or throws.
Use `agent.kms.supportedBackendsForOperation({ operation: 'createKey', type })` to ask.
Source quirk: `createKey` code maps AES length 512, but `isOperationSupported` only accepts 128 and 256, so a 512 request
is refused at the API.

## Where keys live
Keys and records are rows in the same encrypted Askar store (item kind KMS versus item, per Askar's storage doc), each
profile encrypted under its own profile key, which is encrypted under the store key. Consequences: one backup covers
both; the store key protects every private key; losing the store key loses the keys.

## Rotate the store key
```ts
await agent.modules.askar.rotateStoreKey({ newKey: '<NEW_KEY>', newKeyDerivationMethod: 'raw' })  // method optional
// then change AskarModule({ store: { key: '<NEW_KEY>', keyDerivationMethod: 'raw' } }) in your config/secret store
```
- The store must be open (`initialize()` first). Askar re-encrypts the profile keys under the new key and updates the
  store key metadata, so the data itself is not rewritten. `newKeyDerivationMethod` defaults to the current one.
- Rotation changes the on-disk key immediately; if the process restarts with the old key in config it fails with
  `AskarStoreInvalidKeyError`. Update the secret before the restart and take a backup first (below).
- It rekeys the whole store, every tenant profile included. With `ProfilePerWallet` run it on the root agent only.
- A rotation error surfaces as `AskarStoreError` "Error rotating key for store '<id>': ..." with the cause attached.

## Backup and restore (export and import)
```ts
// backup: store open
await agent.modules.askar.exportStore({
  exportToStore: { id: '<BACKUP_ID>', key: '<BACKUP_KEY>',
                   database: { type: 'sqlite', config: { path: '<BACKUP_PATH>' } } },
})
// restore: store closed, destination config is the AskarModule store config
await agent.modules.askar.closeStore()          // or deleteStore() when replacing a lost/damaged store
await agent.modules.askar.importStore({
  importFromStore: { id: '<BACKUP_ID>', key: '<BACKUP_KEY>', database: { type: 'sqlite', config: { path: '<BACKUP_PATH>' } } },
})
await agent.modules.askar.openStore()
```
- The export is a copy into a new Askar store with **its own key** (and optional `keyDerivationMethod`), so the backup
  key can differ from the live key; store the backup key separately from the backup.
- Export needs an open store; import needs a **closed** one ("To import a store the current store needs to be closed
  first"). Import opens the source with the given key and copies it to the *current configured* store location and key.
- Path-based (SQLite) destinations must not exist: `AskarStoreExportPathExistsError` ("Unable to create export...") or
  `AskarStoreImportPathExistsError` ("Unable to import store..."). A failed import deletes the destination path it
  created. `AskarStoreExportUnsupportedError` is also exported; when it is thrown was not read.
- A store holds all tenant profiles, so an export contains every tenant.
- Credo no longer makes automatic pre-update backups (0.6): export first, or snapshot the Postgres database.
- Restore test from the repository: export, `deleteStore()`, provision fresh (empty), delete, `importStore`, `openStore`,
  and the earlier record is back.
- `deleteStore()` closes and removes the whole store, all tenants in it included, and cannot be undone.

## Multi-tenancy with the Tenants module
`@credo-ts/tenants` `TenantsModule({ sessionLimit?: 100, sessionAcquireTimeout?: 1000 })`; the API is
`agent.modules.tenants` (`createTenant({ config: { label } })`, `withTenantAgent({ tenantId }, cb)`, `getTenantAgent`,
`deleteTenantById`, `getAllTenants`).
| `multiWalletDatabaseScheme` | Storage per tenant | Tenant key |
|---|---|---|
| `DatabasePerWallet` (default, for backward compatibility) | its own store (`id` is the tenant context id; same `database` backend as the root, so one SQLite file or Postgres database each) | random raw key generated on provisioning, always opened with `raw`, kept in the tenant record metadata (`_askar/storeConfig`) in the root store |
| `ProfilePerWallet` (recommended by the config comment for performance) | a profile in the root store named by the tenant context id, created on provisioning | none of its own: the root store key protects it |
- With database-per-wallet, the root store is the vault of every tenant key: losing or leaking the root store or its key
  affects all tenants. Back up the root store and every tenant store together.
- Deleting a tenant deletes its store (database-per-wallet) or removes its profile (profile-per-wallet); the tenant
  record and routing records go too.
- Tenant keys are isolated at the profile or store level: `AskarKeyManagementService` runs each operation in the calling
  context's profile.
- `ProfilePerWallet`: store-level operations (provision, open, rotate, export, import, close, delete) throw an
  `AskarError` ("not on store level") when called from a tenant agent; run them on the root agent. Under
  `DatabasePerWallet` each tenant context is store-level.
- Tenant records created in 0.5 with `walletConfig.key` are read through a compatibility path and migrated into the
  metadata on first access. Changing the scheme of a deployment that already has tenants is not documented in what was
  read; treat it as a data migration you must test.
- `sessionLimit` (default 100 concurrent tenant sessions) and `sessionAcquireTimeout` (1000 ms) can make busy services
  throw while waiting for a session; size them to your hardware.

## Secrets on mobile
- Askar encrypts at rest, but its key must live somewhere. The config comment for `keyDerivationMethod: 'raw'` names a
  key held in an on-device keychain backed by biometrics. Flow: generate a raw key once with `Store.generateRawKey()`,
  save it in the platform keychain or keystore, read it (asynchronously) before building `AskarModule`, and pass it as
  `store.key` with `keyDerivationMethod: 'raw'`. With a user PIN as the key keep the default Argon2 method.
- Neither Credo nor Askar docs fetched name a keychain library; the choice and its access-control flags (biometrics, device-only) are yours.
- For keys that must never leave the device's secure hardware, the optional secure-environment KMS backend (P-256, ES256
  only) is the Credo-provided route; Askar-held keys are exportable inside the store backup.
- React Native binding: `@openwallet-foundation/askar-react-native` (see `computing-software.software-engineering.credo.react-native-mobile-agent`);
  the 0.6.0 changelog notes Askar 0.4.0 enabled 16KB page size support on Android.

## Failure modes
- `KeyManagementKeyNotFoundError` on a key you created: it lives in another backend, or the backend you hit does not
  support the operation (the message says which); or the store opened is a different one (wrong `store.id` or tenant).
- Key fails after restore from backup: the import went to a different `store.id`/path than the agent now opens.
- Rotating the key and forgetting to update the configured key: next start throws `AskarStoreInvalidKeyError`.
- Expecting to read a private key back: the KMS has no such call; keep the original secret in your own vault or use a
  store export.
- Running store operations on a tenant agent in `ProfilePerWallet`.

## Verify
- [ ] `createKey` then `getPublicKey({ keyId })` returns the same JWK; `sign` then `verify` round-trips with `ES256` or `EdDSA`.
- [ ] After `deleteKey`, `getPublicKey` throws and a second `deleteKey` returns `false`.
- [ ] Rotate on a scratch store, restart with the new key (opens) and with the old key (`AskarStoreInvalidKeyError`).
- [ ] Export, delete, import, open on a scratch store: records and keys are back.
- [ ] For tenants: a key created in tenant A is not found from tenant B.

## See also
- `computing-software.software-engineering.credo.askar-module-store-config`: options, SQLite/Postgres, key derivation, errors.
- `computing-software.software-engineering.credo.dids-and-key-management`: DIDs and `DidRecord` key mappings.
- `computing-software.software-engineering.credo.upgrading-between-versions`: take an export before storage updates.

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- KMS API method list, backend routing, default and fallback rules, error classes: packages/core/src/modules/kms/KeyManagementApi.ts, KeyManagementModuleConfig.ts. Create-key type shapes: kms/options/KmsCreateKeyOptions.ts. Legacy base58 key id: kms/legacy.ts.
- Askar backend operations, supported curves and algorithms, import limits, delete return value, existing-key errors, ES512 verify, HPKE: packages/askar/src/kms/AskarKeyManagementService.ts; curve and encryption tables: utils/askarKeyTypes.ts; seed/private-key transforms: utils/transformPrivateKey.ts. 0.7.1 HPKE, 0.7.3 P-521 verify, 0.6.0 Android 16KB pages: packages/askar/CHANGELOG.md.
- `rotateStoreKey`, export, import, delete, close, path-exists errors, store-level guard, tenant store config and profile handling: AskarApi.ts, AskarApiOptions.ts, AskarStoreManager.ts, AskarModule.ts, tenants.ts; usage and restore flow: tests/askar-store-api.test.ts. Tenants API and config defaults: packages/tenants/src/TenantsApi.ts, TenantsModuleConfig.ts, models/TenantConfig.ts, services/TenantRecordService.ts. Rekey re-encrypts profile keys, item kinds, profiles: askar docs/storage.md. Removed `agent.wallet`, removed backup: credo.js.org 0.5-to-0.6 guide.
- Not confirmed, so not stated as fact: when `AskarStoreExportUnsupportedError` is thrown; switching the multi-wallet scheme on live data; any Credo or Askar recommendation of a specific mobile keychain library; whether a tenant agent object exposes `kms` directly (examples avoid it); behaviour of `rotateStoreKey` interrupted midway.

Method: documentation only; no commands were run.
