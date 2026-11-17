---
id: computing-software.software-engineering.credo.askar-module-store-config
name: askar-module-store-config
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, askar, askar-module, askar-nodejs, askar-react-native, native-askar, openwallet-askar, hyperledger-askar, aries-askar, store-config, sqlite, postgres, key-derivation, argon2i, raw-key, generate-raw-key, wallet-storage, enable-kms, enable-storage, drizzle-storage, encrypted-storage, wallet-config]
level: practitioner
status: docs-checked
description: "Configure AskarModule in Credo 0.7: pass NativeAskar, set SQLite or Postgres store, choose raw or Argon2 key derivation, generate a raw store key, toggle KMS/storage, handle open errors."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarStorageConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarStoreManager.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/utils/askarStoreConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/CHANGELOG.md
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/drizzle-storage/README.md
  - https://github.com/openwallet-foundation/askar-wrapper-javascript/blob/main/README.md
  - https://github.com/openwallet-foundation/askar-wrapper-javascript/blob/main/packages/askar-shared/src/store/Store.ts
  - https://github.com/openwallet-foundation/askar-wrapper-javascript/blob/main/packages/askar-nodejs/scripts/install.js
  - https://github.com/openwallet-foundation/askar/blob/main/docs/storage.md
  - https://github.com/openwallet-foundation/askar/blob/main/askar-storage/src/protect/store_key.rs
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
  - https://credo.js.org/guides/updating/versions/0.6-to-0.7
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AskarModule and store configuration in Credo (0.7.x)

**Goal:** an agent whose records and keys live in an encrypted Askar store you configured on purpose (backend, key,
key derivation), and that fails with a recognisable error when the key or store is wrong. Written against
**Credo 0.7.3** (`@credo-ts/askar` 0.7.3). Askar is the Rust secure storage and key manager from OpenWallet
Foundation (formerly Hyperledger Aries Askar); Credo ships the `@credo-ts/askar` glue and you add a native binding.

## What changed since the tutorials you will find
- The docs page "Aries Askar" still shows `@credo-ts/askar@^0.5.3` and `@hyperledger/aries-askar-*`. It is 0.5-era.
- 0.6 removed `walletConfig` from the agent config. The wallet id and key now live in `AskarModule({ store })`.
- 0.6 replaced `agent.wallet` with `agent.kms` (see `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`).
- The native packages moved scope: `@hyperledger/aries-askar-nodejs` became `@openwallet-foundation/askar-nodejs`, and the
  module option went `ariesAskar` then `askar` then (0.7.2 and later) `NativeAskar`.
- 0.6 removed Credo's automatic backup. You back up the store yourself.

## Passing the native library
```ts
import { AskarModule } from '@credo-ts/askar'
import { NativeAskar } from '@openwallet-foundation/askar-nodejs'            // Node.js
// import { NativeAskar } from '@openwallet-foundation/askar-react-native'   // React Native

new AskarModule({
  askar: NativeAskar,
  store: { id: '<STORE_ID>', key: '<STORE_KEY_FROM_SECRET_STORE>' },
})
```
- `askar` accepts either the `NativeAskar` class or an `Askar` instance (the deprecated `askar` export). `NativeAskar`
  resolves the registered binding lazily, so import order cannot leave it `undefined`; the config comments recommend it.
- Importing the platform package registers its binding with `@openwallet-foundation/askar-shared` and re-exports the
  shared classes (`Store`, `Key`, `KdfMethod` and so on). Install `askar-shared` as a peer of `@credo-ts/askar`.
- Version pairing: 0.7.0 moved to Askar bindings `^0.6.0` (koffi instead of ffi-napi); the 0.7.2 changelog says
  askar-shared `^0.4.3 || ^0.5.0 || ^0.6.0` stays supported. Wrapper 0.6.0 pairs with Askar library v0.5.0, Node.js
  20, 22, 24 and React Native 0.75 to 0.81 (wrapper README table). The wrapper's `main` branch, read for this skill
  (package version 0.6.1), lists `react-native >= 0.77` as a peer, so check the peer range of the version you install.
- Install-time download: both wrapper packages run `scripts/install.js` on install, which fetches a prebuilt Askar
  library tarball from the Askar GitHub releases (Node: `library-<platform>-<arch>`, platforms linux, darwin
  universal, windows; arch x86_64 or aarch64; React Native: `library-ios-android`). An install with scripts disabled or
  no access to github.com therefore has no native library. This is read from the script, not from a failed install.

