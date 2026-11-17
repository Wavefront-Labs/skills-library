---
id: computing-software.software-engineering.csharp-dotnet.server-sent-events-in-aspnet-core
name: server-sent-events-in-aspnet-core
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-realtime-rpc, server-sent-events, sse, iasyncenumerable, streaming-responses, channels]
level: practitioner
status: docs-checked
description: "Stream server-sent events from ASP.NET Core with IAsyncEnumerable and TypedResults.ServerSentEvents, or a manual text/event-stream; heartbeats and connection limits."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/responses", "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events", "https://learn.microsoft.com/en-us/dotnet/api/system.net.serversentevents.sseparser"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-sent events

SSE streams messages from server to client over a single HTTP connection with content type `text/event-stream`; the browser side is the `EventSource` interface. Simpler than SignalR when you only push.

## Minimal API result
`TypedResults.ServerSentEvents` takes an `IAsyncEnumerable<SseItem<T>>` as its first parameter. In .NET an event message is an `SseItem<T>`, which may carry an event type, an ID and a data payload of type `T`.
```csharp
app.MapGet("/heartrate", (CancellationToken cancellationToken) =>
    TypedResults.ServerSentEvents(GetHeartRate(cancellationToken)));

static async IAsyncEnumerable<SseItem<int>> GetHeartRate(
    [EnumeratorCancellation] CancellationToken cancellationToken)
{
    while (!cancellationToken.IsCancellationRequested)
    {
        yield return new SseItem<int>(Random.Shared.Next(60, 100), eventType: "heartRate");
        await Task.Delay(2000, cancellationToken);
    }
}
```
Returning `IAsyncEnumerable<SseItem<T>>` directly from a handler compiles and runs, but it is serialized as a JSON array rather than an event stream; wrap it in `ServerSentEvents`. `System.Net.ServerSentEvents.SseParser` parses an event stream into `SseItem<T>` values (client side).

## Wire format (MDN)
- Each notification is a block of text terminated by a pair of newlines; send the `Content-Type: text/event-stream` header and `Cache-Control: no-cache`.
- Multiple `data:` lines in one event are concatenated with a newline between them.
- A line starting with a colon is a comment and is ignored; a server can send one periodically to keep the connection from timing out.
- Browser side: `new EventSource(url)`, with an `onerror` callback for failures.

## Gotchas
- When not used over HTTP/2, SSE is limited in the number of open connections per browser and domain (MDN cites 6); with HTTP/2 the maximum simultaneous streams is negotiated (default 100).
- Observe the request's `CancellationToken` so work stops when the client disconnects.

## Checked
Date: 2026-11-09. Confirmed on the cited pages: Minimal API `ServerSentEvents` result and `SseItem<T>` semantics, the JSON-array pitfall of returning `IAsyncEnumerable<SseItem<T>>` directly, `SseParser`, MDN wire format, comment keep-alive, HTTP/2 connection-limit warning. Removed unconfirmed claims: the .NET 10 version label, the manual Channel/`X-Accel-Buffering` sample, heartbeat interval, `Last-Event-ID` replay, auth and buffering/compression/output-caching remarks, curl verification.
Method: documentation only; no commands were run.
