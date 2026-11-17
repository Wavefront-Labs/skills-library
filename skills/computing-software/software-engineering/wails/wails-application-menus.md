---
id: computing-software.software-engineering.wails.wails-application-menus
name: wails-application-menus
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, menus, accelerators, runtime]
level: practitioner
status: docs-checked
description: "Build a Wails application menu with pkg/menu: Menu and MenuItem types, helpers, radio groups, callbacks, macOS roles, accelerators and runtime updates."
sources: [https://wails.io/docs/reference/menus, https://wails.io/docs/reference/runtime/menu, https://wails.io/docs/reference/options, https://github.com/wailsapp/wails/blob/master/v2/pkg/menu/menu.go]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails application menus

Goal: define a menu and attach it via `options.App.Menu` or `runtime.MenuSetApplicationMenu`.

## Method

```go
AppMenu := menu.NewMenu()
if runtime.GOOS == "darwin" {
    AppMenu.Append(menu.AppMenu()) // must be right after NewMenu() on macOS
}
FileMenu := AppMenu.AddSubmenu("File")
FileMenu.AddText("&Open", keys.CmdOrCtrl("o"), func(_ *menu.CallbackData) {})
FileMenu.AddSeparator()
FileMenu.AddText("Quit", keys.CmdOrCtrl("q"), func(_ *menu.CallbackData) { rt.Quit(app.ctx) })
if runtime.GOOS == "darwin" {
    AppMenu.Append(menu.EditMenu()) // enables Cmd+C, Cmd+V, Cmd+Z on macOS
}
err := wails.Run(&options.App{Menu: AppMenu /* ... */})
```

(`rt` aliases `github.com/wailsapp/wails/v2/pkg/runtime`.) On Mac, with no menu given a default menu is created.

## Types

- `menu.Menu{Items []*MenuItem}`; `menu.NewMenuFromItems(first, rest...)` builds one.
- `MenuItem` fields: `Label`, `Role`, `Accelerator *keys.Accelerator`, `Type`, `Disabled`, `Hidden`, `Checked` (checkbox/radio), `SubMenu *Menu`, `Click Callback`.
- Types: `TextType`, `SeparatorType`, `SubmenuType`, `CheckboxType`, `RadioType`. Helpers: `menu.Text`, `Separator`, `Radio`, `Checkbox`, `SubMenu`; on a menu: `AddText`, `AddSeparator`, `AddRadio`, `AddCheckbox`, `AddSubmenu(label)` (returns the new `*Menu`, as in the example above; the page's signature list shows an `AddSubMenu(label, menu)` form, but `v2/pkg/menu/menu.go` defines `AddSubmenu(label string) *Menu`).
- Radio groups are consecutive radio items; two groups cannot be adjacent, put a non-radio item between them.
- `Callback func(*CallbackData)`; `CallbackData.MenuItem` says which item fired, handy for a shared radio callback.
- Roles are Mac only: `AppMenuRole` (`menu.AppMenu()`), `EditMenuRole` (`menu.EditMenu()`).

## Accelerators (package `menu/keys`)

- `keys.CmdOrCtrl("o")` is Cmd+O on Mac, Ctrl+O elsewhere; also `OptionOrAlt`, `Shift`, `Control`.
- Combine: `keys.Combo("a", ControlKey, OptionOrAltKey)` gives Ctrl+Option+A on Mac, Ctrl+Alt+A elsewhere.
- Parse Electron-style strings: `keys.Parse("Ctrl+Option+A")` returns an accelerator and an error (the docs use it to store accelerators in config files).
- Keys are any single character except `+`, written `plus`. Named keys include `backspace`, `tab`, `return`, `enter`, `escape`, `left`, `right`, `up`, `down`, `space`, `delete`, `home`, `end`, `page up`, `page down`, `f1` to `f25`, `f30` to `f39`, `numlock` (the page's table has no `f26` to `f29`).

## Runtime changes

Go only (the JS runtime has no menu support): `MenuSetApplicationMenu(ctx, menu)` sets the menu; after mutating it, call `MenuUpdateApplicationMenu(ctx)` to apply changes.

## Checked

2026-11-07. Read the whole Menus reference page (website/docs/reference/menus.mdx: example, Menu, MenuItem field table, Accelerator, named-key table, Modifier constants and helpers, keys.Combo, Type constants and helpers, Add helpers, radio-group note, Callback, Role) and the whole runtime Menu page (website/docs/reference/runtime/menu.mdx: MenuSetApplicationMenu, MenuUpdateApplicationMenu, JS unsupported) plus the Menu entry of the Options reference page (Mac default menu note). Trimmed: "f1 to f39" (the page's table lists f1-f25 and f30-f39 only) and the keys.Parse return type (the page shows only a value and an err). Corrected: the page's signature list names `AddSubMenu(label, menu)` but its own example calls `AddSubmenu("File")`; the Go source menu.go (added to sources, read for the Menu methods only) confirms `AddSubmenu(label string) *Menu`.

Method: documentation only; no commands were run.
