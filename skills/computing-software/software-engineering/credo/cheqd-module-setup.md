---
id: computing-software.software-engineering.credo.cheqd-module-setup
name: cheqd-module-setup
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, cheqd, did-cheqd, cheqd-network, cosmos, cosmjs, cosmospayerseed, cheqdmodule, cheqddidregistrar, cheqddidresolver, testnet, mainnet, faucet, cheq, fees, react-native, nodejs, ssi, anoncreds, ledger]
level: practitioner
status: docs-checked
description: "Add cheqd to a Credo 0.7 agent: @credo-ts/cheqd wiring for a Node issuer backend and a React Native holder, network config, payer account secrets, funding, fees, testnet to mainnet."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/CheqdModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/CheqdModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/ledger/CheqdLedgerService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/didCheqdUtil.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/tests/setupCheqdModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/package.json
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/pnpm-workspace.yaml
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/CHANGELOG.md
  - https://docs.cheqd.io/product/llms-full.txt
  - https://docs.cheqd.io/product/network/tools/testnet-faucet.md
  - https://docs.cheqd.io/product/network/cheqd/identity-write-pricing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding cheqd to a Credo agent (0.7.x): Node issuer backend and React Native holder

**Goal:** an agent that can resolve `did:cheqd` DIDs and cheqd-hosted AnonCreds objects (every app), and, on the issuer
or verifier-with-own-DID side, write DIDs and resources to the cheqd network. Written against **Credo 0.7.3**
(`@credo-ts/cheqd` 0.7.3). Credo runs only on Node.js and React Native, so a web app means a Node.js agent service that
the browser front end calls
(`computing-software.software-engineering.methods.credo-web-issuer-verifier-service`); a mobile app means a React Native
holder wallet (`computing-software.software-engineering.methods.credo-mobile-holder-wallet`).

## Who needs what
| Role | Needs a funded payer seed? | Why |
|---|---|---|
| Issuer backend (Node) | Yes | Creating a DID, schema, credential definition, revocation registry or status list is a paid transaction. |
| Verifier backend (Node), holder wallet (RN) | No | Resolving is a read. Source: with no `cosmosPayerSeed` the module generates a throwaway random wallet. |

## Packages
- `@credo-ts/cheqd`, plus `@credo-ts/anoncreds` (it is a dependency of the cheqd package) and the AnonCreds native
  binding for the platform: `@hyperledger/anoncreds-nodejs` (Node) or `@hyperledger/anoncreds-react-native` (RN), both
  `^0.4.0` for 0.7 (workspace pins). Askar and `@credo-ts/node` / `@credo-ts/react-native` as in
  `computing-software.software-engineering.credo.agent-setup-nodejs` and
  `computing-software.software-engineering.credo.react-native-mobile-agent`.
- There is no `AnonCredsRsModule` in 0.7. The AnonCreds-RS holder, issuer and verifier services are registered inside
  `AnonCredsModule`, which takes the binding directly as `anoncreds: NativeAnoncreds`. Older tutorials and the 0.5/0.6
  docs show `anoncreds` imported as a value from the binding package; use `NativeAnoncreds` (the config comments
  explain that the old export can be `undefined` depending on import order).
- Import the registry from the subpath `@credo-ts/cheqd/anoncreds`. The root export of `CheqdAnonCredsRegistry` is marked
  deprecated in 0.7.3. `CheqdModule`, `CheqdDidRegistrar`, `CheqdDidResolver`, `CheqdModuleConfig` come from the root.

## Wiring (illustrative, 0.7.3; same shape for Node and RN)
```ts
import { Agent, DidsModule } from '@credo-ts/core'
import { AnonCredsModule } from '@credo-ts/anoncreds'
import { CheqdModule, CheqdDidRegistrar, CheqdDidResolver } from '@credo-ts/cheqd'
import { CheqdAnonCredsRegistry } from '@credo-ts/cheqd/anoncreds'
import { NativeAnoncreds } from '@hyperledger/anoncreds-nodejs'   // RN: '@hyperledger/anoncreds-react-native'

modules: {
  // askar: new AskarModule({ askar: NativeAskar, store: { ... } }),  as in the platform setup skills
  anoncreds: new AnonCredsModule({
    anoncreds: NativeAnoncreds,
    registries: [new CheqdAnonCredsRegistry()],
    tailsFileService: ...,   // issuer with revocation only, see anoncreds-cheqd-issuer-backend
  }),
  cheqd: new CheqdModule({
    networks: [{ network: 'testnet', cosmosPayerSeed: process.env.COSMOS_PAYER_SEED /* <COSMOS_PAYER_SEED>, issuer only */ }],
  }),
  dids: new DidsModule({ registrars: [new CheqdDidRegistrar()], resolvers: [new CheqdDidResolver()] }),
}
```
- Passing `registrars`/`resolvers` to `DidsModule` replaces the defaults; see the gotcha in
  `computing-software.software-engineering.credo.dids-and-key-management` before adding did:web or did:key use.
