---
id: computing-software.software-engineering.software-architecture.service-locator-vs-dependency-injection
name: service-locator-vs-dependency-injection
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, service-locator, dependency-injection, inversion-of-control, testability]
level: practitioner
status: docs-checked
description: "Compare Service Locator with dependency injection, recognise the locator anti-pattern in DI containers, and refactor hidden dependencies into constructor injection."
sources: ["https://martinfowler.com/articles/injection.html", "https://blog.ploeh.dk/2010/02/03/ServiceLocatorisanAnti-Pattern/", "https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Locator vs dependency injection

## The two
- **Service Locator**: an object that knows how to get hold of all the services an application might need; code asks it when it needs one. The locator itself still has to be given to the class.
- **Dependency injection**: dependencies are passed in. Fowler names three styles: constructor, setter and interface injection.

## The positions
- Fowler: the key difference is that with a locator every user of a service depends on the locator, which can hide dependencies on implementations but must be visible; the choice depends on whether that dependency is a problem. It matters most for code written to be used in applications outside the author's control. A locator need not be untestable: it can be a registry (not a singleton) holding test implementations. He starts with constructor injection and switches to setter injection if problems appear (long constructors, for instance). He also notes inversion of control is hard to debug, so avoid it unless it justifies itself.
- Seemann: Service Locator is an anti-pattern. It hides a class's dependencies, causing run-time instead of compile-time errors, and makes it unclear when a change is breaking. Consumers cannot tell from the constructor which services a class needs (a missing registration surfaces as a `KeyNotFoundException`), and a static locator store has to be reset after each unit test. With constructor injection the compiler helps both consumers and producers.
- Microsoft (.NET DI guidelines): avoid the service locator pattern, for example do not call `GetService` to obtain an instance when DI can supply it. Injecting a factory that resolves dependencies at runtime is another variation to avoid, because both mix inversion-of-control strategies. Avoid static access to services (for example capturing `IApplicationBuilder.ApplicationServices` in a static field) and avoid `BuildServiceProvider` while configuring services; use an overload that gives you the `IServiceProvider`.

## Frameworks that cannot do constructor injection
Seemann's comment thread: where the framework creates objects without constructor hooks (for example ASP.NET pages), the composition root has to move into each such object; this keeps container use to an absolute minimum and is not the locator anti-pattern. Do the lookup at that boundary only.

## Refactoring a locator call
1. Find the locator calls in a class.
2. Add a constructor parameter for each dependency, assign to a field and replace the calls.
3. Register the class in the composition root so callers get it by injection.
4. Repeat outward until only the composition root touches the container.
Too many constructor parameters afterwards is a design signal to examine, not a reason to go back to a locator.

## Checked
2026-11-08. Confirmed against Fowler's "Inversion of Control Containers and the Dependency Injection pattern" (read by keyword search of the page, key passages only), Seemann's "Service Locator is an Anti-Pattern" and Microsoft's .NET dependency injection guidelines. Removed or reworded: the claim that Fowler regards a locator as worse, the Func/Provider factory step (Microsoft lists runtime-resolving factories as a variation to avoid), the "when acceptable" list beyond Seemann's framework case, and the parallel-test claim.
Method: documentation only; no commands were run.
