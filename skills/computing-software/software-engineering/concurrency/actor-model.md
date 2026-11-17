---
id: computing-software.software-engineering.concurrency.actor-model
name: actor-model
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, concurrency-models, actor-model, akka, erlang-otp, message-passing, supervision]
level: practitioner
status: draft
description: "Design with the actor model: isolated state, mailboxes and message passing, supervision trees, location transparency, and pitfalls like mailbox overflow and ask deadlocks."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://doc.akka.io/libraries/akka-core/current/typed/actors.html
  - https://learn.microsoft.com/en-us/dotnet/orleans/overview
  - https://getakka.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Actor model

An actor is a unit of computation with private state and a mailbox. Actors interact only by sending asynchronous messages. In response to a message an actor can: change its own state, send messages, and create actors. No shared memory means no locks.

## Implementations
- Erlang/Elixir (BEAM processes, OTP `gen_server`, supervisors) - the reference implementation.
- Akka (Scala/Java; BSL licence since 2.7) and Apache Pekko (Apache fork), Akka.NET.
- Microsoft Orleans (virtual actors/"grains", activated on demand), Dapr actors.
- Proto.Actor (Go/.NET), Ray actors (Python), Swift actors (language-level isolation, not distributed by default).

## Shape (Akka Typed, Java)
```java
public class Counter extends AbstractBehavior<Counter.Command> {
  public sealed interface Command {}
  public record Increment(int by) implements Command {}
  public record Get(ActorRef<Integer> replyTo) implements Command {}
  private int count = 0;                          // private, touched by one message at a time
  public static Behavior<Command> create() { return Behaviors.setup(Counter::new); }
  private Counter(ActorContext<Command> ctx) { super(ctx); }
  @Override public Receive<Command> createReceive() {
    return newReceiveBuilder()
      .onMessage(Increment.class, m -> { count += m.by(); return this; })
      .onMessage(Get.class, m -> { m.replyTo().tell(count); return this; })
      .build();
  }
}
```
Messages are immutable; replies go to an `ActorRef` included in the message.

## Supervision: let it crash
Parents supervise children. On failure, the supervisor restarts (fresh state), resumes, or stops the child, or escalates. Erlang strategies: `one_for_one`, `one_for_all`, `rest_for_one`, with restart intensity limits (max N restarts in T seconds) to prevent restart loops. Design so state that must survive a crash is persisted (event-sourced actors: Akka Persistence, Orleans grain storage).

## Good fits
Many independent stateful entities (devices, game sessions, user sessions, shopping carts), telecom-style systems needing fault isolation, sharded in-memory state across a cluster (Akka Cluster Sharding, Orleans).

## Pitfalls
- **Mailbox growth:** a slow actor with fast senders grows its mailbox unbounded until OOM. Use bounded mailboxes, backpressure (Akka Streams), or work-pulling.
- **Ask pattern deadlocks/timeouts:** actor A asks B, B asks A, both wait. Prefer tell with reply-to; set ask timeouts.
- **Blocking inside actors** starves the dispatcher threads; run blocking I/O on a dedicated dispatcher.
- Message ordering is guaranteed only per sender-receiver pair; delivery is at-most-once by default across the network.
- Hot actors become bottlenecks (one actor per global resource is a single-threaded queue).
- Debugging asynchronous flows needs correlation ids in messages and tracing.

## Verify
- [ ] Actor tests with a test kit (Akka `ActorTestKit`/`TestProbe`, Orleans `TestCluster`) cover message protocols and crash/restart behaviour.
- [ ] Mailbox size metrics and alerts per actor type.
