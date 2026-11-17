---
id: computing-software.software-engineering.csharp-dotnet.idempotency-keys-and-outbox-pattern
name: idempotency-keys-and-outbox-pattern
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-resilience, idempotency-keys, outbox-pattern, at-least-once, inbox-pattern, ef-core]
level: advanced
status: draft
description: "Make .NET services safe under retries: idempotency-key endpoints with unique constraints, and the transactional outbox with EF Core and a dispatcher, plus inbox deduplication for consumers."
sources: ["https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults", "https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer", "https://microservices.io/patterns/data/transactional-outbox.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Idempotency keys and the outbox

Retries (Polly, brokers, clients) deliver duplicates; correctness needs idempotent handlers and reliable publishing.

## Idempotency key on POST
```csharp
app.MapPost("/payments", async (HttpRequest req, PayDto dto, AppDb db) =>
{
    var key = req.Headers["Idempotency-Key"].ToString();
    if (key.Length is 0 or > 100) return Results.BadRequest();
    var existing = await db.Idempotency.FindAsync(key);
    if (existing is not null) return Results.Json(existing.Response, statusCode: existing.StatusCode);   // replay stored result
    try {
        await using var tx = await db.Database.BeginTransactionAsync();
        var pay = Charge(dto); db.Payments.Add(pay);
        db.Idempotency.Add(new IdempotencyRecord(key, 201, pay.ToDto()));         // PK = key: unique constraint is the real guard
        await db.SaveChangesAsync(); await tx.CommitAsync();
        return Results.Created($"/payments/{pay.Id}", pay.ToDto());
    } catch (DbUpdateException) { /* concurrent duplicate: reload and return the stored response */ }
    return Results.Conflict();
});
```
Scope keys per caller, store a request hash to reject key reuse with different bodies (422), expire records (24-72 h). The unique index, not a read-then-write check, makes it race-safe.

## Transactional outbox
Write the business change and an `OutboxMessage` row in the **same** DB transaction; a background dispatcher publishes and marks them sent. Avoids the dual-write problem (DB committed, broker publish lost).
```csharp
db.Orders.Add(order);
db.Outbox.Add(new OutboxMessage { Id = Guid.NewGuid(), Type = "OrderPlaced", Payload = JsonSerializer.Serialize(evt), OccurredAt = clock.GetUtcNow() });
await db.SaveChangesAsync();                                       // atomic

// dispatcher (BackgroundService)
var batch = await db.Outbox.Where(m => m.SentAt == null).OrderBy(m => m.OccurredAt).Take(50).ToListAsync(ct);
foreach (var m in batch) { await bus.PublishAsync(m, ct); m.SentAt = clock.GetUtcNow(); }
await db.SaveChangesAsync(ct);
```
Delivery is **at least once** (crash between publish and mark = resend), so consumers dedupe with an inbox table keyed by message id. Multiple dispatcher instances: use `SELECT ... FOR UPDATE SKIP LOCKED` / `UPDLOCK, READPAST`, or MassTransit/Wolverine/NServiceBus built-in outbox.

## Gotchas
- Outbox table growth: purge sent rows.
- Ordering is per partition/aggregate only.
- Non-idempotent side effects (emails) need their own dedupe key.
- HTTP `PUT`/`DELETE` are naturally idempotent; design POST carefully.

## Verify
Fire the same request 20 times concurrently: one payment row, identical responses; kill the dispatcher after publish and see the message redelivered and ignored by the consumer inbox.
