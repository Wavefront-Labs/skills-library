---
id: computing-software.game-programming.godot.rpc-annotations-and-authority
name: rpc-annotations-and-authority
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, multiplayerapi, godot-rpc, rpc-annotation, multiplayer-authority, set-multiplayer-authority, get-remote-sender-id, call-local, unreliable-ordered, game-programming]
level: practitioner
status: docs-checked
description: "Use Godot 4 @rpc correctly: mode/sync/transfer/channel options, multiplayer authority per node, validating senders on the server, and node path matching rules."
sources: ["https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html", "https://docs.godotengine.org/en/stable/classes/class_multiplayerapi.html", "https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-rpc", "https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html", "https://docs.godotengine.org/en/stable/classes/class_multiplayerpeer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RPC annotations and authority in Godot 4

**Goal:** remote calls that reach the right peers, are rejected from the wrong ones, and do not
silently fail on node-path mismatches.

## The annotation
```gdscript
@rpc(mode, sync, transfer_mode, channel)
# mode:          "authority" (default: only the node's multiplayer authority may call it remotely)
#                "any_peer"  (any peer may call: validate the sender!)
# sync:          "call_remote" (default: not executed locally) | "call_local"
# transfer_mode: "unreliable" | "unreliable_ordered" | "reliable" (default)
# channel:       int, separate ordering channels
```
Examples:
```gdscript
@rpc("any_peer", "call_remote", "reliable")
func request_fire(aim: Vector3) -> void:
    if not multiplayer.is_server(): return
    var sender := multiplayer.get_remote_sender_id()
    if sender != get_multiplayer_authority(): return       # this player's node only
    if not _can_fire(): return
    _spawn_projectile(aim)
    play_fire_fx.rpc()                                     # tell everyone

@rpc("authority", "call_local", "unreliable_ordered")
func play_fire_fx() -> void:
    $Muzzle/Particles.restart()
```
Call styles: `func_name.rpc(args)` to all peers, `func_name.rpc_id(peer_id, args)` to one peer
(`1` is the server). The calling peer runs it locally only with `call_local`.

## Authority
- Each node has a multiplayer authority peer id (default 1 = server), inherited by children when set
  recursively: `player.set_multiplayer_authority(peer_id)` (second arg `recursive=true`).
- Set it identically on every peer, typically from the node name: name player nodes after their peer
  id (`str(id)`) when spawning so all peers agree. `_enter_tree()` is a good place:
  `set_multiplayer_authority(name.to_int())`.
- `is_multiplayer_authority()` decides who reads input / simulates for that node.

## Path matching (the silent failure)
RPCs are addressed by **NodePath**. The node must exist at the same path with the same script RPC
config on sender and receiver. The docs require the same NodePath, so the same name: use
`add_child(node, true)` (`force_readable_name`) for nodes that use RPCs, or spawn via
`MultiplayerSpawner` so paths match.

## Security
- Any `any_peer` function is a public server API: check `get_remote_sender_id()`, validate ranges,
  rate-limit.
- Never send node paths or resource paths from clients that the server will load.
- Do not trust client-computed results (damage, positions) without server checks.

## Debugging
The debugger's Network Profiler lists nodes that use the multiplayer API with incoming and outgoing
counters and a bandwidth meter.

## Verify
- [ ] A client calling an "authority" RPC on a node it does not own has no effect on the server.
- [ ] `any_peer` handlers ignore calls from non-owners.
- [ ] Late-joining clients get node names identical to existing peers.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the High-level multiplayer tutorial, MultiplayerAPI, MultiplayerPeer and Node class pages and the Debugger panel page: @rpc defaults (authority, call_remote, reliable, channel 0), argument order, get_remote_sender_id, set_multiplayer_authority(id, recursive=true), is_multiplayer_authority, rpc_id, TARGET_PEER_SERVER = 1, same-NodePath rule, Network Profiler. Removed: 0-if-local comment, Node not found error text and Player2 example, Customize Run Instances 4.3+ claim, error-logged claim.
Method: documentation only; no commands were run.
