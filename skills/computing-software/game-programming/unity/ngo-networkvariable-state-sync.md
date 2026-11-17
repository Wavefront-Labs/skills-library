---
id: computing-software.game-programming.unity.ngo-networkvariable-state-sync
name: ngo-networkvariable-state-sync
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-netcode, netcode-for-gameobjects, networkvariable, state-synchronization, inetworkserializable, networklist, game-programming]
level: practitioner
status: draft
description: "Synchronise state with NGO NetworkVariable and NetworkList: permissions, OnValueChanged, custom INetworkSerializable structs, late joiners and bandwidth."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/basics/networkvariable/", "https://docs-multiplayer.unity3d.com/netcode/current/advanced-topics/serialization/inetworkserializable/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NGO NetworkVariable state sync

**Goal:** persistent state (health, team, door open) that every client and late joiner sees correctly.

## Declare
```csharp
public class Health : NetworkBehaviour {
    public NetworkVariable<int> Current = new(100,
        NetworkVariableReadPermission.Everyone, NetworkVariableWritePermission.Server);

    public override void OnNetworkSpawn() {
        Current.OnValueChanged += OnHealthChanged;
        OnHealthChanged(0, Current.Value);                // apply initial value (late joiners!)
    }
    public override void OnNetworkDespawn() => Current.OnValueChanged -= OnHealthChanged;

    void OnHealthChanged(int old, int now) => healthBar.Set(now / 100f);

    public void Damage(int amount) { if (IsServer) Current.Value = Mathf.Max(0, Current.Value - amount); }
}
```
- Initialise in the field declaration (or before Spawn on the server), never in Awake on clients.
- Write permission `Owner` for client-authoritative values (cosmetics, input-driven aim); validate anyway.
- Read permission `Owner` hides private data (inventory) from other clients.
- Changes are batched and sent at the network tick (NetworkManager Tick Rate); several writes per tick
  send only the latest value.

## Types
- Supported: primitives, enums, `Vector3`, `Quaternion`, `Color`, `FixedString32Bytes/64/128`
  (not `string`), and structs implementing `INetworkSerializable`.
```csharp
public struct Loadout : INetworkSerializable, IEquatable<Loadout> {
    public int Weapon; public FixedString32Bytes Skin;
    public void NetworkSerialize<T>(BufferSerializer<T> s) where T : IReaderWriter { s.SerializeValue(ref Weapon); s.SerializeValue(ref Skin); }
    public bool Equals(Loadout o) => Weapon == o.Weapon && Skin.Equals(o.Skin);
}
```
- Mutating a field of a struct NetworkVariable requires reassigning `.Value` (copy, modify, assign).
  For reference/collection contents call `CheckDirtyState()` after in-place edits.
- `NetworkList<T>` for synchronised lists (`OnListChanged` with add/remove/value events). T must be
  unmanaged + IEquatable.

## Choosing vs RPCs
| State that persists (late joiners need it) | NetworkVariable |
| One-off events (explosion, sound) | RPC |
| Continuous transforms | NetworkTransform (or custom interpolated variable) |

## Gotchas
- Writing from a client without permission logs an error and is ignored.
- Big structs every tick waste bandwidth; split rarely and frequently changing fields.
- OnValueChanged doesn't fire for the initial value on spawn: call your handler in OnNetworkSpawn.

## Verify
- [ ] A client joining mid-match shows correct health/team immediately.
- [ ] Network Profiler shows variable updates only when values change.
