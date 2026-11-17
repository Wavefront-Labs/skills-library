---
id: computing-software.software-engineering.csharp-dotnet.delegates-events-and-lambdas
name: delegates-events-and-lambdas
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-delegates, csharp-events, lambdas, func-action, event-handler-leaks, closures, csharp-delegates-events, local-functions]
level: practitioner
status: docs-checked
description: "Use C# delegates, events and lambdas correctly: Func/Action, the event pattern, thread-safe raising, unsubscribing to avoid leaks, closure capture gotchas and static lambdas."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/delegates-overview", "https://learn.microsoft.com/en-us/dotnet/csharp/events-overview", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Delegates, events and lambdas

**Goal:** callbacks and notifications that don't leak memory, race, or capture the
wrong variable.

## Delegates
```csharp
Func<int, int, int> add = (a, b) => a + b;
Action<string> log = Console.WriteLine;          // method group conversion
Predicate<User> isActive = u => u.Active;
public delegate decimal PriceRule(Order order);  // named delegate when the name documents intent
```
Delegates are multicast: `+=` combines; invoking a multicast `Func` returns only the last
result. Prefer `Func`/`Action` over custom delegate types unless naming helps.

## The event pattern
```csharp
public sealed class OrderService
{
    public event EventHandler<OrderPlacedEventArgs>? OrderPlaced;

    private void OnOrderPlaced(Order o) =>
        OrderPlaced?.Invoke(this, new OrderPlacedEventArgs(o));
}
public sealed record OrderPlacedEventArgs(Order Order);
```
`event` restricts outsiders to `+=`/`-=`; only the declaring class can invoke or reset it.

## Subscriber leaks
The publisher holds a reference to every subscriber's target object. A short-lived view
model subscribing to a long-lived service's event is never collected until it unsubscribes.
```csharp
service.OrderPlaced += Handler;
// in Dispose:
service.OrderPlaced -= Handler;          // must be the same method; a lambda cannot be removed unless stored
```
Store lambdas in a field if you need to unsubscribe. Alternatives: weak event managers (WPF),
`IObservable<T>` with disposable subscriptions, or a message bus.

## Exceptions in handlers
One throwing handler stops later handlers. For critical fan-out, iterate
`GetInvocationList()` and catch per handler. Async handlers: `async void` event handlers
are the one acceptable use of `async void`; wrap their bodies in try/catch.

## Closures
```csharp
var actions = new List<Action>();
for (int i = 0; i < 3; i++) actions.Add(() => Console.Write(i));   // prints 333: one shared i
foreach (var x in new[] { 0, 1, 2 }) actions.Add(() => Console.Write(x));   // 012 (C# 5+ foreach fix)
```
Copy to a local inside `for` loops. Captured variables are hoisted into a heap-allocated
closure object - avoid capturing in hot paths.
```csharp
cache.GetOrAdd(key, static (k, state) => Load(k, state), state);   // static lambda: compiler forbids captures
```

## Checked
2026-10-28: Confirmed in the delegates overview, events overview and lambda expressions reference: multicast delegates, event += / -= restriction, static lambdas cannot capture. Removed two inline comments about null-conditional invocation and EventArgs that no fetched page states.
Method: documentation only; no commands were run.

## Verify
- [ ] Every `+=` on a longer-lived publisher has a matching `-=` in Dispose.
- [ ] Hot-path lambdas are `static` or use state overloads (no hidden allocations).
