---
id: computing-software.game-programming.unity.editor-windows-and-menu-items
name: editor-windows-and-menu-items
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, editorwindow, menuitem, editor-tools, uitoolkit-editor, asset-database, game-programming]
level: practitioner
status: docs-checked
description: "Build Unity editor tools: MenuItem hotkey characters, validation functions, context and GameObject menus, and EditorWindow with CreateGUI, lifecycle order and GetWindow."
sources: ["https://docs.unity3d.com/ScriptReference/EditorWindow.html", "https://docs.unity3d.com/ScriptReference/MenuItem.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor windows and menu items

**Goal:** add menu commands and custom editor windows (Unity ScriptReference pages).

## MenuItem
- Turns a static function into a menu command; only static functions can use it. Adds items to the main
  menu and Inspector window context menus. Constructors: `MenuItem(string)`,
  `MenuItem(string, bool isValidateFunction)`, `MenuItem(string, bool, int priority)`.
- Hotkey characters: `%` Ctrl (Windows/Linux) or Cmd (macOS); `^` Ctrl on all three; `#` Shift; `&` Alt.
  Bare key after an underscore: `"MyMenu/Do Something _g"`. A space must precede the hotkey text
  (`"MyMenu/Do_g"` is not a hotkey). Shift+Alt+G is `"... #&g"`. Special keys such as `#LEFT`: LEFT,
  RIGHT, UP, DOWN, F1..F12, HOME, END, PGUP, PGDN, INS, DEL, BACKSPACE, TAB, SPACE.
- Validation: a second static method with the same path and `true` as second argument; the item is
  disabled when it returns false. Page example validates `Selection.activeTransform != null`.
- Context menus: `"CONTEXT/Rigidbody/Double Mass"` with a `MenuCommand` parameter; read
  `(Rigidbody)command.context`. `CONTEXT/<EditorTool or EditorToolContext type>/...` adds to the Scene
  view context menu when that tool is engaged.
- `"Assets/..."` items also appear in the Project window right-click menu.
- `"GameObject/..."` creation items: call `GameObjectUtility.SetParentAndAlign(go, menuCommand.context as
  GameObject)`, `Undo.RegisterCreatedObjectUndo`, and set `Selection.activeObject`. Priority 10 groups it
  with the other creation items so it reaches the hierarchy Create dropdown and context menu. Items under
  "GameObject/Create Other" without explicit priority get 10 instead of the default 1000.
- Only set public fields via constructor parameters; changing them later can behave unexpectedly.

## EditorWindow
- Derives from `ScriptableObject`; windows can float or dock as tabs. Open from a `MenuItem`, e.g.
  `GetWindow<MyEditorWindow>()` then set `titleContent`.
- Guidelines: put code dependent on UXML/USS loading in `CreateGUI`; keep event registration inside
  `CreateGUI` or after it.
- Execution order: `OnEnable`; check `EditorApplication.isUpdating` (true while refreshing the
  AssetDatabase); `CreateGUI` (builds the UI if the Editor is not updating); `Update` (multiple times per
  second on visible windows); `OnGUI` (multiple times per frame); `OnDisable`.
- Page example builds a `Label`, `Button` and `Toggle` and adds them to `rootVisualElement`.
- Other members listed: `hasUnsavedChanges`, `saveChangesMessage`, `SaveChanges`, `DiscardChanges`,
  `Repaint`, `OnSelectionChange`, `OnHierarchyChange`, `OnInspectorUpdate` (10 frames per second),
  `ShowUtility`, `ShowModal`, `ShowPopup`, `HasOpenInstances`, `FocusWindowIfItsOpen`.

## Checked
Date: 2026-11-07

Read in full: the `MenuItem` page including its example, and the `EditorWindow` page including its
example and member tables. The linked "Create a custom Editor window with C# script" page was not opened.

Removed because neither page confirms it: the Snap To Ground sample (including `Undo.RecordObjects` on
`Selection.transforms` and the raycast), the `Rigidbody.linearVelocity` reset sample, `[Shortcut]` /
ShortcutManager, `[SerializeField]` state surviving domain reload, `EditorPrefs` / `SessionState`,
subscribing to `hierarchyChanged` / `selectionChanged` and unsubscribing in `OnDisable`, the "Safe edits"
section (`EditorUtility.SetDirty`, `AssetDatabase.SaveAssets`, `StartAssetEditing`, progress bars), and
the Verify list. The page HTML-escaped `<tt>` text is paraphrased, not quoted.

Method: documentation only; no commands were run.
