---
id: creative-arts.animation.scripting.ae-scriptui-panels
name: ae-scriptui-panels
category: creative-arts
field: animation
product: scripting
tags: [scriptui, ae-scripting, extendscript, after-effects, dockable-panel, scriptui-panels, ui-resource-string, artist-tools]
level: advanced
status: draft
description: "Build dockable After Effects tool panels with ScriptUI: Panel vs Window, layout with groups, resource strings, event handlers, and installing into ScriptUI Panels."
sources:
  - https://extendscript.docsforadobe.dev/
  - https://ae-scripting.docsforadobe.dev/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScriptUI panels

**Goal:** an artist-facing dockable panel in AE (Window menu) with buttons and fields that run your
pipeline scripts.

## Dockable panel skeleton

```javascript
// Save as MyTools.jsx in <AE>/Scripts/ScriptUI Panels/ then restart AE; open from Window menu
(function (thisObj) {
  function build(thisObj) {
    var win = (thisObj instanceof Panel) ? thisObj
      : new Window("palette", "My Tools", undefined, { resizeable: true });
    win.orientation = "column"; win.alignChildren = ["fill", "top"];

    var row = win.add("group"); row.orientation = "row";
    row.add("statictext", undefined, "Version:");
    var ver = row.add("edittext", undefined, "v001"); ver.characters = 6;

    var btn = win.add("button", undefined, "Rename selected comps");
    btn.onClick = function () {
      app.beginUndoGroup("Rename comps");
      var sel = app.project.selection;
      for (var i = 0; i < sel.length; i++) {
        if (sel[i] instanceof CompItem) sel[i].name = sel[i].name.replace(/_v\d+$/, "") + "_" + ver.text;
      }
      app.endUndoGroup();
    };
    win.onResizing = win.onResize = function () { this.layout.resize(); };
    return win;
  }
  var w = build(thisObj);
  if (w instanceof Window) { w.center(); w.show(); } else { w.layout.layout(true); }
})(this);
```

- `thisObj instanceof Panel` is true when launched from the Window menu (docked); otherwise create a
  floating `palette`.
- Lay out with nested `group`s and `orientation`/`alignChildren`; call `layout.layout(true)` after
  building.
- Controls: `button`, `checkbox`, `radiobutton`, `edittext`, `dropdownlist`, `slider`, `listbox`,
  `progressbar`, `panel` (bordered group), `tabbedpanel`.

## Good tool behaviour

- Validate selection and show friendly messages; never let an exception reach the user without
  context (`try { } catch (e) { alert(e.toString()); }`).
- Long operations: update a progressbar and call `win.update()` (AE UI does not repaint otherwise).
- Persist settings with `app.settings.saveSetting("MyTools", "ver", ver.text)`.

## Gotchas

- Panels in `ScriptUI Panels` load at startup; syntax errors show only when opening the panel.
- Fonts and sizes differ between macOS and Windows; avoid hard-coded pixel sizes, use `characters`
  and fill alignment.
- Encrypt/distribute as `.jsxbin` if needed (File - Export as Binary in the ExtendScript tooling or VS
  Code ExtendScript Debugger).

## Verify

Open from the Window menu, dock it, resize: controls reflow; run the button with nothing selected and
with mixed selection: no errors, one undo step per action.
