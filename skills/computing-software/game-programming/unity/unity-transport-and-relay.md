---
id: computing-software.game-programming.unity.unity-transport-and-relay
name: unity-transport-and-relay
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-netcode, unity-transport, unity-relay, netcode-for-gameobjects, join-codes, nat-traversal, game-programming]
level: practitioner
status: docs-checked
description: "Connect Netcode for GameObjects games through Unity Relay: packages, NetworkManager and UnityTransport setup, host allocation and join code, joining, udp/dtls/wss, WebGL."
sources: ["https://docs.unity.com/ugs/manual/relay/manual/relay-and-ngo"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity Transport and Relay

**Goal:** players connect through Unity Relay with Netcode for GameObjects (NGO) using the Relay allocation and join code flow.

## Setup
- Unity's page says the unified Multiplayer Services package (`com.unity.services.multiplayer`) replaces the standalone Relay package, which is deprecated in Unity 6; install it from the Unity Registry in Package Manager, plus `com.unity.netcode.gameobjects`.
- Link the project to Unity services first (project settings; see Get started with Multiplayer Services).
- Add a GameObject with the `NetworkManager` component, select `UnityTransport` as the transport, and set the Protocol Type of the Unity Transport component to Relay Unity Transport.

## Host
Initialize Unity Services, sign in (the sample uses anonymous sign-in), create an allocation for the expected number of connections, hand the Relay server data to the transport, request the join code and start the host. The documented sample:
```csharp
public async Task<string> StartHostWithRelay(int maxConnections, string connectionType)
{
    await UnityServices.InitializeAsync();
    if (!AuthenticationService.Instance.IsSignedIn)
        await AuthenticationService.Instance.SignInAnonymouslyAsync();
    var allocation = await RelayService.Instance.CreateAllocationAsync(maxConnections);
    NetworkManager.Singleton.GetComponent<UnityTransport>().SetRelayServerData(AllocationUtils.ToRelayServerData(allocation, connectionType));
    var joinCode = await RelayService.Instance.GetJoinCodeAsync(allocation.AllocationId);
    return NetworkManager.Singleton.StartHost() ? joinCode : null;
}
```
Call `StartServer` instead of `StartHost` to run a server rather than a host.

## Client
The join code from the host's allocation is passed to `RelayService.Instance.JoinAllocationAsync(joinCode: joinCode)`; then `SetRelayServerData(AllocationUtils.ToRelayServerData(allocation, connectionType))` and `NetworkManager.Singleton.StartClient()`.

## Connection type
Must be one of `udp`, `dtls` (encrypted; see the DTLS page) or `wss` (Web).

## WebGL / Web platform
Upgrade the Unity Transport package to 2.0.0 or later, pass `wss` as the connection type and set `UnityTransport.UseWebSockets = true`.

## Sessions
The Multiplayer Services package introduces sessions; Unity points to "Build a session with Netcode for GameObjects" as the alternative to wiring Relay by hand.

## Verify
- [ ] Two players on different networks connect with the join code.
- [ ] Both sides use the same connection type.

## Checked
Confirmed against the Relay and Netcode for GameObjects page (packages, setup steps, sample code, connection types, Web requirements). Removed because the Unity Transport page and other sources were not readable (the cited docs-multiplayer.unity3d.com page returns only a redirect stub): direct-connect `SetConnectionData` advice, timeout defaults, packet queue and payload settings, DTLS certificate guidance, allocation expiry, region selection, the `CreateSessionAsync` call and the debug network simulator.
Method: docs-only read of cited pages, 2026-11-08
