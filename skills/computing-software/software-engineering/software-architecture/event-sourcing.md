---
id: computing-software.software-engineering.software-architecture.event-sourcing
name: event-sourcing
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, distributed-data, event-sourcing, event-store, snapshots, upcasting, projections]
level: practitioner
status: verified
description: "Implement event sourcing: append-only event streams per aggregate, rehydration, optimistic concurrency on stream version, snapshots, schema evolution and GDPR erasure."
sources:
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
  - https://developers.eventstore.com/
  - https://martendb.io/events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event sourcing

Store the state of an entity as the sequence of events that changed it, instead of the current state. Current state = fold over events.

## Core mechanics
```python
def load(stream_id):
    events = store.read_stream(stream_id)          # ordered, append-only
    account = Account()
    for e in events: account.apply(e)               # pure state transitions
    return account, len(events)                      # version = event count / last position

def handle_withdraw(cmd):
    account, version = load(cmd.account_id)
    new_events = account.withdraw(cmd.amount)        # decides; raises if invariant broken
    store.append(cmd.account_id, new_events, expected_version=version)   # optimistic concurrency
```
- `apply` methods never fail and never have side effects (they replay history).
- Command methods validate against current state and return new events.
- `expected_version` makes concurrent writers conflict instead of silently interleaving (EventStoreDB, now KurrentDB, takes an expected revision / stream state on append and errors if the stream differs; Marten has `Append(streamId, expectedVersion, events)` (needs `EventAppendMode.Rich` in Marten 9) and `AppendOptimistic`; Axon; or a `UNIQUE(stream_id, version)` constraint in a relational store; the sketch above was run against SQLite with that constraint and the second concurrent writer got an integrity error).

## Snapshots
Long streams load slowly. Store a snapshot every N events (or on schedule) with its version; load snapshot then events after it. Snapshots are a cache - they can be deleted and rebuilt. Often better: keep streams short by modelling lifecycle (close the account-year stream, start a new one).

## Schema evolution
Events are stored forever, so:
- Only additive changes to existing event types where possible; consumers tolerate unknown fields.
- **Upcasting:** transform old event versions into the current shape on read (`v1 AccountOpened{name}` -> `v2{first_name, last_name}`).
- New event type for a genuinely new meaning; never rewrite history in place except via a deliberate copy-transform migration.

## Projections and queries
You cannot query "all accounts with balance > X" from streams; build projections (CQRS read models). Subscriptions (catch-up, persistent) feed projections with checkpointing.

## Hard parts
- **Personal data and GDPR erasure:** encrypt personal fields per subject and delete the key (crypto-shredding), or keep PII out of events and reference it.
- Fixing bugs means compensating events, not editing old ones.
- Event design is a public contract inside the context - name events in domain language.
- Not for every aggregate: use it where audit history, temporal queries ("what was the state on 1 March"), or complex state transitions justify the cost.

## Verify
- [ ] Given-when-then tests: given past events, when command, then expected new events (or error).
- [ ] Concurrent appends with the same expected version: exactly one succeeds.
- [ ] Old-version events load correctly through upcasters.
