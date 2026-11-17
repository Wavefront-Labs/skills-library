---
id: computing-software.general-digital-literacy.basic-troubleshooting.taskbar-start-menu-and-dock
name: taskbar-start-menu-and-dock
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-os-settings, taskbar-settings, start-menu, dock]
level: intro
status: draft
description: "Pin and unpin apps, move or auto-hide the taskbar or Dock, tidy the Start menu and system tray, and recover a missing or frozen taskbar on Windows and Mac."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Taskbar, Start menu and Dock

## Windows 11 taskbar
- Pin: right-click an app (Start or open window) > **Pin to taskbar**. Unpin: right-click > *Unpin*.
- Settings > Personalisation > **Taskbar**: hide Search/Task view/Widgets/Chat buttons, *Taskbar behaviours* > alignment (Left/Center), **Automatically hide the taskbar**, show on all displays, *Combine taskbar buttons*.
- System tray icons: *Other system tray icons* to choose which appear beside the clock.
- Start menu: right-click an app > *Pin to Start*, drag to reorder, make folders by dropping one icon on another; Settings > Personalisation > Start controls recommendations and layout.

## Mac Dock
- Drag an app into the Dock to keep it; drag out until "Remove" appears to remove. Right-click > *Options > Keep in Dock*.
- System Settings > **Desktop & Dock**: size, magnification, position (left/bottom/right), *Automatically hide and show the Dock*, *Show suggested and recent apps*.
- Menu bar items: Cmd-drag to rearrange; Control Centre settings choose which show.

## Recovery
- Windows taskbar frozen or missing: Ctrl+Shift+Esc > Task Manager > *Windows Explorer* > **Restart**. Still broken: sign out and in; run `sfc /scannow` in an admin terminal.
- Taskbar on the wrong screen: Settings > System > Display > select the monitor > *Make this my main display*.
- Mac Dock unresponsive: Terminal `killall Dock`.

## Verify
- [ ] Daily apps are one click away and the taskbar/Dock behaves the same after restart.