- A holder or verifier that only reads can use `networks: [{ network: 'mainnet' }, { network: 'testnet' }]` with no seed.
- Keep `registries` order in mind when you also use Indy VDR (`new IndyVdrAnonCredsRegistry()`): each registry declares
  the identifiers it supports, and cheqd's matches `did:cheqd:(testnet|mainnet):...`.

## NetworkConfig fields (all of them)
`network` (string, required), `rpcUrl` (optional), `cosmosPayerSeed` (optional).
- `network` must be `testnet` or `mainnet`; the identifier regex only accepts those two. A DID on a network that is not
  in `networks` fails with "not found in cheqd networks configuration".
- Default RPC endpoints in source: mainnet `https://rpc.cheqd.net`, testnet `https://rpc.cheqd.network`. Set `rpcUrl` for
  your own node or a local test chain.
- `cosmosPayerSeed`: if it matches the English-mnemonic pattern it is used as a mnemonic (account prefix `cheqd`,
  addresses look like `cheqd1...`); any other string is taken as a raw key (the source feeds its UTF-8 bytes to a
  secp256k1 key, after stripping a leading `0x`). The cheqd docs say "a 32-bit seed value or a mnemonic".
- The module connects to every configured network in the background at `initialize()` without awaiting it; a network that
  fails to initialise is logged and skipped, then retried on first use. So a bad RPC URL or seed shows up as a failure at
  the first registration, not at start-up.
- `CheqdModule.register` sets `global.Buffer` to the `buffer` package when none exists (relevant on RN).

## Secrets
The payer seed controls real funds on mainnet. Load it from a secret manager or environment at start-up on the backend
only; never ship it in a mobile bundle or a web front end, and never log it (Credo logs registration errors with their
messages, so keep it out of exception text). Use separate seeds for testnet and mainnet. Keep it distinct from DID
signing keys: those live in the agent KMS (see `dids-and-key-management`), the payer seed only pays fees. The DID keys
sit in the Askar store, so the store key and backups matter as much as the seed:
`computing-software.software-engineering.credo.askar-kms-keys-and-store-backup` and
`computing-software.software-engineering.credo.askar-module-store-config`.

## React Native specifics
- The cheqd docs (page titled for 0.6.x, with Node 16/18 prerequisites) ask RN apps to alias the cosmjs packages to
  `@cosmjs-rn/*` at `^0.27.1` through npm `overrides` or Yarn `resolutions`, and to add a `shim.js` that sets
  `global.Buffer` to the `buffer` package, imported before the app. Not confirmed for 0.7.3: that guidance predates it.
  The 0.7.3 workspace pins `@cosmjs/*` to `^0.36.2` for `@cheqd/sdk-esm` 5.5.1, and 0.7.2 notes pinned CosmJS to match.
  Test an RN build before trusting the old overrides, and expect to need the platform polyfills in
  `computing-software.software-engineering.credo.react-native-mobile-agent`.
- A holder that only resolves still bundles the whole cosmjs/cheqd SDK dependency tree; keep the issuer-only code paths out
  of the app (do not give the app a payer seed).
- Hermes, Expo managed workflow and Metro behaviour for `@credo-ts/cheqd` are not covered by the sources read; not stated.

## Funding and fees (only what the official pages say)
- An address does not exist on chain until it holds CHEQ (cheqd docs hint on the Credo setup page).
- **Testnet:** the faucet is part of cheqd Studio (`https://studio.cheqd.net/`). It funds any `cheqd1...` testnet address,
  including one made for Credo. It needs a Studio account with an active Basic or Build plan or the 30-day trial of Basic;
  otherwise requests return 403. Request in the Studio account area ("Balances & Faucet") or with `POST
  https://studio-api.cheqd.net/account/faucet`, header `x-api-key: <STUDIO_API_KEY>`, JSON body with optional `address` and
  `amount` (CHEQ). Limits on the page: 100,000 CHEQ per account per UTC month, an address can be topped up to at most
  100,000, 10,000 sent when no amount is given, 10 seconds between requests; 429 carries `Retry-After`; after a 504 check the
  balance before retrying. The old standalone faucet site is no longer public.
