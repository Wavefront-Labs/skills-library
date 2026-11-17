---
id: creative-arts.literary-writing.scrivener.binder-folders-and-text-documents
name: binder-folders-and-text-documents
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, binder-structure, scrivener, scrivener-3, binder, folders, draft-folder, chapters, scenes, convert-to-folder]
level: practitioner
status: draft
description: "Structure the Scrivener binder with folders and text documents: chapters as folders, scenes as documents, converting between them, and what the Draft folder compiles."
sources: ["https://www.literatureandlatte.com/learn-and-support/user-guides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Binder: folders and text documents

**Goal:** a binder whose structure mirrors the book, so navigation, drag-reordering and compile behave predictably. Menu names below follow Scrivener 3; shortcuts and exact labels differ between the Mac and Windows editions and by version, so confirm in the app's Help or the official user guide.

## Basics
- The binder has top-level containers, typically **Draft** (or Manuscript), **Research** and **Trash**. Only the Draft folder is compiled by default; documents elsewhere are not part of the output unless you set otherwise.
- A **text document** holds text. A **folder** is a container that can hold documents and other folders. In Scrivener 3, a folder is also a document in its own right and can carry its own text, synopsis and notes; documents can contain sub-documents too. The distinction is mostly organisational.

## Common structures
- **Scene-per-document:** Draft > Chapter folders > scene documents. Easy to reorder scenes and view each chapter as a continuous text in Scrivenings mode (`creative-arts.literary-writing.scrivener.scrivenings-mode`).
- **Part > Chapter > Scene:** nested folders for parts. Compile formatting can be assigned per folder level.
- **Chapter-per-document** for novellas or nonfiction with long sections; use sections as sub-documents.

## Working steps
1. Create items with the add buttons in the toolbar or the Project menu (Add New Text, Add New Folder).
2. Rename by selecting and typing a title in the editor header or the binder.
3. Drag documents and folders to reorder or nest. Use keyboard move commands (Documents menu) for precise moves.
4. Convert a document to a folder, or a folder to a file, from the Documents > Convert menu when the role changes.
5. Use icons, labels and status (`creative-arts.literary-writing.scrivener.labels-and-status`) to track what each item is.
6. Set per-item **Include in Compile** in the Inspector's metadata or in Compile if you want an item to appear only in the working draft.

## Gotchas
- Moving a document out of Draft removes it from compile.
- Deleting a folder trashes everything in it.
- Folders that hold only structure with no text can show as chapter headings, depending on compile settings.

## Verify
- [ ] Binder mirrors the table of contents.
- [ ] Compile output matches the chapters you expect (compile a test; see `creative-arts.literary-writing.scrivener.compile-to-manuscript-format`).
