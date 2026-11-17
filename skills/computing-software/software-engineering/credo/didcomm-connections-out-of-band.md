---
id: computing-software.software-engineering.credo.didcomm-connections-out-of-band
name: didcomm-connections-out-of-band
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, didcomm, out-of-band, oob, rfc-0434, did-exchange, rfc-0023, connections, invitation, qr-code, did-peer, did-peer-4, connection-events, aries]
level: practitioner
status: docs-checked
description: "Create and accept DIDComm out-of-band invitations with Credo 0.7 (agent.didcomm.oob), track connection records and events, and pick DID Exchange peer DID settings."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/oob/DidCommOutOfBandApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/connections/DidCommConnectionsApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/connections/DidCommConnectionsModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/connections/DidCommConnectionEvents.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Faber.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/demo/src/Alice.ts
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DIDComm connections with out-of-band invitations (Credo 0.7.x)

**Goal:** two agents hold a DIDComm connection (pairwise peer DIDs) so they can run credential, proof and message
protocols. Credo implements Out-of-Band 1.1 (Aries RFC 0434) for invitations and DID Exchange (RFC 0023) as the
handshake. Needs an agent with `DidCommModule` (`computing-software.software-engineering.credo.agent-setup-nodejs`).

## Inviter: create and publish an invitation
```ts
const outOfBandRecord = await agent.didcomm.oob.createInvitation({
  label: 'Example Issuer',            // label/imageUrl are per invitation since 0.6
  imageUrl: 'https://example.com/logo.png',
  multiUseInvitation: false,          // true = many holders may use it; not allowed together with messages
})
const url = outOfBandRecord.outOfBandInvitation.toUrl({ domain: 'https://issuer.example.com/invite' })
// render `url` as a QR code or deep link; keep outOfBandRecord.id to find the connection later
```
Options worth knowing: `handshakeProtocols` (defaults to every handshake the agent supports, in its order),
`handshake: false` with `messages` for connectionless requests, `goal`/`goalCode`, `autoAcceptConnection` (falls back
to the connections module setting), `alias`, `routing` (normally filled from the default mediator), and `invitationDid`
for an invitation that points at a public DID (cannot be combined with `routing`). `createLegacyInvitation()` produces
an RFC 0160 connection invitation for agents that only speak the old protocol, which 0.6 deprecated.

## Invitee: receive the invitation
```ts
const { outOfBandRecord, connectionRecord } = await agent.didcomm.oob.receiveInvitationFromUrl(url, {
  label: 'Alice wallet',              // required in 0.7
})
const connected = await agent.didcomm.connections.returnWhenIsConnected(connectionRecord!.id, { timeoutMs: 20000 })
```
`receiveInvitationFromUrl` parses (including shortened URLs) and calls `receiveInvitation`; use `parseInvitation(url)`
first if you want to show the inviter's label and ask the user. Config: `autoAcceptInvitation`,
`autoAcceptConnection`, `reuseConnection` (reuse an existing connection to the same inviter via handshake-reuse instead
of creating a duplicate), `routing`, `acceptInvitationTimeoutMs`, `ourDid`. With `autoAcceptInvitation: false`, accept
later with `agent.didcomm.oob.acceptInvitation(outOfBandRecord.id, { ... })`.

## Inviter: find the resulting connection
Listen for state changes and match on the out-of-band id; also query in case the event already fired:
```ts
import { DidCommConnectionEventTypes, type DidCommConnectionStateChangedEvent } from '@credo-ts/didcomm'

agent.events.on<DidCommConnectionStateChangedEvent>(DidCommConnectionEventTypes.DidCommConnectionStateChanged, (e) => {
  if (e.payload.connectionRecord.outOfBandId !== outOfBandRecord.id) return
  // e.payload.connectionRecord.state, e.payload.previousState
})
const [existing] = await agent.didcomm.connections.findAllByOutOfBandId(outOfBandRecord.id)
```
Without `autoAcceptConnections` you must call `acceptRequest(connectionId)` (inviter) or `acceptResponse(connectionId)`
(invitee) yourself. Implicit invitations (`receiveImplicitInvitation` against a public DID) always need manual acceptance.

## Connections module settings (`DidCommModule({ connections: { ... } })`)
- `autoAcceptConnections` (default `false`).
- `peerNumAlgoForDidExchangeRequests`: default `PeerDidNumAlgo.ShortFormAndLongForm` (did:peer:4) since 0.6. Set
  `PeerDidNumAlgo.GenesisDoc` (did:peer:1) only for older agents that cannot resolve did:peer:4.
- `peerNumAlgoForDidRotation`: did:peer:4 by default; did:peer:2 is the other allowed value.

## Useful connection API
`getAll`, `getById`, `findAllByQuery`, `findByDid`, `sendPing`, `rotate({ connectionId, toDid? })` (DID rotation,
RFC 0794, emits `DidCommConnectionDidRotated`), `hangup({ connectionId, deleteAfterHangup? })`,
`addConnectionType`/`findAllByConnectionTypes` to tag connections (for example to mark your mediator), `deleteById`.

## Failure modes
- Invitation URL domain is not reachable by the invitee, or the endpoint in the invitation is `localhost`: set
  `DidCommModule({ endpoints })` to the public URL.
- Calling 0.5-style `agent.oob` or `agent.connections`: those moved to `agent.didcomm.*` in 0.6.
- Waiting only on the event: if the connection completed before you subscribed, you miss it; also query by
  out-of-band id as above.

## Verify
- [ ] Both sides reach `completed` state (`returnWhenIsConnected` resolves) within your timeout.
- [ ] `agent.didcomm.connections.sendPing(connectionId, {})` round-trips.
- [ ] A second scan of a single-use invitation is rejected; a multi-use one creates a new connection.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Invitation and receive option names, required `label` on receive, multi-use and messages restriction, `invitationDid`/`routing` exclusivity, `receiveImplicitInvitation`, `acceptInvitation`, `parseInvitation`, `createLegacyInvitation`: packages/didcomm/src/modules/oob/DidCommOutOfBandApi.ts.
- Connection API methods incl. `returnWhenIsConnected(id, { timeoutMs })`, `rotate`, `hangup`, connection types: DidCommConnectionsApi.ts. Defaults for auto-accept and peer DID algorithms, implicit-invitation note: DidCommConnectionsModuleConfig.ts. Event names and payloads: DidCommConnectionEvents.ts.
- Event-plus-query pattern and `toUrl({ domain })`: demo/src/Faber.ts; receive with label: demo/src/Alice.ts.
- Label moved per call, `agent.didcomm.*` access, did:peer:4 default, connection protocol v1 deprecation: credo.js.org 0.5-to-0.6 guide and packages/didcomm/CHANGELOG.md 0.6.0.

Method: documentation only; no commands were run.
