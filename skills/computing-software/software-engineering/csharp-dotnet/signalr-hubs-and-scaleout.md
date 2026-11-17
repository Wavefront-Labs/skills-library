---
id: computing-software.software-engineering.csharp-dotnet.signalr-hubs-and-scaleout
name: signalr-hubs-and-scaleout
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-realtime-rpc, signalr-hubs, signalr, websockets, redis-backplane, strongly-typed-hubs]
level: practitioner
status: draft
description: "Build ASP.NET Core SignalR hubs: strongly typed clients, groups, auth, streaming, connection lifetime, backplane scale-out with Redis or Azure SignalR, and message size limits."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction", "https://learn.microsoft.com/en-us/aspnet/core/signalr/hubs", "https://learn.microsoft.com/en-us/aspnet/core/signalr/scale"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SignalR hubs

```csharp
public interface IChatClient { Task Receive(string user, string msg); }

[Authorize]
public class ChatHub(ILogger<ChatHub> log) : Hub<IChatClient>
{
    public async Task Send(string room, string msg) =>
        await Clients.Group(room).Receive(Context.UserIdentifier ?? "?", msg);
    public Task Join(string room) => Groups.AddToGroupAsync(Context.ConnectionId, room);
    public async IAsyncEnumerable<int> Counter([EnumeratorCancellation] CancellationToken ct) { for (var i=0;;i++){ yield return i; await Task.Delay(1000, ct); } }
    public override Task OnDisconnectedAsync(Exception? e) { log.LogInformation("bye {Id}", Context.ConnectionId); return base.OnDisconnectedAsync(e); }
}
builder.Services.AddSignalR(o => { o.MaximumReceiveMessageSize = 64 * 1024; o.EnableDetailedErrors = builder.Environment.IsDevelopment(); });
app.MapHub<ChatHub>("/chat");

// from outside a hub
public class Notifier(IHubContext<ChatHub, IChatClient> hub) { public Task Push(string m) => hub.Clients.All.Receive("system", m); }
```
Transports negotiate WebSockets -> Server-Sent Events -> long polling. Hub instances are transient per call: no instance state, and do not store connection data in fields; use groups or an external store. Browser tokens: send the access token in query string `access_token` for WebSockets and read it in `JwtBearerEvents.OnMessageReceived` (restricted to the hub path).

## Scale-out
Connections are per server. With more than one instance add a backplane (`AddStackExchangeRedis`) or Azure SignalR Service, and use sticky sessions unless WebSockets-only with `SkipNegotiation`. Keep `KeepAliveInterval` (15 s) and `ClientTimeoutInterval` (30 s) in ratio 1:2.

## Gotchas
- Hub methods run on the thread pool one at a time per connection (by default); long-running work blocks that client's messages.
- `Clients.All` sends to everyone; check authorization for groups.
- Reconnects get a new `ConnectionId`; use `UserIdentifier`.
- CORS must allow credentials for cross-origin clients.

## Verify
Two clients in a test (`HubConnectionBuilder` with `WebApplicationFactory`) join a room; only members receive the message; the disconnect handler fires.
