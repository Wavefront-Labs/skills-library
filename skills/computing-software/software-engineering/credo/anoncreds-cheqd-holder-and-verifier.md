---
id: computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier
name: anoncreds-cheqd-holder-and-verifier
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, anoncreds, cheqd, did-cheqd, holder, verifier, react-native, anoncreds-react-native, askar-react-native, wallet, mobile-wallet, proof-request, link-secret, revocation, non-revoked, nodejs, web-app, verifiable-credentials]
level: practitioner
status: docs-checked
description: "Hold and verify AnonCreds credentials whose ids are did:cheqd resources with Credo 0.7: React Native holder wiring, Node verifier backend, resolution behaviour, checks that matter."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/anoncreds/services/CheqdAnonCredsRegistry.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/ledger/CheqdLedgerService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/src/dids/didCheqdUtil.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/AnonCredsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/anoncreds/src/services/tails/BasicTailsFileService.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/cheqd/tests/setupCheqdModule.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/react-native/package.json
  - https://docs.cheqd.io/product/llms-full.txt
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AnonCreds on cheqd: holder (React Native) and verifier (Node.js) with Credo 0.7.x

**Goal:** a phone wallet that receives and presents AnonCreds credentials issued under `did:cheqd`, and a verifier service
that checks them, with neither needing a payer seed because both only read from the network. The issuer side is
`computing-software.software-engineering.credo.anoncreds-cheqd-issuer-backend`; wiring is
`computing-software.software-engineering.credo.cheqd-module-setup`. The DIDComm exchanges themselves (connection, offer,
accept, proof request, presentation) are unchanged by cheqd: follow
`computing-software.software-engineering.credo.didcomm-connections-out-of-band`,
`computing-software.software-engineering.credo.didcomm-credential-issuance` and
`computing-software.software-engineering.credo.didcomm-proof-requests`, registering the `anoncreds` format service on both
sides. App-level recipes: `computing-software.software-engineering.methods.credo-mobile-holder-wallet` (phone) and
`computing-software.software-engineering.methods.credo-web-issuer-verifier-service` (web, with Credo in a Node backend).

## What the ids look like (what a wallet and verifier receive)
- Issuer DID: `did:cheqd:<testnet|mainnet>:<uuid>`.
- Schema, credential definition, revocation registry definition ids: `<issuerDid>/resources/<resource-uuid>`.
- The registry resolves these through the chain's DID-Linked Resource queries. Revocation status lists are fetched by
  resource name, type and a timestamp, not by id.
- A credential therefore carries a network name; a wallet or verifier with no entry for that network cannot resolve it.

## React Native holder wiring (illustrative, 0.7.3)
```ts
import { AnonCredsModule } from '@credo-ts/anoncreds'
import { AnonCredsDidCommCredentialFormatService, AnonCredsDidCommProofFormatService } from '@credo-ts/anoncreds/didcomm'
import { CheqdModule, CheqdDidResolver } from '@credo-ts/cheqd'
import { CheqdAnonCredsRegistry } from '@credo-ts/cheqd/anoncreds'
import { DidsModule } from '@credo-ts/core'
import { NativeAnoncreds } from '@hyperledger/anoncreds-react-native'

anoncreds: new AnonCredsModule({ anoncreds: NativeAnoncreds, registries: [new CheqdAnonCredsRegistry()] }),
cheqd: new CheqdModule({ networks: [{ network: 'mainnet' }, { network: 'testnet' }] }),   // no payer seed on a phone
dids: new DidsModule({ resolvers: [new CheqdDidResolver()] }),
```
plus Askar (`NativeAskar` from `@openwallet-foundation/askar-react-native`), polyfills and mediator exactly as in
`computing-software.software-engineering.credo.react-native-mobile-agent`, and the DIDComm credential and proof protocols
listing the AnonCreds format services (see the two DIDComm skills for the exact registration).
- Do not hand the app a `cosmosPayerSeed`: without one the module generates a throwaway wallet that cannot pay, which is what
  a reader needs. Never embed a funded seed in a mobile bundle.
- Include only the networks the wallet should accept; list `testnet` in production builds only if you intend to accept
  test credentials.
- `AnonCredsModule` creates a link secret automatically (`autoCreateLinkSecret` defaults to true); the holder's credentials
  are bound to it, so it lives in the Askar store and is lost with it. Decide the wallet backup and restore story before
  shipping (see the Askar store key notes in the React Native skill).
