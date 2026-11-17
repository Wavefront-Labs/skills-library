---
id: computing-software.software-engineering.desktop-ui-frameworks.maui-handlers-customisation
name: maui-handlers-customisation
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [maui-handlers-customisation, maui-desktop, maui, dotnet, winui3, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Customise native controls with handler Mapper AppendToMapping and the PlatformView property."
sources:
  - https://learn.microsoft.com/en-us/dotnet/maui/user-interface/handlers/customize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MAUI handler customisation

**Goal:** platform-specific look and behaviour.

```csharp
Microsoft.Maui.Handlers.EntryHandler.Mapper.AppendToMapping("MyCustomization", (handler, view) => {
#if WINDOWS
    handler.PlatformView.GotFocus += (s, e) => handler.PlatformView.SelectAll();
#endif
});
```

**Gotcha:** Handlers are global: customising a handler customises every control of that type in the app. To target one instance, subclass the control and modify the handler only when the control is of the subclass. `PrependToMapping` runs before and `AppendToMapping` after the control's own mappings, and `ModifyMapping` changes an existing mapping.

## Verify
- Every Entry on Windows selects its text on focus; other platforms are unchanged.

## Checked

2026-11-03. Confirmed in the .NET MAUI handler customisation page: `Mapper.AppendToMapping/PrependToMapping/ModifyMapping`, `PlatformView` (a `TextBox` on Windows), the `GotFocus`/`SelectAll` example, and handlers being global with the subclass technique for one instance. Removed: the `BorderThickness` example and the "register once at startup" claim, which that page does not state.

Method: documentation only; no commands were run.
