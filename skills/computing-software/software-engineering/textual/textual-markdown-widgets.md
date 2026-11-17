---
id: computing-software.software-engineering.textual.textual-markdown-widgets
name: textual-markdown-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-markdown, markdown, markdown-viewer, table-of-contents, links, tui]
level: practitioner
status: docs-checked
description: "Render Markdown in Textual with the Markdown widget and the MarkdownViewer (table of contents, navigation), and handle link clicks and contents messages."
sources: [https://textual.textualize.io/widgets/markdown/, https://textual.textualize.io/widgets/markdown_viewer/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Markdown and MarkdownViewer

Goal: show Markdown documents in a TUI, optionally with browser-like navigation.

## Method
- `Markdown` (added in 0.11.0): displays a Markdown document. The docs example passes a Markdown string with emphasis, headers, lists, syntax-highlighted code blocks, quotes and tables:

```python
def compose(self) -> ComposeResult:
    yield Markdown(EXAMPLE_MARKDOWN)
```

- Constructor: `Markdown(markdown=None, *, name, id, classes, parser_factory=None, open_links=True)`. With `parser_factory=None` a "gfm-like" parser is used.
- Messages: `Markdown.LinkClicked` (has `href` and `markdown`), `Markdown.TableOfContentsUpdated` (has `table_of_contents`), `Markdown.TableOfContentsSelected` (has `block_id`). It has no reactive attributes or bindings, but provides component classes for styling.
- `open_links=False` stops links opening automatically so a `LinkClicked` handler decides.
- Methods: `update(markdown)` replaces the document, `append(markdown)` adds a fragment (both return an awaitable), `load(path)` loads a file (async, can raise `OSError`), `goto_anchor(anchor)` returns `True` if a heading slug matched. Properties `source` and `table_of_contents`.
- Streaming: `Markdown.get_stream(widget)` returns a `MarkdownStream`; `await stream.write(chunk)` and `await stream.stop()`. The docs say direct appends may not keep up at around 20 appends per second and a stream combines updates.
- `MarkdownViewer` (added in 0.11.0): adds browser-like functionality on top of `Markdown`, including a Table of Contents. Reactive `show_table_of_contents` (bool, default `True`) toggles the sidebar. It posts no messages and has no bindings. Navigation methods: async `go(location)`, `back()`, `forward()`. Properties `document` (the Markdown widget) and `table_of_contents`.
- Choose `Markdown` for static display, `MarkdownViewer` when users need contents navigation.

## Checked
2026-11-07. Read in full: the Markdown and MarkdownViewer widget pages (including the API sections). Confirmed: version badges, constructor parameters and `open_links` default, message names and attributes, no reactive attributes or bindings on Markdown, `show_table_of_contents` default, update/append/load/goto_anchor/get_stream, go/back/forward. Removed: the "not focusable" / "focusable" claims (the pages print a generic Focusable bullet for both) and the invented Verify section; the open_links claim no longer relies on library source.
Method: documentation only; no commands were run.
