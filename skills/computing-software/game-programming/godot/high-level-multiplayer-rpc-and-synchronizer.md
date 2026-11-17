---
id: computing-software.game-programming.godot.high-level-multiplayer-rpc-and-synchronizer
name: high-level-multiplayer-rpc-and-synchronizer
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, multiplayer, rpc, multiplayerapi, multiplayersynchronizer, multiplayerspawner, authority, enet, scene-replication-interface, peer-id, game-programming]
level: advanced
status: docs-checked
description: "Replicate nodes and calls in Godot 4's high-level multiplayer API: @rpc annotations, authority, and MultiplayerSynchronizer/Spawner."
sources: ["https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html", "https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html", "https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html", "https://docs.godotengine.org/en/stable/classes/class_enetmultiplayerpeer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Godot 4 high-level multiplayer: RPCs, authority, and synchronizers

**Goal:** get networked state and remote calls working using Godot's built-in
scene replication interface, without hand-rolling a packet protocol — and avoid
the authority mistakes that make every client think it's the server.

## Setting up a peer
```gdscript
var peer = ENetMultiplayerPeer.new()
peer.create_server(7777, 32)          # host
# or: peer.create_client("127.0.0.1", 7777)   # client
multiplayer.multiplayer_peer = peer
```
`multiplayer` is a singleton-like `MultiplayerAPI` accessible from any node;
`multiplayer.is_server()`, `multiplayer.get_unique_id()` are the two checks
you'll write constantly.

## `@rpc` annotations — read every parameter
```gdscript
@rpc("authority", "call_remote", "reliable")
func take_damage(amount: int) -> void: ...

@rpc("any_peer", "call_local", "unreliable")
func send_input(input_vector: Vector2) -> void: ...
```
- First arg: **who is allowed to call this remotely** — `"authority"` (only the
  node's authority, usually the server, may trigger it remotely) vs
  `"any_peer"` (any connected peer may call it — use for client-to-server input,
  never for anything a cheating client shouldn't control). The sending and
  receiving node must have the same NodePath, so give RPC nodes matching names (use
  `force_readable_name` in `add_child()`).
- Second: `call_local` runs the function locally too when you call it, vs
  `call_remote`-only which only runs on the remote end — mixing this up means
  either double-executing locally or never seeing your own effect.
- Third: `reliable` vs `unreliable` vs `unreliable_ordered`, same tradeoff as
  any netcode: reliable for one-shot gameplay events, unreliable for
  high-frequency position/input updates where a dropped packet just gets
  superseded by the next one.
Call with `my_node.take_damage.rpc(10)` (broadcast per the annotation's target)
or `.rpc_id(peer_id, 10)` for a specific peer.

## Authority — the concept that trips up every beginner
Every node has a `set_multiplayer_authority(peer_id)` — the peer allowed to
control it. By default, everything is authority of the server (peer id 1). A
player's own character node needs `set_multiplayer_authority(owning_peer_id)`
set **on spawn, on every peer** (server and all clients must agree on who owns
what) so that peer is the authority for that node (the docs: the authority is the
server by default, changed per node with `set_multiplayer_authority`).

## MultiplayerSynchronizer and MultiplayerSpawner
- **MultiplayerSynchronizer**: attach to a node, list the properties to
  replicate (position, animation state). It replicates them from the authority
  to other peers; `replication_interval` (default 0.0) sets the interval.
  `public_visibility` (default true) plus per-peer visibility (`set_visibility_for`)
  lets you limit which peers see a node's state.
- **MultiplayerSpawner**: `add_spawnable_scene()` registers scenes that are
  automatically replicated from the authority to other peers when added as
  children of the node at `spawn_path`; do not call `add_child()` on nodes
  returned by a custom `spawn()`, it is done automatically.

## Verify
- [ ] Every `@rpc` call's first/second argument deliberately chosen, not left at
      the default `authority`/`call_remote` without checking it's correct for
      that call's direction.
- [ ] Each player-controlled node's authority is set identically on server and
      all clients at spawn time.
- [ ] Gameplay-critical RPCs are `reliable`; continuous state uses a
      MultiplayerSynchronizer or `unreliable` RPC, not both doing the same job.
- [ ] Tested with 1 host + 2 client instances locally (not just 2 total) —
      catches "works for the second player, breaks for the third" authority bugs.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the High-level multiplayer tutorial and the ENetMultiplayerPeer, MultiplayerSynchronizer, MultiplayerSpawner class pages: create_server/create_client, is_server, get_unique_id, @rpc mode names and meanings, unreliable_ordered, set_multiplayer_authority default server, replication_interval 0.0, public_visibility true, spawn_path, add_spawnable_scene, set_visibility_for. Added: same-NodePath requirement. Removed: silently-dropped claim, synchronizer-fights-input explanation, Replication Editor name, spawner-absent add_child claim.
Method: documentation only; no commands were run.
