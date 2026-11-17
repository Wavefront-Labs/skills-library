---
id: computing-software.software-engineering.software-architecture.observer-pattern
name: observer-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, observer-pattern, gof, publish-subscribe, event-listeners, memory-leaks]
level: practitioner
status: verified
description: "Implement the Observer pattern safely: subscription API, push vs pull notification, unsubscribing to avoid leaks, re-entrancy, ordering and exceptions in listeners."
sources:
  - https://refactoring.guru/design-patterns/observer
  - https://en.wikipedia.org/wiki/Observer_pattern
  - https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observer pattern

**Intent (GoF):** define a one-to-many dependency so that when one object (subject) changes state, all its dependents (observers) are notified automatically.

## Shape
```typescript
type Listener<T> = (event: T) => void;

class Emitter<T> {
  private listeners = new Set<Listener<T>>();
  subscribe(fn: Listener<T>): () => void {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);        // return the unsubscribe handle
  }
  emit(event: T) {
    for (const fn of [...this.listeners]) {          // snapshot: listeners may unsubscribe mid-loop
      try { fn(event); } catch (err) { reportError(err); }   // one bad listener must not starve others
    }
  }
}
```
Platform versions: DOM `addEventListener`/`AbortSignal`, Node `EventEmitter`, .NET `event`/`IObservable<T>`, Java `PropertyChangeSupport`, Kotlin `Flow`, RxJS.

## Design decisions
- **Push vs pull:** push the changed data in the event (decoupled, but payload grows) or notify and let observers query the subject (simpler event, more coupling). Push immutable event objects.
- **Synchronous vs asynchronous:** sync delivery runs listeners on the emitter's thread and inside its call stack, so a slow listener slows the subject. Queue or post to an executor when listeners do I/O.
- **Ordering:** do not promise ordering between listeners; if one must run first, it is a pipeline, not observers.

## Failure modes
- **Lapsed listener leak:** the subject holds a strong reference to every observer, so a forgotten unsubscribe keeps screens, components, or whole object graphs alive. Always pair subscribe with unsubscribe (React `useEffect` cleanup, `AbortController`, `IDisposable`, `DisposableStore`). Weak references are a last resort.
- **Re-entrancy:** a listener that changes the subject triggers nested notifications; guard with a flag or queue events.
- **Notification storms:** batch or coalesce (debounce) when many fields change at once.
- **Iterating while mutating:** copy the listener collection before dispatch (see snapshot above) or use `CopyOnWriteArrayList`.

## Observer vs pub/sub vs mediator
Observer: observers know the subject. Pub/sub: a broker/topic decouples both sides (in-process event bus or a message broker). Mediator: a central object coordinates peers with logic of its own.

## Verify
- [ ] Heap snapshot after mounting/unmounting a component 100 times shows no retained listeners.
- [ ] A throwing listener does not stop other listeners and is reported.
