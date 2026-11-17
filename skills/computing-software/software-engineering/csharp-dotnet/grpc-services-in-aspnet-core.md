---
id: computing-software.software-engineering.csharp-dotnet.grpc-services-in-aspnet-core
name: grpc-services-in-aspnet-core
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-realtime-rpc, grpc-aspnet-core, grpc, protobuf, grpc-client-factory, deadlines]
level: practitioner
status: draft
description: "Create gRPC services and clients on ASP.NET Core: proto contracts, streaming, deadlines and cancellation, status codes, client factory, interceptors, HTTP/2 and gRPC-Web notes."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/grpc/", "https://learn.microsoft.com/en-us/aspnet/core/grpc/clientfactory", "https://learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gRPC in ASP.NET Core

```proto
syntax = "proto3";
option csharp_namespace = "Shop.Grpc";
service Orders { rpc Get (GetRequest) returns (Order); rpc Watch (GetRequest) returns (stream Order); }
message GetRequest { int32 id = 1; }
message Order { int32 id = 1; string status = 2; }   // never reuse or renumber field tags; use reserved
```
```xml
<PackageReference Include="Grpc.AspNetCore" Version="2.*" />
<Protobuf Include="Protos\orders.proto" GrpcServices="Server" />   <!-- Client in the consuming project -->
```
```csharp
public class OrdersService : Orders.OrdersBase {
    public override async Task<Order> Get(GetRequest r, ServerCallContext ctx) =>
        await repo.Find(r.Id, ctx.CancellationToken) ?? throw new RpcException(new Status(StatusCode.NotFound, "no order"));
    public override async Task Watch(GetRequest r, IServerStreamWriter<Order> w, ServerCallContext ctx) {
        while (!ctx.CancellationToken.IsCancellationRequested) { await w.WriteAsync(await repo.Find(r.Id)); await Task.Delay(1000, ctx.CancellationToken); } }
}
builder.Services.AddGrpc(o => o.Interceptors.Add<LoggingInterceptor>());
app.MapGrpcService<OrdersService>();

builder.Services.AddGrpcClient<Orders.OrdersClient>(o => o.Address = new Uri("https://orders:5001"))
       .AddStandardResilienceHandler();                      // ok for unary
var reply = await client.GetAsync(new GetRequest { Id = 1 }, deadline: DateTime.UtcNow.AddSeconds(3), cancellationToken: ct);
```
## Rules
- Always set **deadlines** on clients; they propagate and the server sees cancellation.
- Map exceptions to `StatusCode` (don't leak details; `EnableDetailedErrors` only in dev).
- Needs HTTP/2: Kestrel HTTPS negotiates it; cleartext needs an HTTP/2-only endpoint. Browsers cannot speak gRPC: use gRPC-Web (`app.UseGrpcWeb()`) or JSON transcoding (`Microsoft.AspNetCore.Grpc.JsonTranscoding`).
- Reuse clients/channels (long-lived); one channel multiplexes many calls, but add `SocketsHttpHandler.EnableMultipleHttp2Connections` for heavy load.
- Load balancing: L4 balancers pin one connection; use client-side balancing or an L7 proxy.
- Auth: JWT bearer via metadata, `[Authorize]` on services.
- Compatible evolution: add fields, never change types; `reserved` removed tags.

## Verify
Integration test with `WebApplicationFactory` and `GrpcChannel.ForAddress(client.BaseAddress, new GrpcChannelOptions{HttpHandler = server.CreateHandler()})`; a call with a 1 ms deadline against a slow service returns `DeadlineExceeded`.
