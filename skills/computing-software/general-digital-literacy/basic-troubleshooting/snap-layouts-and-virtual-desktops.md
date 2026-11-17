---
id: computing-software.general-digital-literacy.basic-troubleshooting.snap-layouts-and-virtual-desktops
name: snap-layouts-and-virtual-desktops
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, os-settings, snap-layouts, virtual-desktops, mission-control, window-management, stage-manager]
level: intro
status: docs-checked
description: "Arrange windows side by side with Windows Snap and macOS tiling, and separate tasks onto virtual desktops (Task View, Mission Control Spaces) with keyboard shortcuts."
sources:
  - https://support.microsoft.com/en-us/windows/experience/snap-your-windows
  - https://support.microsoft.com/en-us/windows/how-to-multitask-in-windows-b4fa0333-98f8-ef43-e25c-06d4fb1d6960
  - https://support.apple.com/guide/mac-help/tile-app-windows-mchlef287e5d/mac
  - https://support.apple.com/guide/mac-help/mac-window-tiling-icons-keyboard-shortcuts-mchl9674d0b0/mac
  - https://support.apple.com/guide/mac-help/work-in-multiple-spaces-mh14112/mac
  - https://support.apple.com/guide/mac-help/use-stage-manager-mchl534ba392/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snap windows and virtual desktops

**Goal:** two or more apps neatly side by side, and separate desktops for different tasks.

## Windows Snap
- **Drag** a window to the left or right edge to snap to that half, to a corner for a quarter, or to the top to maximise vertically. Dropping a window at the top of the screen shows the **Snap bar** of layouts.
- **Snap layouts:** hover over the maximise or restore button, or press `Win+Z`, and pick a layout; **Snap Assist** then offers thumbnails of your other open windows to fill the rest.
- **Keyboard:** hold the Windows key and press an arrow key (Left or Right for halves, Up or Down for top or bottom positions); release when it is where you want.
- Drag the divider between snapped windows to resize them together.
- **Snap groups:** hover over a taskbar icon that belongs to a group to restore the whole group or one app; groups also show in Task View and the `Alt+Tab` view.
- Settings > System > **Multitasking** > *Snap windows* turns Snap on or off and lists options (Snap Assist, layouts on maximise hover, Snap bar, snapped windows in taskbar, Task View and Alt+Tab).

## Windows virtual desktops
- **Task View:** the taskbar button or `Win+Tab` > **New desktop**.
- Switch: pick a desktop in Task View, or `Win+Ctrl+Left` / `Win+Ctrl+Right`.
- Close a desktop: in Task View hover over it and use its close button; its open apps move to the next desktop.
- Move a window: drag it to a desktop thumbnail in Task View, or right-click it > **Move to**.
- `Alt+Tab` switches between open apps on the current desktop.

## Mac tiling
- Drag a window to the left or right edge, a corner, or the menu bar (fills the desktop). Hold **Option** while dragging toward an edge or corner for faster tiling.
- Hover over the green button for **Move & Resize** (halves and quarters) and **Fill & Arrange** layouts; or use the **Window** menu (Move & Resize, Center, Fill).
- Keyboard: `Fn-Control-Left/Right/Up/Down Arrow` for halves, `Fn-Control-F` fill, `Fn-Control-C` centre, `Fn-Control-R` return to the previous size.
- Dragging a window through the top edge opens Mission Control; turn off *Drag windows to top of screen to enter Mission Control* in Desktop & Dock settings if you do not want that. Edge and Option-drag tiling can be turned on or off (Apple's "Change window tiling settings on Mac").

## Mac Spaces
- Enter **Mission Control**, then click **+** in the Spaces bar to add a space (up to 16).
- Move between spaces: `Control+Left/Right Arrow`, a three- or four-finger trackpad swipe left or right (two fingers on a Magic Mouse), or the Spaces bar.
- Assign an app: Control-click its Dock icon > **Options** > *Assign To* > All Desktops, This Desktop, or None. An app used full screen gets its own space.
- **Stage Manager:** System Settings > Desktop & Dock > Desktop & Stage Manager, or Control Center. Recent apps sit on the left and the active window in the centre. If it will not turn on, enable *Displays have separate Spaces* in Desktop & Dock > Mission Control.

## Verify
- [ ] Two apps snapped or tiled side by side; a second desktop or space holds a different task and you can switch with the shortcut.

## Checked
Checked 2026-10-27 against Microsoft Support "Snap your windows" and "How to multitask in Windows", and the Apple Mac User Guide pages "Tile windows on Mac", "Mac window tiling icons & keyboard shortcuts", "Work in multiple spaces on Mac" and "Organize your Mac desktop with Stage Manager" (macOS 27 Golden Gate page set). Confirmed: all Snap gestures and settings, Win+Z, Win+Tab, Win+Ctrl+arrows, Mac tiling methods and Fn-Control shortcuts, Spaces limits and assignments, Stage Manager. Removed unconfirmed claims (Win+Ctrl+D and Win+Ctrl+F4, the Up/Down quarter and minimise behaviour, "Sequoia and later" tiling date, Ctrl+Up and F3 for Mission Control, wallpaper-per-desktop on Windows).
Method: documentation only; no commands were run.
