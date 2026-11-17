---
id: computing-software.software-engineering.credo.react-native-mobile-agent
name: react-native-mobile-agent
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, aries-framework-javascript, react-native, mobile-wallet, holder, askar, askar-react-native, expo-crypto, react-native-get-random-values, react-native-fs, secure-environment, metro, decentralized-identity, ssi]
level: practitioner
status: docs-checked
description: "Run a Credo 0.7 agent inside a React Native app: required native peers, Askar RN binding, polyfill and Metro notes, secure-environment KMS, and app lifecycle."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/react-native/package.json
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/react-native/src/index.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/react-native/src/kms/SecureEnvironmentKeyManagementService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/react-native/CHANGELOG.md
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/askar/src/AskarModuleConfig.ts
  - https://credo.js.org/guides/getting-started/set-up
  - https://credo.js.org/guides/updating/versions/0.6-to-0.7
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credo in a React Native app (0.7.x)

**Goal:** a mobile holder agent that stores keys and credentials on the device and talks to issuers and verifiers.
Written against **Credo 0.7.3**. The docs' platform page names exactly two runtimes, Node.js and React Native; the
intended split is a Node.js issuer/verifier and a React Native holder.

## Packages
- `@credo-ts/core`, `@credo-ts/react-native`, `@credo-ts/askar` and `@openwallet-foundation/askar-react-native`
  (0.7 expects `^0.6.0`; it replaced `@hyperledger/aries-askar-react-native` in 0.6).
- Add as needed: `@credo-ts/didcomm`, `@credo-ts/openid4vc`, `@credo-ts/anoncreds` with
  `@hyperledger/anoncreds-react-native` (`^0.4.0`), `@credo-ts/indy-vdr` with `@hyperledger/indy-vdr-react-native`
  (`^0.3.0`), `@credo-ts/cheqd`.
- Peer dependencies of `@credo-ts/react-native` 0.7.3:
  - `react-native` `>=0.71.4`;
  - `react-native-get-random-values` `>=1.11.0 <3.0.0`;
  - `expo-crypto` (required since 0.6; used for hashing in the W3C JSON-LD libraries);
  - one file-system module: `@dr.pogodin/react-native-fs` (preferred since 0.7) or the unmaintained
    `react-native-fs`; the package tries them in that order and throws if neither is installed;
  - optional `@animo-id/expo-secure-environment`, only for `SecureEnvironmentKeyManagementService`.

## Setup notes
- **Random values:** React Native has no `crypto.getRandomValues()`. `@credo-ts/react-native` imports
  `react-native-get-random-values` itself, and the docs also tell you to import it first in your entry file
  (`index.js`/`index.tsx`), so it is in place before any crypto code runs.
- **Metro:** the docs' set-up page asks for `cjs` in `resolver.sourceExts` because some dependencies ship `.cjs`
  files. That page was written for 0.5; keep the setting unless your Metro version already resolves `.cjs`.
- **ESM:** Credo is ESM-only since 0.6; Metro bundles it, so a React Native app needs no ESM migration.
- **Files:** `ReactNativeFileSystem` keeps data under `<DocumentDirectoryPath>/.afj` (cache and temp under the
  matching RNFS directories). Pass custom base paths to its constructor if you need them elsewhere.

## Agent (illustrative, 0.7.3)
```ts
import { Agent } from '@credo-ts/core'
import { agentDependencies } from '@credo-ts/react-native'
import { AskarModule } from '@credo-ts/askar'
import { NativeAskar } from '@openwallet-foundation/askar-react-native'
import { DidCommModule, DidCommHttpOutboundTransport, DidCommWsOutboundTransport,
         DidCommMediatorPickupStrategy } from '@credo-ts/didcomm'

const agent = new Agent({
  config: {},
  dependencies: agentDependencies,
  modules: {
    askar: new AskarModule({
      askar: NativeAskar,
      store: { id: 'wallet', key: walletKeyFromKeychain, keyDerivationMethod: 'raw' },
    }),
    didcomm: new DidCommModule({
      transports: { outbound: [new DidCommWsOutboundTransport(), new DidCommHttpOutboundTransport()] },
      mediationRecipient: {
        mediatorInvitationUrl: '<MEDIATOR_INVITATION_URL>',
        mediatorPickupStrategy: DidCommMediatorPickupStrategy.PickUpV2LiveMode,
      },
    }),
  },
})
await agent.initialize()
```
- No inbound transport: a phone has no public address. Receive through a mediator
  (`computing-software.software-engineering.credo.didcomm-mediation-and-message-pickup`). OpenID4VC-only wallets
  need no DIDComm module at all (`computing-software.software-engineering.credo.openid4vc-issuer-holder-verifier`).
