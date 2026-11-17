---
id: computing-software.systems-network-administration.linux.input-methods-ibus-and-fcitx5
name: input-methods-ibus-and-fcitx5
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, input-method, ibus, fcitx5, cjk-input, im-module, wayland-input]
level: practitioner
status: docs-checked
description: "Set up input methods on Linux desktops with IBus or Fcitx5: environment variables, Wayland versus X11, and fixing Chromium and Electron apps that ignore the IM."
sources:
  - https://wiki.archlinux.org/title/Input_method
  - https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland
  - https://github.com/ibus/ibus/wiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Input methods (IBus/Fcitx5)

An input method framework (IMF) turns keystrokes into characters that a keyboard layout alone can't: Chinese pinyin, Japanese kana-kanji, Korean hangul and so on. Install one framework as the active IMF to avoid conflicts.

## Environment variables
X11 and XWayland applications read:
```
GTK_IM_MODULE=fcitx    # or ibus
QT_IM_MODULE=fcitx     # or ibus
XMODIFIERS=@im=fcitx   # or @im=ibus
```
To bypass the IMF for GTK and Qt, set `GTK_IM_MODULE=gtk-im-context-simple` and `QT_IM_MODULE=simple`.

## Wayland with Fcitx5
- `XMODIFIERS` is still needed for X11 applications under XWayland.
- Ideal GTK setup: do not set `GTK_IM_MODULE`, so GTK3 and GTK4 use the text-input-v3 protocol natively
  (`GTK_IM_MODULE=wayland` or `fcitx` both also work).
- For Qt, KWin supports text-input-v2; on other compositors use `QT_IM_MODULE=fcitx`. Qt 4 and
  XCB-based Qt applications need `QT_IM_MODULE=fcitx`.
- On KDE, start Fcitx5 from System Settings > Virtual Keyboard so the text-input protocol works.
- With GNOME, the input-method popup is positioned correctly only with the Kimpanel extension.

## Chromium and Electron on Wayland
```bash
chromium --enable-features=UseOzonePlatform --ozone-platform=wayland --enable-wayland-ime
```
Add `--wayland-text-input-version=3` for text-input-v3 compositors; prefer version 1 on KWin.
Under XWayland, install the GTK IM module and set `GTK_IM_MODULE=fcitx` as on X11.

## Verify
- [ ] Typing in a GTK app, a Qt app and a browser produces candidates and commits characters.

## Checked
2026-10-28. Confirmed in the Arch Wiki Input method page and the Fcitx wiki Wayland page: the three
environment variables and their ibus/fcitx values, the `simple` fallback values, XMODIFIERS need under
XWayland, text-input-v2/v3 behaviour, Virtual Keyboard setting, Chromium flags, Kimpanel popup note.
Removed (not confirmed): package names, `ibus` and `fcitx5` command usage, key bindings, config file
locations for the variables, Flatpak, Java and tmux notes, `fcitx5-diagnose`.
Method: documentation only; no commands were run.
