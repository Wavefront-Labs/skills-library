---
id: computing-software.systems-network-administration.apache-guacamole.multiple-connections-tiling
name: multiple-connections-tiling
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, multiple-connections, tiled-view, connection-switcher, broadcast-input, focus, thumbnails]
level: intro
status: docs-checked
description: "Run several Guacamole connections in one tab: switch from the menu, tile them with checkboxes, and broadcast keystrokes to focused tiles."
sources:
  - https://guacamole.apache.org/doc/gug/using-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple connections and tiling

Switching:
- Open the Guacamole menu (Ctrl+Alt+Shift) and pick another connection from the connection-name dropdown at the top.
- The previous one keeps running as a thumbnail in a panel at the lower right; click it to return, or its X to close it.

Tiling several sessions in one window:
1. In the same menu's connection list, tick the checkboxes of the connections to show.
2. They are arranged in equally-sized tiles.
3. Click a tile to focus it (blue title and border). Keyboard input and the menu affect only the focused tile.
4. Hold **Ctrl** and click to focus individual tiles, or **Shift** to focus a rectangle of tiles.
5. Each key pressed is broadcast to every focused tile; Guacamole translates your local keyboard layout to each remote layout.

Uses and cautions:
- Handy for running the same command on several hosts; check which tiles are focused before typing, because input is broadcast.

The page gives no limit on the number of tiles.

Verify: tick two connections, focus both with Ctrl, type a character and see it appear in both.

## Checked

2026-11-08. Read the whole of the Guacamole user interface chapter (using-guacamole.html) and confirmed the switching dropdown, lower-right thumbnail panel with X to close, checkbox tiling in equal tiles, focus indication, Ctrl and Shift multi-focus, broadcast typing and layout translation. Removed the claim that each tile counts toward connection limits and the cross-reference built on it (not stated on the page).
Method: documentation only; no commands were run.