- **Store key:** generate a random key once, keep it in the platform keychain/keystore, and use
  `keyDerivationMethod: 'raw'`, which the Askar config documents for keys held in an on-device keychain. With a
  user PIN as the key, keep the default Argon2 KDF.

## Device-bound keys
`SecureEnvironmentKeyManagementService` (backend name `secureEnvironment`) creates only P-256 (`EC`/`P-256`) keys, signs
only with `ES256`, can delete keys, and refuses import, encryption and random bytes. Backends are registered through
`new Kms.KeyManagementModule({ backends: [...] })` (the pattern the OpenID4VC demo uses for its extra Node backend);
when you add it, confirm the Askar backend is still listed, because Askar must keep handling Ed25519, X25519 and
encryption. Since 0.7.1 the KMS honours `defaultBackend` when no backend is named, so choose it deliberately.

## Lifecycle
- Initialise once (for example in a context provider); calling `initialize()` twice throws.
- When the app goes to the background, stop pickup with `agent.didcomm.mediationRecipient.stopMessagePickup()`; on
  resume call `initiateMessagePickup()` (both exist on the mediation recipient API).
- Call `agent.shutdown()` before deleting or re-keying the wallet.

## Failure modes
- Missing file-system peer: the error names both `@dr.pogodin/react-native-fs` and `react-native-fs`.
- Missing `expo-crypto`: JSON-LD credential hashing fails.
- Native binding versions that do not match the Credo minor: install the versions listed in the migration guide and pin
  them.

## See also
Askar store options, raw key generation (`Store.generateRawKey()`), install-time native download and open errors:
`computing-software.software-engineering.credo.askar-module-store-config`. Key types, store key rotation, backup and the
mobile key-storage flow: `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup`.

cheqd as the ledger for a holder wallet: `computing-software.software-engineering.credo.cheqd-module-setup` (including the
React Native cosmjs and Buffer notes) and `computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier`.

## Verify
- [ ] App start logs no StorageService or native-binding error and `agent.isInitialized` is `true`.
- [ ] Killing and reopening the app keeps connections and credentials (store opened with the same key).
- [ ] A test message sent to the wallet while backgrounded arrives after resume through the mediator.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3 (tag v0.7.3; npm `latest` 0.7.3). Source read from branch `v0.7.x`.
- Peer dependency list and ranges: packages/react-native/package.json. Self-import of `react-native-get-random-values` and `agentDependencies` (global fetch/WebSocket): packages/react-native/src/index.ts. FS lookup order and error: src/rnfs.ts. `.afj` paths: src/ReactNativeFileSystem.ts.
- `expo-crypto` required since 0.6 and switch to `@dr.pogodin/react-native-fs` in 0.7.0: packages/react-native/CHANGELOG.md.
- Secure-environment KMS operations: src/kms/SecureEnvironmentKeyManagementService.ts. `defaultBackend` fix: packages/core/CHANGELOG.md 0.7.1.
- `raw` KDF guidance and `NativeAskar` for React Native: packages/askar/src/AskarModuleConfig.ts. Native binding versions: credo.js.org 0.6-to-0.7 guide. Polyfill and Metro `cjs` advice: credo.js.org set-up page (0.5-era text).
- Not confirmed, so not stated: Hermes requirements, Expo managed versus bare workflow guidance (the current docs give none for 0.7).

Method: documentation only; no commands were run.
