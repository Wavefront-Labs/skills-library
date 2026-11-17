---
id: computing-software.software-engineering.csharp-dotnet.maui-shell-navigation-and-lifecycle
name: maui-shell-navigation-and-lifecycle
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-desktop-ui, maui-shell, dotnet-maui, navigation, dependency-injection, platform-specific]
level: practitioner
status: draft
description: "Structure a .NET MAUI app with Shell: routes and query parameters, DI-registered pages and view models, lifecycle, platform-specific code, permissions and secure storage."
sources: ["https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/", "https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/navigation", "https://learn.microsoft.com/en-us/dotnet/maui/platform-integration/storage/secure-storage"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MAUI Shell

```xml
<!-- AppShell.xaml -->
<Shell xmlns="http://schemas.microsoft.com/dotnet/2021/maui" xmlns:pages="clr-namespace:Shop.Pages">
  <TabBar>
    <ShellContent Title="Home" Icon="home.png" ContentTemplate="{DataTemplate pages:HomePage}" Route="home" />
    <ShellContent Title="Cart" Icon="cart.png" ContentTemplate="{DataTemplate pages:CartPage}" Route="cart" />
  </TabBar>
</Shell>
```
```csharp
// MauiProgram.cs
builder.Services.AddSingleton<IApi, Api>();
builder.Services.AddTransient<DetailPage>().AddTransient<DetailViewModel>();      // pages and view models resolved by DI
// AppShell.xaml.cs
Routing.RegisterRoute("detail", typeof(DetailPage));                               // non-visual-hierarchy routes

await Shell.Current.GoToAsync($"detail?id={id}");                                  // string query
await Shell.Current.GoToAsync("detail", new Dictionary<string, object> { ["Order"] = order });   // object parameters
await Shell.Current.GoToAsync("..");                                                // back

[QueryProperty(nameof(Order), "Order")]
public partial class DetailViewModel : ObservableObject { [ObservableProperty] Order? order; }
```
## Lifecycle and platform
- Page events: `Appearing`/`Disappearing`, `NavigatedTo`/`NavigatedFrom` (Shell); window lifecycle via `Window.Created/Activated/Stopped/Resumed`. Save state on `Stopped`: mobile OS may kill the app without warning.
- Platform code: `#if ANDROID` / `IOS` or partial classes in `Platforms/<os>/`; handlers customise native controls (`Microsoft.Maui.Handlers.EntryHandler.Mapper.AppendToMapping`).
- Permissions: `await Permissions.RequestAsync<Permissions.Camera>()`; declare them in `AndroidManifest.xml`/`Info.plist` (missing declarations fail silently or crash).
- Secrets: `SecureStorage.Default.SetAsync` (Keychain/Keystore), not `Preferences`. Connectivity: `Connectivity.Current`; HTTP with `IHttpClientFactory` and `https` only (iOS ATS, Android cleartext blocked).
- Performance: avoid deep layout nesting, use `CollectionView` with templates, compiled bindings (`x:DataType`), trimming/AOT settings (`PublishAot` is for iOS/MacCatalyst), image sizing.
- Tooling: `dotnet workload install maui`; Android emulators need HAXM/Hyper-V, iOS builds need a Mac. Hot Reload for XAML and C#.

## Gotchas
- Shell passes query values as strings; URL-encode and prefer object parameters.
- Pages registered as singleton retain state/leak: use transient.
- Routes must be unique; relative routes ("detail") only work from the right Shell context.
- Threading: UI updates on `MainThread`.

## Verify
Navigate forward/back in an emulator and confirm view-model state; a test with Appium or manual run on both Android and iOS for permission prompts and background/resume behaviour.