## Options
| Option | Meaning | Default |
|---|---|---|
| `store.id` | Store name, and the default profile of the root agent. SQLite: part of the file path. Postgres: the database name | required |
| `store.key` | Passphrase or raw key that opens the store | required |
| `store.keyDerivationMethod` | `kdf:argon2i:mod`, `kdf:argon2i:int` or `raw` | `kdf:argon2i:mod` |
| `store.database` | `{ type: 'sqlite', config? }` or `{ type: 'postgres', config, credentials }` | SQLite |
| `multiWalletDatabaseScheme` | `DatabasePerWallet` or `ProfilePerWallet` (tenants only, see the backup skill) | `DatabasePerWallet` |
| `enableKms` | Register `AskarKeyManagementService` (backend name `askar`) | `true` |
| `enableStorage` | Register `AskarStorageService` as the `StorageService` | `true` |

### SQLite
```ts
store: { id: 'wallet', key, database: { type: 'sqlite', config: { path: '<DB_DIR>', maxConnections: 5 } } }
```
- No `path`: the file is `<dataPath>/wallet/<store.id>/sqlite.db`, where `dataPath` comes from the file system
  dependency (`@credo-ts/node` or `@credo-ts/react-native`). `inMemory: true` gives `sqlite://:memory:` (tests).
  Credo creates the directory for a file-backed store and refuses to provision over an existing path.
- `minConnections` and `maxConnections` are passed to Askar as URL parameters.

### Postgres
```ts
store: {
  id: '<DATABASE_NAME>', key,
  database: {
    type: 'postgres',
    config: { host: '<HOST>:5432', connectTimeout: 10, maxConnections: 20,
              connectionParameters: { sslmode: 'verify-full', sslrootcert: '<CA_PATH>' } },
    credentials: { account: '<DB_USER>', password: '<DB_PASSWORD>' },   // adminAccount/adminPassword optional
  },
}
```
- Account and password are URL-encoded into `postgres://account:password@host/<store.id>`; load both from a secret
  manager, never from source.
- `connectionParameters` (added in 0.7.1) are appended to the connection URL and passed to sqlx, so SSL needs no
  environment variables. Parameters Credo derives itself are rejected with an `AskarError`: `connect_timeout`,
  `idle_timeout`, `max_connections`, `min_connections`, `admin_account`, `admin_password`, `host`, `port`, `user`,
  `password`, `dbname`.
- `adminAccount` and `adminPassword` become `admin_account` and `admin_password` URL parameters; what Askar does with
  them was not confirmed here.
- Askar's storage doc suggests pgBouncer or a managed proxy when many replicas each hold their own pool.

## Store key and key derivation
- `kdf:argon2i:mod` (default, strongest) and `kdf:argon2i:int` (faster) derive the real key from a passphrase with a
  random salt; Askar records `kdf:argon2i:13:mod?salt=<hex>` as store metadata. Use for human passphrases or PINs.
- `raw` skips derivation: `key` must already be a random 32-byte key encoded as base58 (Askar rejects a wrong length or
  non-base58 text). The raw key itself is not stored in the database. The config comment says `raw` suits a key held in
  an on-device keychain backed by biometrics.
- Generate a raw key with the Askar wrapper, once, and put it straight into your secret store:
  ```ts
  import { Store } from '@openwallet-foundation/askar-nodejs'   // or ...-react-native
  const rawKey: string = Store.generateRawKey()                  // optional seed: Store.generateRawKey(seedBytes)
  ```
  A seed makes the key deterministic, so never use a guessable seed. Credo itself calls the binding's
  `storeGenerateRawKey({})` to make per-tenant keys.
- Changing key or method later is `rotateStoreKey` (backup skill). Keep `keyDerivationMethod` equal to how the store was
  provisioned; what Askar does on a mismatch was not confirmed (wrong-key error below).

## Lifecycle you get for free
- `agent.initialize()` opens the root store; if it does not exist yet and the context is initialised, Credo provisions
  it and writes the framework storage version record. So the first start creates the store.
- The API is `agent.modules.askar` (`isStoreOpen`, `provisionStore`, `openStore`, `closeStore`, `deleteStore`,
  `exportStore`, `importStore`, `rotateStoreKey`). `openStore` on an already open store throws; close first.
- `agent.shutdown()` closes the store; call it on SIGTERM.

