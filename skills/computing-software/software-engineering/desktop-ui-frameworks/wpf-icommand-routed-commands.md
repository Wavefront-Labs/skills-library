---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-icommand-routed-commands
name: wpf-icommand-routed-commands
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-icommand-routed-commands, wpf-commands-input, wpf, commands, routedcommand, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Wire commands with CommandBinding and KeyBinding and refresh state with CommandManager.InvalidateRequerySuggested."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/commanding-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF ICommand and RoutedCommand

**Goal:** keyboard shortcuts, menus and buttons from one command.

```xml
<Window.CommandBindings>
  <CommandBinding Command="ApplicationCommands.Save" Executed="OnSave" CanExecute="CanSave"/>
</Window.CommandBindings>
<MenuItem Header="_Save" Command="ApplicationCommands.Save"/>
```

**Gotcha:** `CommandManager` raises `RequerySuggested` for conditions it can detect; call `CommandManager.InvalidateRequerySuggested` to force it when a condition that enables or disables the command changes elsewhere.

## Verify
- The menu and toolbar items enable and disable together.

## Checked

2026-11-03. Confirmed in the WPF commanding overview: `CommandBinding`, `KeyBinding`, `CommandManager`, and `InvalidateRequerySuggested` forcing the `RequerySuggested` event. Removed: the Window.InputBindings Ctrl+K sample and the claim that CanExecute is re-queried on input events, which are not stated in that page.

Method: documentation only; no commands were run.
