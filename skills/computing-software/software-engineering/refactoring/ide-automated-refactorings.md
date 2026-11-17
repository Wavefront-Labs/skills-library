---
id: computing-software.software-engineering.refactoring.ide-automated-refactorings
name: ide-automated-refactorings
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, ide-refactoring, automated-refactoring, intellij, rider, vscode, rope]
level: practitioner
status: draft
description: "Use IDE automated refactorings (rename, extract, inline, move, change signature) efficiently and know where they are unsafe: reflection, dynamic code, strings and public APIs."
sources: ["https://www.jetbrains.com/help/idea/refactoring-source-code.html", "https://code.visualstudio.com/docs/editing/refactoring", "https://learn.microsoft.com/en-us/visualstudio/ide/refactoring-in-visual-studio", "https://rope.readthedocs.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated IDE refactorings and their safety limits

## Core set and shortcuts (defaults)
| Refactoring | IntelliJ/Rider | VS Code | Visual Studio |
|---|---|---|---|
| Rename | Shift+F6 | F2 | Ctrl+R, Ctrl+R |
| Extract method/function | Ctrl+Alt+M | Ctrl+Shift+R (refactor menu) | Ctrl+R, Ctrl+M |
| Extract variable | Ctrl+Alt+V | Ctrl+. / Ctrl+Shift+R | Ctrl+. |
| Inline | Ctrl+Alt+N | Ctrl+Shift+R | Ctrl+R, Ctrl+I (preview) |
| Change signature | Ctrl+F6 | language-dependent | Ctrl+R, Ctrl+O/V |
| Move | F6 | drag in explorer (TS updates imports) | Ctrl+. move type to file |
| Refactor this menu | Ctrl+Alt+Shift+T | Ctrl+Shift+R | Ctrl+. |
macOS: Cmd for Ctrl, IntelliJ rename is Shift+F6, extract method Cmd+Alt+M.

Language servers expose the same through LSP code actions (Pylance/basedpyright, rust-analyzer,
gopls, tsserver, Roslyn) so Neovim/Emacs/Helix get them too. Python also: `rope`, Bowler, LibCST.

## How they stay safe
They use the semantic model (types, symbol resolution), so in statically typed code they're
reliable. Always use the **preview** for multi-file changes and run tests after.

## Where they break
- Reflection and string references: `Class.forName("..")`, Spring bean names, `getattr(obj, "name")`,
  JS `obj["prop"]`, serialization field names, ORM queries in strings, DI config XML/YAML.
- Dynamic languages without type info: rename may miss duck-typed call sites or rename unrelated
  methods with the same name. Check "search in comments and strings" results by hand.
- Code outside the project: other repos, published libraries, scripts, SQL, templates, mobile clients.
- Generated code that will be regenerated; macros/preprocessors (C/C++), code in build files.
- Extract method with side effects or multiple outputs: the tool may create out parameters or
  refuse; restructure first (split variable, slide statements).
- Inline can change semantics if the expression has side effects or is evaluated a different number
  of times.

## Habit
Prefer the automated refactoring over manual edits whenever one exists; a manual rename across
30 files is how typos and missed references happen. Grep afterwards for the old name.