- **Mainnet:** you need real CHEQ in the payer account (the network page points to `https://cheqd.io/get-involved/` for
  acquiring it). The docs give no purchase or custody steps beyond that, so none are given here.
- **Prices (docs, subject to governance change):** the identity-write pricing page lists mainnet DID write about USD 2.00
  (50 CHEQ), DID update about USD 1.00 (25 CHEQ), DID deactivate about USD 0.40 (10 CHEQ), and resource creation for
  AnonCreds objects (schema, credential definition, status list) about USD 0.10 (2.5 CHEQ) each; testnet writes are free
  in that table. The same page's first table lists "Resource create (default)" at USD 0.20, so treat resource prices as
  approximate and check the page for the current figure.
- Credo submits writes with a default fee option `{ slippageBps: 1000 }` (CheqdLedgerService) unless you pass `fee` or
  `feeOptions` in the create/update/deactivate/resource options. cheqd documents a fee market with prices in `ncheq`; the
  Credo-side details beyond that default were not read.
- Budget for the revocation write pattern: every status-list update is another resource write.

## Moving from testnet to mainnet
1. Add `{ network: 'mainnet', cosmosPayerSeed }` (a different, funded seed) beside or instead of the testnet entry.
2. Create the issuer DID again with `options.network: 'mainnet'`; testnet DIDs, schemas and credential definitions do not
   exist on mainnet, and every id embeds the network (`did:cheqd:mainnet:...`).
3. Re-register schema, credential definition, revocation registry and status list under the mainnet DID
   (`anoncreds-cheqd-issuer-backend`). Credentials issued from testnet ids stay bound to testnet ids.
4. Wallets and verifiers need `mainnet` in their own `networks` list to resolve the new ids.

## Failure modes
- "No cheqd networks configured" or "not found in cheqd networks configuration": the network of the DID is missing from
  `networks`.
- Registration fails with an insufficient-funds style error from the chain: payer address unfunded or too low (the failure
  text is returned in `didState.reason`, prefixed `unknownError:`).
- `cheqd` resolves nothing after adding `DidsModule`: the resolver is not listed in `resolvers`.
- Using the 0.5 tutorials (`walletConfig`, `agent.wallet.createKey`, `secret.verificationMethod`): those APIs are gone;
  see `cheqd-did-lifecycle`.

## Verify
- [ ] On a funded testnet seed, `agent.dids.create({ method: 'cheqd', options: { network: 'testnet', createKey: ... } })`
  returns `didState.state === 'finished'` (see `cheqd-did-lifecycle`).
- [ ] A second agent with a seedless config resolves that DID with `agent.dids.resolveDidDocument(did)`.
- [ ] The mobile bundle contains no payer seed (search the built bundle for the env var name or the seed's address prefix).

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- `CheqdModule` (config object, background connect, Buffer fallback): packages/cheqd/src/CheqdModule.ts. `NetworkConfig` fields: CheqdModuleConfig.ts. Default RPC URLs, background-initialise and skip-on-error behaviour, default `slippageBps: 1000`, "not found in networks" message: ledger/CheqdLedgerService.ts. Seed handling (random wallet when empty, mnemonic vs raw key, `cheqd` prefix): dids/didCheqdUtil.ts. Network values `testnet|mainnet` and identifier regexes: anoncreds/utils/identifiers.ts.
- Registry subpath and deprecated root export: src/index.ts and src/anoncreds/index.ts, package.json exports. Wiring shape (AnonCredsModule + CheqdModule + DidsModule): tests/setupCheqdModule.ts. `NativeAnoncreds` and no Rs module: packages/anoncreds/src/AnonCredsModuleConfig.ts and AnonCredsModule.ts (the repo's packages list has no anoncreds-rs package). Binding versions and cosmjs pins: pnpm-workspace.yaml; CosmJS pin note: packages/cheqd/CHANGELOG.md 0.7.2.
- cheqd docs (fetched 2026-10-28): Credo setup page in llms-full.txt (RN overrides, Buffer shim, unfunded-address hint); testnet faucet page; identity-write-pricing page (both tables as quoted).
- Not confirmed: whether the cosmjs-rn overrides work with 0.7.3; Hermes/Expo behaviour; mainnet CHEQ acquisition steps; Credo-side fee-market usage beyond the default option.

Method: documentation only; no commands were run.
