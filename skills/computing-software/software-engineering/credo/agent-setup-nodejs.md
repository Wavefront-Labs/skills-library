---
id: computing-software.software-engineering.credo.agent-setup-nodejs
name: agent-setup-nodejs
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, aries-framework-javascript, afj, decentralized-identity, ssi, nodejs, agent-setup, askar, didcomm, didcomm-transports, esm, typescript, openwallet-foundation]
level: practitioner
status: docs-checked
description: "Set up a Credo 0.7 agent on Node.js: packages, Agent constructor, AskarModule store config, DidCommModule with HTTP/WS transports, initialize and shutdown."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/samples/mediator.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/BaseAgent.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/core/src/agent/Agent.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/DidCommModuleConfig.ts
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
  - https://credo.js.org/guides/updating/versions/0.6-to-0.7
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credo agent setup on Node.js (0.7.x)

**Goal:** a running Credo agent process with encrypted storage, a key management backend and (optionally) DIDComm
transports. Written against **Credo 0.7.3**. Credo was called Aries Framework JavaScript (AFJ) until 0.5; old
tutorials using `@aries-framework/*` or `walletConfig` describe an API that no longer exists.

## What changed that trips people up
- **ESM only** since 0.6. Use `"type": "module"`, `node16`/`nodenext` module resolution, `.js` suffixes on relative
  imports. Supported Node.js for 0.7 is 22 and 24 (20 may run but is unsupported).
- **No `walletConfig`, `label` or `endpoints` in the agent config.** Storage settings live on `AskarModule({ store })`;
  endpoints and transports live on `DidCommModule`; a label is passed per invitation.
- **DIDComm is a separate package** (`@credo-ts/didcomm`). Its APIs hang off `agent.didcomm.*`.
- The agent constructor throws `Missing required dependency: 'StorageService'` unless a storage module (Askar, Drizzle
  or your own) is registered.
- The docs site's set-up tutorials and snippets still show the 0.5 API; trust the migration guides and the repository
  `demo/` and `samples/` code for 0.7.

## Packages
`@credo-ts/core`, `@credo-ts/node`, `@credo-ts/askar` plus the native binding `@openwallet-foundation/askar-nodejs`
(0.7 expects `^0.6.0`). Add `@credo-ts/didcomm` only if you use DIDComm. The 0.7 bindings no longer use
`ffi-napi`/`ref-napi`, so no C toolchain is needed to install them. Keep every `@credo-ts/*` package on the same
version, and pin the native binding versions with `resolutions`/`overrides` so a transitive dependency cannot pull in an
older binary.

## Minimal agent (illustrative, 0.7.3)
```ts
import { Agent } from '@credo-ts/core'
import { AskarModule } from '@credo-ts/askar'
import { DidCommModule, DidCommHttpOutboundTransport, DidCommWsOutboundTransport } from '@credo-ts/didcomm'
import { agentDependencies, DidCommHttpInboundTransport } from '@credo-ts/node'
import { NativeAskar } from '@openwallet-foundation/askar-nodejs'

const agent = new Agent({
  config: {},                                   // logger, autoUpdateStorageOnStartup, allowInsecureHttpUrls, ...
  dependencies: agentDependencies,
  modules: {
    askar: new AskarModule({
      askar: NativeAskar,
      store: { id: '<STORE_ID>', key: '<STORE_KEY_FROM_SECRET_MANAGER>' },
    }),
    didcomm: new DidCommModule({
      endpoints: ['https://agent.example.com'],
      transports: {
        inbound: [new DidCommHttpInboundTransport({ port: 3000 })],
        outbound: [new DidCommHttpOutboundTransport(), new DidCommWsOutboundTransport()],
      },
      connections: { autoAcceptConnections: true },
    }),
  },
})

await agent.initialize()
// ... use agent.didcomm.*, agent.dids, agent.kms, agent.modules.<custom>
await agent.shutdown()
```

