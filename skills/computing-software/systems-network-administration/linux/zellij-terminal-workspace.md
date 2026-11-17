---
id: computing-software.systems-network-administration.linux.zellij-terminal-workspace
name: zellij-terminal-workspace
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, zellij, terminal-multiplexer, layouts, kdl, session-resurrection]
level: intro
status: docs-checked
description: "Use zellij as a modern multiplexer: modes and keybinding locking, sessions and attach, KDL layouts for repeatable workspaces, floating panes and session resurrection."
sources:
  - https://zellij.dev/documentation/layouts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zellij

A Rust terminal workspace. Install method, keybindings and session behaviour change between releases: check the
current Zellij documentation and the on-screen status bar, which shows the active keybindings.

## Layouts (KDL)
Per the Zellij layouts documentation, layouts are text files that define an arrangement of panes and tabs.
```kdl
layout {
    pane split_direction="vertical" {
        pane command="htop"
        pane
    }
}
```
```bash
zellij --layout /path/to/layout_file.kdl
```
- By default Zellij loads the `default.kdl` layout from the `layouts` directory, a subdirectory of the config directory.
- A layout can also be applied inside a running session with the same command; it starts as one or more new tabs in
  the current session.
- Pane options beyond `split_direction` and `command` (arguments, names, focus, floating panes) are described on the
  layouts page and its sub-pages: read the version for the release you run.

## Gotchas
- Default keys can collide with shell and editor shortcuts: check the documentation for the locked mode and keybinding
  presets in your version.
- Install per host; it is not a drop-in replacement for tmux scripting and shared-socket workflows.

## Verify
- [ ] `zellij --layout <file>` opens the defined panes and tabs.

## Checked
2026-10-28. Confirmed in the Zellij layouts page: layouts are text files of panes and tabs, `pane split_direction`,
`pane command`, `zellij --layout <file>`, `default.kdl` in the layouts directory, applying a layout in a running session
as new tabs. Removed as unconfirmed (the documentation root and other pages were stubs): mode key chords, session
commands, `zellij run`, `zellij action`, tab names, `focus`, floating panes, session resurrection, plugins, config
dump, OSC52 clipboard, cargo install line.
Method: documentation only; no commands were run.
