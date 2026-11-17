---
id: computing-software.software-engineering.tauri.tauri-system-tray
name: tauri-system-tray
category: computing-software
field: software-engineering
product: tauri
tags: [system-tray, tauri, tray-icon, desktop]
level: practitioner
status: docs-checked
description: "Create a Tauri system tray icon in Rust or JavaScript, set its icon and menu, and handle menu and mouse events."
sources:
  - "https://v2.tauri.app/learn/system-tray/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri system tray

Goal: give quick access to common actions from a tray icon.

## Setup

Enable the feature in `src-tauri/Cargo.toml`:

```toml
tauri = { version = "2.0.0", features = [ "tray-icon" ] }
```

## Create, icon and menu

Rust:

```rust
use tauri::{
  menu::{Menu, MenuItem},
  tray::TrayIconBuilder,
};

let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
let menu = Menu::with_items(app, &[&quit_i])?;

let tray = TrayIconBuilder::new()
  .icon(app.default_window_icon().unwrap().clone())
  .menu(&menu)
  .show_menu_on_left_click(true)
  .build(app)?;
```

JavaScript:

```javascript
import { TrayIcon } from '@tauri-apps/api/tray';
import { defaultWindowIcon } from '@tauri-apps/api/app';

const tray = await TrayIcon.new({
  icon: await defaultWindowIcon(),
  menu,              // a Menu from @tauri-apps/api/menu
  menuOnLeftClick: true,
});
```

By default the menu shows on both left and right clicks. To stop it on left click use `show_menu_on_left_click(false)` (Rust) or `menuOnLeftClick: false` (JS).

## Menu events

Rust:

```rust
TrayIconBuilder::new()
  .on_menu_event(|app, event| match event.id.as_ref() {
    "quit" => { app.exit(0); }
    _ => { println!("menu item {:?} not handled", event.id); }
  })
```

In JavaScript, give each menu item an `action` callback.

## Tray (mouse) events

Events: click (single left, right or middle, including whether released), double click, enter, move, leave. On Linux these are unsupported: no event is emitted, though the icon is shown and a right click still shows a context menu.

```rust
TrayIconBuilder::new()
  .on_tray_icon_event(|tray, event| match event {
    TrayIconEvent::Click {
      button: MouseButton::Left,
      button_state: MouseButtonState::Up,
      ..
    } => {
      let app = tray.app_handle();
      if let Some(window) = app.get_webview_window("main") {
        let _ = window.unminimize();
        let _ = window.show();
        let _ = window.set_focus();
      }
    }
    _ => {}
  })
```

In JavaScript pass an `action: (event) => ...` option and switch on `event.type` (`Click`, `DoubleClick`, `Enter`, `Move`, `Leave`).

## Checked
2026-11-08. Read the Tauri v2 system-tray page (tauri-docs, v2 branch) in full; claims match.
Method: documentation only; no commands were run.
