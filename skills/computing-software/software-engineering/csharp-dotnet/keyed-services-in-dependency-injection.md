---
id: computing-software.software-engineering.csharp-dotnet.keyed-services-in-dependency-injection
name: keyed-services-in-dependency-injection
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-generic-host, keyed-services, dependency-injection, fromkeyedservices, service-lifetimes, decorators]
level: practitioner
status: docs-checked
description: "Register and resolve multiple implementations by key in .NET DI with AddKeyedSingleton and [FromKeyedServices]; AnyKey fallbacks and scope validation."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#keyed-services", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection#keyed-services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyed services

## Register and resolve
```csharp
services.AddKeyedSingleton<IPaymentGateway, StripeGateway>("stripe");
services.AddKeyedScoped<IPaymentGateway, AdyenGateway>("adyen");
services.AddKeyedSingleton<ICache>(KeyedService.AnyKey, (sp, key) => new DefaultCache(key?.ToString() ?? "unknown"));

// constructor
public class Checkout([FromKeyedServices("stripe")] IPaymentGateway gw) { }

// manual
var gw = sp.GetRequiredKeyedService<IPaymentGateway>("stripe");
```

## What the docs state (dotnet DI overview page)
- You can register multiple services with different keys and look them up by key, using the keyed overloads of the registration methods.
- The key is not limited to `string`; it can be any `object` whose type correctly implements `Equals`.
- `[FromKeyedServices(key)]` on a constructor parameter selects the keyed service.
- `KeyedService.AnyKey` registered as a fallback matches any key without its own registration; a specific key registration wins for that key.
- `GetKeyedServices<T>(KeyedService.AnyKey)` returns only the services registered with specific keys, not the AnyKey fallback.
- From .NET 10, calling the singular `GetKeyedService()` with `KeyedService.AnyKey` throws `InvalidOperationException`.
- Scope validation: in the Development environment, `Host.CreateApplicationBuilder` checks that scoped services are not resolved from the root provider or injected into singletons. A BackgroundService needing scoped services should inject `IServiceScopeFactory` and create a scope.

## Practitioner notes (not covered by the dotnet page; the ASP.NET Core DI page source was not re-read)
- Prefer constants or enums over string literals for keys.
- For runtime choices driven by request data, an injected resolver/factory is usually clearer than using the container as a service locator.
- Missing keyed registrations surface at resolution time; add a startup smoke test and consider `ValidateOnBuild`/`ValidateScopes`.

## Verify
A test host builds, resolves each key, and has scope validation enabled.

## Checked
Method: 2026-11-08 docs-only read of the Keyed services section of the dotnet DI overview page. The ASP.NET Core DI page was not fetched. Removed unsupported claims: minimal-API and Blazor `[Inject(Key=...)]` usage, the .NET 8 vs 9 null-key behaviour, "AnyKey transient lifetime" example, third-party container (Autofac, Lamar) remarks, `IKeyedServiceProvider` package note and AOT remark. Added the .NET 10 AnyKey behaviour.
