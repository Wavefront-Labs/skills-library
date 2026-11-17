---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-mvvm-messenger-di
name: wpf-mvvm-messenger-di
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-mvvm-messenger-di, wpf-mvvm, wpf, mvvm, communitytoolkit, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Decouple view models with WeakReferenceMessenger and resolve services from an IServiceProvider."
sources:
  - https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/messenger
  - https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/ioc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF messenger and dependency injection

**Goal:** loosely-coupled WPF app.

```csharp
// register (r is the recipient; avoids capturing "this")
WeakReferenceMessenger.Default.Register<UserChangedMessage>(this, (r, m) => ((MainViewModel)r).User = m.Value);
// send from another module
WeakReferenceMessenger.Default.Send(new UserChangedMessage(user));
WeakReferenceMessenger.Default.UnregisterAll(this);

// services: build an IServiceProvider once at startup (Microsoft.Extensions.DependencyInjection)
var services = new ServiceCollection();
services.AddSingleton<IFilesService, FilesService>();
IServiceProvider provider = services.BuildServiceProvider();
var files = provider.GetService<IFilesService>();
```

**Gotcha:** The MVVM Toolkit has no built-in DI; it relies on `Microsoft.Extensions.DependencyInjection`. Messages can also be received by implementing `IRecipient<TMessage>` and calling `Register(this)`. Unregister recipients when they are no longer needed.

## Verify
- Messages reach subscribers and services resolve through constructor injection.

## Checked

2026-11-03. Confirmed in the MVVM Toolkit Messenger and Ioc pages: `WeakReferenceMessenger.Default.Register/Send/UnregisterAll`, the `(r, m)` handler form, `IRecipient<TMessage>`, `ServiceCollection.AddSingleton`, `BuildServiceProvider`, and that DI comes from Microsoft.Extensions.DependencyInjection. Removed: the generic Host builder code and the StartupUri advice, which those pages do not cover.

Method: documentation only; no commands were run.
