---
id: computing-software.software-engineering.typer.typer-file-types-import
name: typer-file-types-import
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, file, path, imports, file-objects]
level: intro
status: docs-checked
description: "Decide between Path and Typer's file-like types and import FileText, FileTextWrite, FileBinaryRead and FileBinaryWrite directly from typer."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/reference/file_objects.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/file/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/file.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing Typer file object types

Typer offers two ways to declare file parameters, and the reference page frames the choice simply:

- To declare some types of files, use `Path`.
- When you need access to a file-like object, use the special File types (covered in the File tutorial page). In that tutorial, a file-like object is what `open()` returns.

## Imports

All four classes are imported from `typer` directly:

```python
from typer import FileBinaryRead, FileBinaryWrite, FileText, FileTextWrite
```

You can equally reference them as `typer.FileText` and so on, after `import typer`.

## The four classes

- `FileText`: reading text.
- `FileTextWrite`: writing text.
- `FileBinaryRead`: reading binary data.
- `FileBinaryWrite`: writing binary data.

The reference page only lists each class with its generated API documentation; the behaviour (modes, `lazy`, `atomic`, `encoding`) is explained in the File tutorial page.

## Decision rule

Per the tutorial, `Path` is usually enough (you can read and write data with it the same way). Use the File types for special cases, such as migrating an existing application that expects a file-like object.

Usage, as in the tutorial:

```python
def main(config: Annotated[typer.FileText, typer.Option()]):
```

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/reference/file_objects.md and docs/tutorial/parameter-types/file.md (added to sources). Removed or trimmed: nothing; the tutorial page was added to sources because the Path guidance and open() description come from it.

Method: documentation only; no commands were run.
