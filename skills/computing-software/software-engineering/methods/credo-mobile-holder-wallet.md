---
id: computing-software.software-engineering.methods.credo-mobile-holder-wallet
name: credo-mobile-holder-wallet
category: computing-software
field: software-engineering
product: methods
tags: [method, recipe, credo, credo-ts, mobile-wallet, holder-wallet, react-native, didcomm, openid4vc, mediation, decentralized-identity, ssi, production-tier]
level: advanced
status: draft
description: "Recipe: build a production React Native holder wallet on Credo 0.7: skills in order (setup, storage, mediation, DIDComm and/or OpenID4VC, upgrades) with gates per phase."
sources:
  - https://credo.js.org/guides/concepts/platform-and-environment
  - https://github.com/openwallet-foundation/credo-ts/tree/v0.7.x/packages/react-native
  - https://github.com/openwallet-foundation/credo-ts/tree/v0.7.x/demo-openid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Method: Credo mobile holder wallet (production tier)

## Outcome
A React Native app that holds a user's credentials in an encrypted on-device store, receives offers and proof
requests while offline (through a mediator for DIDComm) or by scanning OpenID4VC QR codes, asks the user before
sharing anything, and survives app updates and Credo upgrades without losing data. Targets Credo 0.7.x, whose docs
name React Native as the holder platform and Node.js as the issuer/verifier platform.

## Ingredients
| Phase | Skill ids |
|---|---|
| 1. Agent in the app | `computing-software.software-engineering.credo.react-native-mobile-agent`, `computing-software.software-engineering.mobile-development.secure-storage-and-permissions` |
| 2. Identity and keys | `computing-software.software-engineering.credo.dids-and-key-management`, `computing-software.software-engineering.credo.askar-module-store-config`, `computing-software.software-engineering.credo.askar-kms-keys-and-store-backup` |
| 3a. DIDComm channel (if your issuers use DIDComm) | `computing-software.software-engineering.credo.didcomm-mediation-and-message-pickup`, `computing-software.software-engineering.credo.didcomm-connections-out-of-band` |
| 3b. OpenID4VC channel (if your issuers use OID4VC) | `computing-software.software-engineering.credo.openid4vc-issuer-holder-verifier` |
| 4. Receive credentials | `computing-software.software-engineering.credo.didcomm-credential-issuance` (holder side), OID4VCI holder section of the 3b skill |
| 5. Present | `computing-software.software-engineering.credo.didcomm-proof-requests` (holder side), OID4VP holder section of the 3b skill |
| 4b. AnonCreds on cheqd (if issuers register on cheqd) | `computing-software.software-engineering.credo.cheqd-module-setup`, `computing-software.software-engineering.credo.anoncreds-cheqd-holder-and-verifier` |
| 6. App plumbing | `computing-software.software-engineering.mobile-development.deep-links-app-links-universal-links`, `computing-software.software-engineering.mobile-development.app-lifecycle-and-offline-sync` |
| 7. Upgrades | `computing-software.software-engineering.credo.upgrading-between-versions` |

## Ordering law
Storage and keys come first because every later phase writes records into the store and signs with its keys; a
store key chosen badly cannot be changed without re-keying the wallet. The transport channel (3a or 3b) must work
before any credential exchange can be tested. Presentation depends on held credentials. Upgrade handling is
designed before the first public release because the first release's store format is the one every later version
must open.

## Phases and gates
1. **Agent boots on both platforms.** Gate: cold start on a physical Android and iOS device initialises the agent
   with no native-binding or StorageService error, and a second launch opens the same store.
2. **Store key and identity.** The store key is random, kept in the platform keystore/keychain, and used with the
   `raw` KDF (or a user PIN with the default Argon2 KDF). Gate: uninstall/reinstall behaviour is a documented decision
   (backed-up or lost), and a holder DID or JWK binding key can be created and found again after restart.
3. **Channel.** 3a: mediation granted and pickup running. Gate: a message sent while the app is closed arrives within
   one pickup cycle after resume. 3b: holder-only `OpenId4VcModule`. Gate: a QR code from a test issuer resolves to an
   offer showing issuer name and credential types.
4. **Receive.** Gate: the user sees issuer and claims before accepting (no `Always` auto-accept on the holder), and
   accepted credentials are listed after an app restart.
5. **Present.** Gate: the user sees which claims will be shared and from which credential, can decline, and the test
   verifier reports a verified result; a request for a claim the user lacks shows a clear "cannot satisfy" state.
6. **Plumbing.** Gate: invitation, offer and request links open the app from the camera and from other apps; pickup
   stops on background and restarts on resume.
7. **Upgrade drill.** Gate: install build N, create data, install build N+1 with the next Credo patch or minor, and all
   records load (UpdateAssistant reports up to date).

## Acceptance criteria
- Every phase gate passed on at least one current Android and one current iOS device.
- No secret (store key, private keys) leaves the device or appears in logs.
- No exchange completes without an explicit user action on the holder.
- Upgrade drill passed for the Credo version shipped.

## Failure modes this method prevents
- Store key derived from something guessable or hard-coded, discovered only after release.
- A wallet that works on the simulator but cannot receive DIDComm messages on a real network (no mediator).
- Silent auto-acceptance that shares data without consent.
- An app update that bumps Credo and bricks existing wallets.

## Verify
Run the seven gates as a checklist per release. This method is a draft: it has not yet been executed end to end, and
its gates are the author's recommended thresholds rather than numbers from the Credo docs.
