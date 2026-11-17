---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-focus-keyboard-navigation
name: wpf-focus-keyboard-navigation
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-focus-keyboard-navigation, wpf-commands-input, wpf, commands, routedcommand, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Set initial focus in the Loaded handler and use Keyboard.Focus, MoveFocus and dialog default/cancel buttons."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/focus-overview
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/windows/dialog-boxes-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF focus and keyboard navigation

**Goal:** keyboard-usable dialogs.

```xml
<StackPanel KeyboardNavigation.TabNavigation="Cycle">
  <TextBox x:Name="box"/>
  <Button IsDefault="True" Content="OK"/>
  <Button IsCancel="True" Content="Cancel"/>
</StackPanel>
```

```csharp
// in the window's Loaded handler
Keyboard.Focus(box);
box.MoveFocus(new TraversalRequest(FocusNavigationDirection.Next));
```

**Gotcha:** The element to receive initial focus must be in the visual tree of the initial window and have `Focusable` and `IsVisible` true; the recommended place to set it is the `Loaded` event handler (a Dispatcher callback also works). Keyboard focus (Keyboard class) and logical focus (FocusManager) are different concepts.

## Verify
- Tab, Enter and Escape behave correctly with no mouse.

## Checked

2026-11-03. Confirmed in the WPF focus overview (keyboard vs logical focus, `KeyboardNavigation.TabNavigation`, `Keyboard.Focus`, `MoveFocus` with `TraversalRequest`, initial focus rules and Loaded handler) and the dialog boxes overview (`IsDefault`, `IsCancel`). Removed: TabIndex usage and the FocusManager.FocusedElement self-binding, which those pages do not confirm.

Method: documentation only; no commands were run.