- React Native specifics for the cheqd dependencies (cosmjs aliasing, Buffer shim) are in `cheqd-module-setup`, including
  which parts could not be confirmed for 0.7.3. The `@hyperledger/anoncreds-react-native` binding needs the native
  linking steps of that package; the Credo docs page for it was not fully readable in this check, so follow the package's
  own README and pin `^0.4.0` for Credo 0.7.
- Resolving is a network call to the configured RPC (default `https://rpc.cheqd.net` mainnet, `https://rpc.cheqd.network`
  testnet; override with `rpcUrl`). For a production app consider your own RPC endpoint and handle timeouts in the UI.
  Tails files for revocable credentials are separate downloads from the URL in the registry definition, verified by hash.
- Resolved objects may be served from a local record or a cache (the registry advertises `allowsLocalRecord` and
  `allowsCaching`), so a repeated presentation does not necessarily re-query the chain.

## Verifier backend (Node.js)
- Same module wiring with `networks` for the networks you accept, no seed, plus the `anoncreds` DIDComm proof format.
- A proof request names restrictions; the verifier resolves schema, credential definition, and (if `non_revoked` is
  asked) the revocation registry definition and a status list through the cheqd registry during verification.
  Always restrict by `cred_def_id` or `issuer_id` and read `isVerified` on the proof exchange record, as in
  `didcomm-proof-requests`; a cryptographically valid proof from an unknown issuer still verifies.
- For revocation checks, `non_revoked: { from?, to }` uses unix-second timestamps. The resolver picks the status list
  version created closest before (at or earlier than) the requested timestamp (`getClosestResourceVersion`), so a
  timestamp earlier than the first status list finds nothing, and a recent `to` returns the newest list.
- For a web app, the backend creates the proof request (connection-based or connectionless out-of-band, see the DIDComm
  skills) and the browser only shows a QR code and polls your API for the result.

## Failure modes
- Offer or proof fails to resolve with `unable to resolve schema/credential definition: ...`: the network of the id is not in
  `networks`, the RPC is unreachable, or the issuer wrote to a different network.
- Revocable credential fails to prove: the tails URL is unreachable, or its content does not match the registered
  hash (the download is hash-checked).
- Verifier accepts a proof from the wrong issuer: missing `restrictions`.
- Wallet restored on a new device with no store backup: link secret and credentials are gone; the on-chain objects are
  unaffected.
- Wallet pinned to old native bindings: install the versions in the Credo 0.6-to-0.7 migration guide.

## Verify
- [ ] On a device, a test credential from the issuer (testnet) reaches state `done` and
  `agent.modules.anoncreds.getCredentials({})` (or the credential records) lists it after an app restart.
- [ ] Airplane mode: the wallet shows a clear resolution failure, not a crash, when the RPC is unreachable.
- [ ] The verifier's exchange record ends with `isVerified === true`, and a proof request restricted to a different
  `cred_def_id` fails to be satisfied by that credential.
- [ ] With revocation: after the issuer revokes and publishes a new status list, a fresh `non_revoked` request fails.

## Checked
- Date: 2026-10-28. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Registry read paths (resolve by resource id, by name/type/time; local-record and caching flags; error text): packages/cheqd/src/anoncreds/services/CheqdAnonCredsRegistry.ts and dids/CheqdDidResolver.ts. Default RPC URLs, seedless random wallet: ledger/CheqdLedgerService.ts, dids/didCheqdUtil.ts. `NativeAnoncreds`, React Native snippet, `autoCreateLinkSecret`: packages/anoncreds/src/AnonCredsModuleConfig.ts. Tails download with hash check: services/tails/BasicTailsFileService.ts. Module combination: cheqd/tests/setupCheqdModule.ts. RN peer dependencies: packages/react-native/package.json (see the React Native skill).
- cheqd docs (fetched 2026-10-28, llms-full.txt): proof request and issue flow examples (0.5 API; names differ in 0.7, so exchange calls are cited from the DIDComm skills); cosmjs-rn and Buffer notes.
- Not confirmed: holder-side behaviour when offline; whether a holder-only app can omit `CheqdDidRegistrar` entirely (read paths in source use only the resolver and ledger service; not run); native linking steps for `@hyperledger/anoncreds-react-native` on 0.7.

Method: documentation only; no commands were run.