## Turning parts of Askar off
- `enableKms: false` when you register `new AskarKeyManagementService()` yourself on a `Kms.KeyManagementModule`;
  otherwise Credo throws because a backend named `askar` already exists.
- `enableStorage: false` when another `StorageService` is registered; otherwise Credo throws "There is an instance of
  StorageService already registered". With both flags off Credo logs a warning that Askar is not used.
- 0.7.x also ships `@credo-ts/drizzle-storage` (PostgreSQL or SQLite via Drizzle ORM, record bundles, SQL migrations you
  must run before initialising; README calls the bundle API experimental). It replaces record storage only. The Askar
  key service reads keys from the Askar store, so keeping `enableKms` on still needs a configured `store`. The README
  advises Askar storage if you cannot run migrations on every deploy because Askar defines no schema.

## Errors on open and provision
All are exported from `@credo-ts/askar`.
| Error | When |
|---|---|
| `AskarStoreNotFoundError` | `openStore` found no store (also for a missing in-memory store) |
| `AskarStoreInvalidKeyError` | open failed with Askar's encryption error: message "Incorrect key for store '<id>'" |
| `AskarStoreDuplicateError` | `provisionStore` on an existing store; an Askar encryption error during provision is also mapped here, so provisioning an existing store with a wrong key reports Duplicate, not InvalidKey |
| `AskarStoreError` | any other failure; the original error is `cause` |
The store has no "locked" state: it is either open on the context or not. `openStore` while open throws
"Store already opened"; `closeStore` with none open throws "There is no open store."

## Failure modes
- Hard-coded or lost store key: the wallet is unrecoverable; keep the key out of source and back it up apart from the
  data.
- `Missing required dependency: 'StorageService'`: `enableStorage: false` with no other storage module.
- Two agents sharing one SQLite file or one store id on Postgres without meaning to.
- Mixed 0.6 and 0.7 packages or an old binding: install the versions in the 0.6-to-0.7 guide and pin them.

## Verify
- [ ] First start creates the store (SQLite file at the expected path, or the Postgres database) and logs no error.
- [ ] Restart with the same `store` config reopens it and earlier records are still there.
- [ ] A deliberately wrong `key` in a scratch copy throws `AskarStoreInvalidKeyError` (catch it by class).
- [ ] The key comes from a secret store and the repository contains no key literal.

## See also
- `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`: keys, rotation, export/import, tenants.
- `computing-software.software-engineering.credo.agent-setup-nodejs` and `computing-software.software-engineering.credo.react-native-mobile-agent`: whole-agent wiring.
- `computing-software.software-engineering.credo.upgrading-between-versions`: storage version updates.

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x` (@credo-ts/askar 0.7.3).
- Option names, defaults, comments (`NativeAskar`, `keyDerivationMethod`, `enableKms`, `enableStorage`, scheme default): packages/askar/src/AskarModuleConfig.ts. Registration guards, warning, onInitialize/onDelete hooks: AskarModule.ts. Storage config shapes: AskarStorageConfig.ts. URI building, default SQLite path, reserved Postgres parameters: utils/askarStoreConfig.ts. Open/provision/close behaviour and error mapping, auto-provision, `agent.modules.askar` API: AskarStoreManager.ts, AskarApi.ts, tests/askar-store-api.test.ts. Exported error classes: src/index.ts.
- 0.7.0 koffi, 0.7.1 `connectionParameters`, 0.7.2 `NativeAskar` and askar-shared range: packages/askar/CHANGELOG.md. Binding versions and removed backup, `walletConfig`, `agent.wallet`: credo.js.org 0.5-to-0.6 and 0.6-to-0.7 guides. "Aries Askar" docs page is 0.5-era: credo.js.org/guides/getting-started/set-up/aries-askar.
- `Store.generateRawKey(seed?)`: askar-wrapper-javascript packages/askar-shared/src/store/Store.ts. Raw key base58 and length check, `raw` not stored, `kdf:argon2i:13:mod?salt=` metadata, argon2i levels: askar storage.md, store_key.rs and protect/kdf. Install-time download: askar-nodejs and askar-react-native `scripts/install.js`, package.json `binary`. Compatibility table: wrapper README (React Native peer on main from askar-react-native/package.json).
- Drizzle: packages/drizzle-storage/README.md.
- Not confirmed, so not stated: what `adminAccount` does in Askar, behaviour when `keyDerivationMethod` differs from how the store was provisioned, Drizzle storage combined with Askar KMS in a documented or tested setup, Postgres version requirements.

Method: documentation only; no commands were run.