## Key settings
- **Askar store:** `id` names the store (and the SQLite file path or Postgres database); `key` opens it.
  `keyDerivationMethod` is `kdf:argon2i:mod` by default, `kdf:argon2i:int` (faster) or `raw` (only when the key is
  already strong, e.g. from a keychain). `database` selects SQLite (default) or Postgres. Pass `NativeAskar`, not the
  deprecated `askar` export, which can be `undefined` depending on ESM import order. SQLite and Postgres settings, raw
  key generation and error names: `computing-software.software-engineering.credo.askar-module-store-config`; keys,
  store key rotation, backups and tenants: `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`.
- **Multi-tenant:** `multiWalletDatabaseScheme` defaults to `DatabasePerWallet`; the config comments recommend
  `ProfilePerWallet` for performance.
- **DIDComm endpoints:** with no `endpoints`, Credo advertises the `didcomm:transport/queue` endpoint (for agents that
  only receive over return routes, such as mobile). Behind a proxy, set the public URL here, not the bind port.
- **Transports** can be passed in `DidCommModule({ transports })` or added later with
  `agent.didcomm.registerInboundTransport()` / `registerOutboundTransport()` before `initialize()`. The HTTP and WS
  *inbound* transports come from `@credo-ts/node`; the outbound ones from `@credo-ts/didcomm`.
- **Sharing one port for HTTP and WebSocket:** pass your own Express `app` to `DidCommHttpInboundTransport({ app, port })`
  and hand a `ws` `WebSocketServer({ noServer: true })` to `DidCommWsInboundTransport({ server })`, then forward
  `upgrade` events from `httpInboundTransport.server` (pattern in `samples/mediator.ts`). DIDComm HTTP transports and
  the OpenID4VC package expect Express 5.
- **Sub-modules of DIDComm** (`credentials`, `proofs`, `mediator`, `mediationRecipient`, `messagePickup`,
  `basicMessages`) are on by default; pass `false` to drop one. Connections, out-of-band and discover-features are
  always on.

## Lifecycle
- `initialize()` runs module initialisation, opens the root context, then checks the storage version. If storage is
  outdated it throws unless `autoUpdateStorageOnStartup: true` (see
  `computing-software.software-engineering.credo.upgrading-between-versions`). Re-initialising an initialised agent
  throws.
- `shutdown()` stops transports and closes the context. Call it on SIGTERM so SQLite/Postgres handles close cleanly.
- Listen to events with `agent.events.on(EventType, handler)`; event names are listed in each protocol skill.

## Failure modes
- `require()` of Credo from CommonJS: works only on Node versions that can require ESM; migrate the project instead.
- Hard-coded store keys in source: load them from a secret manager; losing the key loses the wallet.
- Mixing 0.6 and 0.7 packages, or old native bindings: dependency injection breaks in confusing ways.

## Verify
- [ ] `agent.isInitialized` is `true` after `initialize()` and the process logs no storage-version error.
- [ ] For DIDComm: an out-of-band invitation URL from `agent.didcomm.oob.createInvitation()` shows your public endpoint.
- [ ] Restarting the process reopens the same store (records created before restart are still there).

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3 (GitHub tag v0.7.3, 2026-10-24; npm `latest` 0.7.3). Source read from branch `v0.7.x` (package.json 0.7.3).
- Agent constructor, StorageService requirement, `initialize()` storage check and `shutdown()`: packages/core/src/agent/Agent.ts. `InitConfig` keys: packages/core/src/types.ts.
- Askar store options, KDF values, `NativeAskar` recommendation, multi-wallet default: packages/askar/src/AskarModuleConfig.ts.
- DidCommModule options, default sub-modules, queue endpoint default: packages/didcomm/src/DidCommModuleConfig.ts and DidCommModule.ts; `registerInboundTransport` on packages/didcomm/src/DidCommApi.ts.
- Inbound transports exported from `@credo-ts/node`: packages/node/src/index.ts. Shared-port pattern: samples/mediator.ts. Module wiring: demo/src/BaseAgent.ts.
- ESM-only, removed walletConfig/label, Express 5, Node 22/24, native binding versions, no ffi-napi: credo.js.org migration guides 0.5-to-0.6 and 0.6-to-0.7.
- The 0.5-to-0.6 guide's `getDefaultDidcommModules()` helper is not exported in 0.7.3, so this skill uses `new DidCommModule()`.

Method: documentation only; no commands were run.
