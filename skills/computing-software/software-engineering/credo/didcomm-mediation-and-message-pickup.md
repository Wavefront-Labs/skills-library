---
id: computing-software.software-engineering.credo.didcomm-mediation-and-message-pickup
name: didcomm-mediation-and-message-pickup
category: computing-software
field: software-engineering
product: credo
tags: [credo, credo-ts, didcomm, mediator, mediation, mediation-recipient, message-pickup, pickup-v2, live-mode, rfc-0211, rfc-0212, rfc-0685, websocket, mobile-agent, queue-transport-repository]
level: practitioner
status: docs-checked
description: "Run a Credo 0.7 DIDComm mediator and connect mobile agents to it: mediationRecipient config, pickup strategies (v1, v2, live mode, implicit), polling and queues."
sources:
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/samples/mediator.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/routing/DidCommMediationRecipientModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/routing/DidCommMediatorModuleConfig.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/routing/DidCommMediationRecipientApi.ts
  - https://github.com/openwallet-foundation/credo-ts/blob/v0.7.x/packages/didcomm/src/modules/routing/DidCommMediatorPickupStrategy.ts
  - https://credo.js.org/guides/tutorials/mediation
  - https://credo.js.org/guides/updating/versions/0.5-to-0.6
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DIDComm mediation and message pickup (Credo 0.7.x)

**Why:** a phone has no public address, so other agents cannot post DIDComm messages to it. A mediator is a cloud
agent that receives and queues messages for its recipients; the recipient picks them up or keeps a WebSocket open for
live delivery. Coordination follows Aries RFC 0211; pickup follows RFC 0212 (v1) and RFC 0685 (v2).

## Mediator (Node.js)
Mediator and mediation-recipient sub-modules are enabled by default in `DidCommModule`; configure the mediator side:
```ts
didcomm: new DidCommModule({
  endpoints: ['https://mediator.example.com', 'wss://mediator.example.com'],
  transports: {
    inbound: [httpInbound, wsInbound],          // DidCommHttpInboundTransport / DidCommWsInboundTransport from @credo-ts/node
    outbound: [new DidCommHttpOutboundTransport(), new DidCommWsOutboundTransport()],
  },
  mediator: { autoAcceptMediationRequests: true },   // default false
  connections: { autoAcceptConnections: true },
  // queueTransportRepository: <persistent queue>    // default is in-memory
}),
```
- Expose an invitation (the sample creates a fresh OOB invitation on each GET of `/invitation`) and serve HTTP and
  WebSocket on one port by forwarding `upgrade` events (see `samples/mediator.ts`).
- `messageForwardingStrategy`: `DirectDelivery` (default; deliver straight away, nothing queued), `QueueOnly`, or
  `QueueAndLiveModeDelivery`. The config marks `QueueAndLiveModeDelivery` as the intended future default.
- The default `InMemoryQueueTransportRepository` loses queued messages on restart and cannot be shared between
  instances. Implement `DidCommQueueTransportRepository` over a database for production (it replaced
  `MessagePickupRepository` in 0.6; every method now takes `AgentContext` first).

## Recipient (mobile or any agent without inbound transport)
```ts
didcomm: new DidCommModule({
  transports: { outbound: [new DidCommWsOutboundTransport(), new DidCommHttpOutboundTransport()] },
  mediationRecipient: {
    mediatorInvitationUrl: '<MEDIATOR_INVITATION_URL>',
    mediatorPickupStrategy: DidCommMediatorPickupStrategy.PickUpV2LiveMode,
  },
}),
```
With `mediatorInvitationUrl`, `initialize()` connects to the mediator, requests mediation and makes it the default
(the label sent is empty). For more control use the API: `requestAndAwaitGrant(connection)`, `provision(connection)`,
`setDefaultMediator(record)`, `findDefaultMediator()`, `getMediators()`.

Once a default mediator exists, new invitations and DID documents use its routing keys and endpoint automatically.

## Pickup strategies (`DidCommMediatorPickupStrategy`)
| Strategy | Behaviour | Transport |
|---|---|---|
| `PickUpV1` | poll every `mediatorPollingInterval` (default 5000 ms), batches of `maximumMessagePickup` (default 10) | HTTP or WS |
| `PickUpV2` | same polling loop using Pickup 2.0 | HTTP or WS |
| `PickUpV2LiveMode` | fetch the queue, then switch on live delivery over the open socket | WebSocket |
| `Implicit` | ping once and keep the socket open; messages ride the return route (used by ACA-Py mediators) | WebSocket |
| `None` | no automatic pickup; call the pickup API yourself | any |

If unset, Credo chooses a strategy through Discover Features. Reconnection after a dropped socket backs off from
`baseMediatorReconnectionIntervalMs` (default 100) doubling up to `maximumMediatorReconnectionIntervalMs` (default
unbounded); set the maximum on mobile to save battery.

Manual control: `agent.didcomm.mediationRecipient.initiateMessagePickup(mediator?, strategy?)` and
`stopMessagePickup()`; one-off fetch with `agent.didcomm.messagePickup.pickupMessages({ connectionId, protocolVersion:
'v2' })`.

## Failure modes
- Mobile app sets only HTTP outbound but asks for live mode: live mode and implicit pickup need a WebSocket.
- Mediator restarts with the in-memory queue: queued messages for offline wallets are gone.
- Mediator advertises `localhost` or the wrong scheme in `endpoints`: recipients cannot reach it from a device.
- Several mediator instances behind a load balancer: the default queue is per process, so a message queued on one
  instance is invisible to another. Share a persistent queue repository between instances.

## Verify
- [ ] `findDefaultMediator()` returns a record in `granted` state after startup.
- [ ] An invitation created by the recipient lists the mediator endpoint and a routing key.
- [ ] A message sent while the app was closed is delivered after the app reconnects.

## Checked
- Date: 2026-10-27. Release: Credo 0.7.3; source read from branch `v0.7.x`.
- Recipient options and defaults (polling 5000 ms, batch 10, backoff 100 ms to infinity, invitation URL, Discover Features fallback): DidCommMediationRecipientModuleConfig.ts. Strategy enum: DidCommMediatorPickupStrategy.ts. WebSocket need for live and implicit modes, polling loop and API methods: DidCommMediationRecipientApi.ts.
- Mediator options (`autoAcceptMediationRequests` default false, forwarding strategies and default): DidCommMediatorModuleConfig.ts. In-memory default queue: DidCommModuleConfig.ts.
- Mediator wiring, `/invitation` route and HTTP/WS upgrade sharing: samples/mediator.ts.
- Empty label when provisioning through `mediatorInvitationUrl`, QueueTransportRepository rename: packages/didcomm/CHANGELOG.md 0.6.0 and credo.js.org 0.5-to-0.6 guide. Mobile rationale: credo.js.org mediation tutorial.
- `granted` state value: packages/didcomm/src/modules/routing/models/DidCommMediationState.ts (requested, granted, denied).

Method: documentation only; no commands were run.
