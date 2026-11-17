---
id: computing-software.game-programming.unity.ngo-connection-approval
name: ngo-connection-approval
category: computing-software
field: game-programming
product: unity
tags: [unity, netcode-for-gameobjects, connection-approval, connection-payload, player-prefab-selection, game-programming]
level: practitioner
status: draft
description: "Gate Netcode for GameObjects joins with ConnectionApprovalCallback: payload validation, version checks, capacity, choosing player prefabs and spawn points, rejection reasons."
sources: ["https://docs-multiplayer.unity3d.com/netcode/current/basics/connection-approval/", "https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.1/api/Unity.Netcode.NetworkManager.ConnectionApprovalRequest.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NGO connection approval

**Goal:** the server decides who joins, with what character, where — and tells rejected clients why.

## Enable
NetworkManager > Connection Approval ticked, then on the server/host before `StartServer/StartHost`:
```csharp
nm.ConnectionApprovalCallback = (req, res) => {
    var payload = JsonUtility.FromJson<JoinPayload>(Encoding.UTF8.GetString(req.Payload));
    if (payload.buildVersion != Application.version) { Reject(res, "version_mismatch"); return; }
    if (nm.ConnectedClientsIds.Count >= maxPlayers)    { Reject(res, "server_full"); return; }
    res.Approved = true;
    res.CreatePlayerObject = true;
    res.PlayerPrefabHash = PrefabHashFor(payload.characterId);   // null = default player prefab
    res.Position = spawnPoints.Next(); res.Rotation = Quaternion.identity;
    res.Pending = false;
};
void Reject(NetworkManager.ConnectionApprovalResponse res, string reason) {
    res.Approved = false; res.Reason = reason; res.Pending = false;
}
```
Client side, before `StartClient`:
`nm.NetworkConfig.ConnectionData = Encoding.UTF8.GetBytes(JsonUtility.ToJson(payload));`
and read the reason in `nm.OnClientDisconnectCallback` via `nm.DisconnectReason`.

## Async approval
Set `res.Pending = true` and finish later (e.g. after verifying a session ticket with a backend);
must complete before the connection timeout (NetworkConfig > Client Connection Buffer Timeout).

## Rules
- The host's own connection also goes through the callback (clientId == ServerClientId).
- Payload is size-limited (keep it small; NGO limits connection data); never trust it — it's a
  claim. Verify tokens server-side.
- `PlayerPrefabHash` must be a prefab registered in the Network Prefabs list.

## Gotchas
- Forgetting `Pending = false` leaves clients hanging until timeout.
- With approval enabled and no callback set, all connections are rejected.

## Verify
- [ ] Old build version gets a "version_mismatch" message on screen.
- [ ] Join with a full server: client receives "server_full" and returns to menu.
