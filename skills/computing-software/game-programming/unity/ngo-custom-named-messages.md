---
id: computing-software.game-programming.unity.ngo-custom-named-messages
name: ngo-custom-named-messages
category: computing-software
field: game-programming
product: unity
tags: [unity, custom-messages, netcode-for-gameobjects, ngo, custommessagingmanager, fastbufferwriter, game-programming]
level: practitioner
status: docs-checked
description: "Netcode for GameObjects CustomMessagingManager API: register named message handlers, send named and unnamed messages with a FastBufferWriter and NetworkDelivery."
sources: ["https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.0/api/Unity.Netcode.CustomMessagingManager.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NGO custom named messages

**Goal:** send data between peers without RPCs bound to a spawned NetworkObject, using `CustomMessagingManager`
(namespace `Unity.Netcode`, assembly `Unity.Netcode.Runtime.dll`). The API page says these named messages are different from
the NetworkManager custom messages and "much easier to use".

## API surface (NGO 2.0)
Handlers:
- `RegisterNamedMessageHandler(string name, HandleNamedMessageDelegate callback)`: runs the callback when a named message is
  received.
- `UnregisterNamedMessageHandler(string name)`.
- Event `OnUnnamedMessage` (`UnnamedMessageDelegate`): invoked when unnamed messages arrive.

Sending named messages (all take a `FastBufferWriter` and a `NetworkDelivery` that defaults to `ReliableSequenced`):
- `SendNamedMessage(string messageName, ulong clientId, FastBufferWriter messageStream, NetworkDelivery)`
- `SendNamedMessage(string messageName, IReadOnlyList<ulong> clientIds, FastBufferWriter messageStream, NetworkDelivery)`
- `SendNamedMessageToAll(string messageName, FastBufferWriter messageStream, NetworkDelivery)`

Sending unnamed messages (same delivery default):
- `SendUnnamedMessage(ulong clientId, FastBufferWriter messageBuffer, NetworkDelivery)`
- `SendUnnamedMessage(IReadOnlyList<ulong> clientIds, ...)`: sends to everyone if the list is null.
- `SendUnnamedMessageToAll(FastBufferWriter messageBuffer, NetworkDelivery)`

```csharp
var cmm = NetworkManager.Singleton.CustomMessagingManager;
cmm.RegisterNamedMessageHandler("Chat", OnChat);
cmm.SendNamedMessageToAll("Chat", writer, NetworkDelivery.ReliableSequenced);
```
The `FastBufferWriter` (stream) holds the payload; the `ulong` clientId identifies the target client.

## Verify
- [ ] Each registered handler name is unregistered with `UnregisterNamedMessageHandler` when no longer needed.
- [ ] Sender and receiver use the same message name string.

## Checked
Date: 2026-11-09. Read in full: NGO 2.0 API page for `CustomMessagingManager`. The two docs-multiplayer.unity3d.com sources
(custom messages and FastBufferWriter/Reader) return only a stub page and were dropped. Removed as not confirmable from the
API page: handler registration timing, the `FastBufferWriter` constructor and `WriteValueSafe` usage, server relay and
client-to-client behaviour, name hashing, delivery mode list and fragmentation, `OverflowException`, and the unnamed
message header-byte advice.
Method: docs-checked 2026-11-09 against the NGO 2.0 CustomMessagingManager API page.
