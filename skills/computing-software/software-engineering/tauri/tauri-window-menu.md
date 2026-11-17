---
id: computing-software.software-engineering.tauri.tauri-window-menu
name: tauri-window-menu
category: computing-software
field: software-engineering
product: tauri
tags: [window-menu, tauri, menus, desktop]
level: practitioner
status: docs-checked
description: "Create native Tauri window menus in JavaScript or Rust: items, submenus, predefined items, event handling, updates and closing JS menu resources."
sources:
  - "https://v2.tauri.app/learn/window-menu/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri window menu

Goal: attach a native menu to a window (or tray). Desktop only.

## Base menu

JavaScript: `Menu.new({ items: [...] })` with items having `id`, `text`, optional `action`, `checked`, `enabled`, or `{ item: 'Separator' }`; then `await menu.setAsAppMenu()`. Update an item through `await menu.get('status')` then `setText(...)`.

Rust:

```rust
let menu = MenuBuilder::new(app)
    .text("open", "Open")
    .check("check_item", "Check Item")
    .separator()
    .build()?;
app.set_menu(menu.clone())?;
```

## Events (Rust)

```rust
app.on_menu_event(move |app_handle: &tauri::AppHandle, event| {
    match event.id().0.as_str() {
        "open" => { println!("open event"); }
        _ => { println!("unexpected menu event"); }
    }
});
```

In JavaScript give each item an `action` callback.

## Multi-level menus

Use `Submenu.new({ text, items })` (JS) or `SubmenuBuilder::new(app, "File")` (Rust), then `MenuBuilder::new(app).items(&[...])`. On macOS all items must be under a submenu (top-level items are ignored), and the first submenu goes under the application menu regardless of its `text`, so make the first one something like "About". Submenu icons exist since Tauri 2.8.0. In Rust, using `Image` needs the `image-png` or `image-ico` feature on `tauri`.

## Predefined items

JS: `PredefinedMenuItem.new({ text, item: 'Copy' })` (also `Separator`, `Undo`, `Redo`, `Cut`, `Paste`, `SelectAll`). Rust: builder methods `.copy()`, `.undo()`, `.redo()`, `.cut()`, `.paste()`, `.select_all()`, `.separator()`.

## Changing status

Change text, icon or checked state via item setters (`set_text`, `set_icon`, `set_checked`, `set_accelerator`; JS `setChecked`, `setIcon`, `setAccelerator`), or call `set_menu` again.

## Avoid JavaScript menu leaks

Since Tauri 2.12 the JS menu APIs support `await using`, which closes resources when the variable leaves scope (an older browser may need a polyfill). Otherwise call `close()`:

```typescript
const copy = await PredefinedMenuItem.new({ item: 'Copy' });
const menu = await Menu.new({ items: [copy] });
await copy.close();
const prev = await menu.setAsAppMenu();
await menu.close();
await prev?.close();
```

Close menu items from `Menu.get` and anything returned by `setAsAppMenu`. JS menus are references; release all of them to release the menu.

## Checked

Checked 2026-11-08 against the Tauri v2 window menu page: JavaScript and Rust menu creation, on_menu_event, macOS submenu rules, submenu icons since 2.8.0, the image-png and image-ico features, predefined items, status changes, and await using from Tauri 2.12 with the close rules. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
