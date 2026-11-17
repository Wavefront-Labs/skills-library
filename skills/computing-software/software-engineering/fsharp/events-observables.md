---
id: computing-software.software-engineering.fsharp.events-observables
name: events-observables
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, events-observables, fsharp-concurrency, event-module, observable-module]
level: practitioner
status: draft
description: "Create and combine first-class F# events and observables with Event, Observable and CLIEvent."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Events and observables
**Goal:** model event streams.

```fsharp
let evt = Event<string>()
let stream = evt.Publish
stream.Add(fun s -> printfn "got %s" s)
evt.Trigger "hello"

let evens =
    Event<int>().Publish
    |> Event.filter (fun n -> n % 2 = 0)
    |> Event.map (fun n -> n * n)

type Button() =
    let click = Event<unit>()
    [<CLIEvent>]
    member _.Click = click.Publish        // visible as a .NET event
    member _.Fire() = click.Trigger()

let obs = Observable.map ((+) 1) (Event<int>().Publish)
use sub = obs.Subscribe(fun v -> printfn "%d" v)
```
- `Event<'T>` has `Publish` (IEvent) and `Trigger`; `Event.map/filter/merge/choose/scan/pairwise` compose.
- `[<CLIEvent>]` exposes standard `+=` events for C#.
- `Observable` module works on `IObservable<'T>`; subscribing returns an `IDisposable` to unsubscribe.
- For richer Rx operators use System.Reactive (third party).

## Gotchas
- Event handlers hold references; unsubscribe to avoid leaks.
- Event triggers run subscribers synchronously on the caller thread.

## Self-check
Trigger 1..4 on the `evens` stream and see only squares of 2 and 4.
