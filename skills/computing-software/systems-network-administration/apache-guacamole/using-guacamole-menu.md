---
id: computing-software.systems-network-administration.apache-guacamole.using-guacamole-menu
name: using-guacamole-menu
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, guacamole-menu, ctrl-alt-shift, clipboard, on-screen-keyboard, text-input, touch-input, zoom, user-settings, file-browser]
level: intro
status: docs-checked
description: "Use the in-session Guacamole menu (Ctrl+Alt+Shift): clipboard, file browser, on-screen keyboard, input modes, zoom and Settings."
sources:
  - https://guacamole.apache.org/doc/gug/using-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The Guacamole menu and settings

Open or close the menu with **Ctrl+Alt+Shift** (touch: swipe from the left edge). It holds the clipboard, connection switcher, Home, Disconnect, Share, file transfer, zoom, input modes and on-screen keyboard.

- Home screen: Filter field narrows by connection name; thumbnails of recent connections (default 6, adjustable in Settings). One accessible connection opens directly.
- User menu (top right): Home, Settings, Logout (closes all connections).
- Clipboard: text area at the top of the menu, hidden until clicked; edits sync to the remote clipboard. With the browser clipboard API enabled it syncs automatically.
- File transfer (VNC, RDP, SSH): drag files into the window, or use the menu's file browser (double-click to download, Upload Files). RDP drive Download folder auto-downloads. See apache-guacamole.sftp-file-transfer.
- On-screen keyboard: sends Ctrl+Alt+Del, Alt+Tab, etc. without the local OS intercepting them.
- Text input mode: for mobile keyboards and IMEs (Chinese, Japanese, Korean).
- Mouse emulation: absolute (default on touchscreens; tap = left click, press-and-hold = right click) or relative/touchpad (two-finger tap right click, three-finger tap middle, two-finger drag scroll).
- Zoom: pinch, or menu "-" / "+" in 10% steps.

Settings page: display language (English, Dutch, French, German, Italian, Russian), change password (if permitted), default keyboard/mouse mode. Preferences are stored per browser.

Verify: Ctrl+Alt+Shift toggles the menu and pasted text appears on the remote desktop.

## Checked

2026-11-08. Read the whole of the Guacamole user interface chapter (using-guacamole.html) and confirmed the menu shortcut and swipe gesture, clipboard behaviour, file browser and RDP Download folder, on-screen keyboard, text input and IME note, mouse emulation gestures, 10% zoom steps, language list, per-browser preferences and the default of 6 recent connections. Nothing removed. The cross-reference to the SFTP skill was not checked against any page.
Method: documentation only; no commands were run.
