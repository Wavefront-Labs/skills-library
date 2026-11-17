---
id: computing-software.software-engineering.textual.textual-tab-widgets
name: textual-tab-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-tabs, tabs, tabbed-content, content-switcher, tab-pane, tui]
level: practitioner
status: docs-checked
description: "Build tabbed UIs in Textual with Tabs, TabbedContent and TabPane, or ContentSwitcher: constructing tabs, ids, switching with active or current, and messages."
sources: [https://textual.textualize.io/widgets/tabs/, https://textual.textualize.io/widgets/tabbed_content/, https://textual.textualize.io/widgets/content_switcher/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Tabs, TabbedContent and ContentSwitcher

Goal: switch between views with tabs.

## Method
**Tabs** (0.15.0+): headers only, no content.
- `yield Tabs("First tab", "Second tab", Text.from_markup("[u]Third[/u] tab"))`. Strings or `Text` become `Tab` widgets with ids `tab-1`, `tab-2`, ...; pass `Tab("First tab", id="one")` for explicit ids.
- Reactive `active` (str, default `""`) is the active tab id; set it to switch.
- Message `Tabs.TabActivated` carries `event.tab` (use `event.tab.id`). `clear()` empties the tabs and sends `TabActivated` with `tab` set to `None` (plus `Tabs.Cleared`). `add_tab()` accepts a string, `Text` or `Tab`.

**TabbedContent** (0.16.0+): combines Tabs and ContentSwitcher; only one child is visible.
- Titles as positional args: `with TabbedContent("Leto", "Jessica", "Paul"): yield Markdown(...)` for each child; or wrap each child in `TabPane("Leto", id="leto")`.
- Give each TabPane an `id` to switch programmatically: `self.query_one(TabbedContent).active = "jessica"`. Without ids panes get `tab-1`, `tab-2`, ...
- First pane is initial; choose another with `TabbedContent(initial="jessica")`.
- Messages: `TabbedContent.TabActivated`, `TabbedContent.Cleared`. Filter in a handler with `@on(TabbedContent.TabActivated, pane="#<pane id>")` (the message allows `pane` as a selector attribute).
- Styling: the inner `Tab` ids are the pane id prefixed with `--content-tab-`.

**ContentSwitcher** (0.14.0+): container showing one child at a time. Every child needs a unique id; children without one are hidden and ignored.
- Reactive `current` (str or None, default `None`) is the id of the visible child; `None` shows nothing. Set it, for example from a `Button.Pressed` handler using the button's id. Set the initial child via `ContentSwitcher(initial="id")`; without `initial` no child is shown to start. Setting an unknown id raises `NoMatches`. It posts no messages.
- Ids are unique within a parent, so buttons and switcher children may share ids.

## Checked
2026-11-07. Read in full: Tabs, TabbedContent and ContentSwitcher widget pages. Confirmed: version badges, Tab construction and auto ids, active reactive, TabActivated and Cleared, clear and add_tab, TabPane titles and ids, initial, --content-tab- prefix, current reactive, initial and ids. Removed: the not-focusable claim (pages print generic bullets), the invented #home selector value and the Verify section. Added: NoMatches on unknown id, children without ids ignored.
Method: documentation only; no commands were run.
