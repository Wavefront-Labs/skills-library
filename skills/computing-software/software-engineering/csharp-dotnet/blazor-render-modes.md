---
id: computing-software.software-engineering.csharp-dotnet.blazor-render-modes
name: blazor-render-modes
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, blazor, render-modes, prerendering, interactive-server, webassembly, blazor-web-app]
level: practitioner
status: docs-checked
description: "Choose and apply Blazor render modes in Blazor Web Apps: static SSR, Interactive Server, WebAssembly, Auto, per-component or global, prerendering and parameter limits."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/blazor/components/render-modes", "https://learn.microsoft.com/en-us/aspnet/core/blazor/components/prerender", "https://learn.microsoft.com/en-us/aspnet/core/blazor/components/lifecycle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blazor render modes (Blazor Web Apps, .NET 8+)

Every component in a Blazor Web App adopts a render mode that decides where it renders and whether it is interactive. Apply one with the `@rendermode` directive on the component instance or on the component definition. Standalone Blazor WebAssembly apps have no render modes.

| Mode | Render location | Interactive |
|---|---|---|
| Static Server (static SSR) | server | no |
| InteractiveServer | server (interactive SSR, Blazor Server) | yes |
| InteractiveWebAssembly | client (CSR, Blazor WebAssembly) | yes |
| InteractiveAuto | server first, then client on later visits once the Blazor bundle is downloaded | yes |

```razor
<Dialog @rendermode="InteractiveServer" />                    @* on a component instance *@
@rendermode InteractiveServer                                 @* on a component definition *@
@rendermode @(new InteractiveServerRenderMode(prerender: false))
<Routes @rendermode="InteractiveServer" />                    @* globally, in App.razor *@
```

## Enabling the modes (Program file)
```csharp
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode();
```
Add only the calls for the modes you use. Components that use the Interactive WebAssembly render mode must be built from the client project (the `.Client` project the template adds) so they are in the downloaded bundle.

## Key behaviours
- **Prerendering** is enabled by default for interactive components, so components render twice (once to prerender, once to set up interactivity) and `OnInitializedAsync` runs twice. To preserve state across the two runs see the "prerendered state persistence" article.
- Turn prerendering off per component with `new InteractiveServerRenderMode(prerender: false)` (likewise `InteractiveWebAssemblyRenderMode` and `InteractiveAutoRenderMode`), or on `<Routes>` and `<HeadOutlet>`.
- A component in the `.Client` project is also prerendered on the server, which has no access to client-side Blazor services: injecting one (for example `IWebAssemblyHostEnvironment`) fails during prerendering with a "no registered service" error. Design such components to run on both server and client.
- JS interop is not possible while prerendering; do JS interop calls in `OnAfterRender`/`OnAfterRenderAsync`, which run after the component has rendered interactively (`firstRender` tells you whether it is the first render).
- Parameters passed from a static parent to an interactive child must be JSON serializable: you cannot pass a `RenderFragment` or child content (a runtime `InvalidOperationException` results).

## Verify
- [ ] Each interactive page declares its render mode (or inherits a global one) and the matching `Add*Components` and `Add*RenderMode` calls exist.
- [ ] Data loaded in `OnInitializedAsync` is not fetched twice visibly in the logs when prerendering is on.

## Checked
2026-11-09. Confirmed on the Learn pages for render modes (mode table, @rendermode on instance and definition, Routes global mode, Program file calls, client-project requirement, serializable parameters and the RenderFragment error), prerendering (render twice, prerender: false forms, .Client service injection error) and component lifecycle (OnInitializedAsync called twice when prerendering, no JS interop while prerendering, OnAfterRender and firstRender). The cached render-modes page was the .NET 9 version; the .NET 10 page was not read. Removed as not on those pages: StreamRendering, PersistentComponentState and .NET 10 persistence attribute names, circuit retention settings, scale and download-cost remarks, secrets advice, static SSR @onclick note, AuthenticationStateProvider note, AddAdditionalAssemblies and network-tab check.
Method: documentation only; no commands were run.
