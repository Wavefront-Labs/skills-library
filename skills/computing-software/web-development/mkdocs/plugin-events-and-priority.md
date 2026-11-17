---
id: computing-software.web-development.mkdocs.plugin-events-and-priority
name: plugin-events-and-priority
category: computing-software
field: web-development
product: mkdocs
tags: [plugin-events, event-priority, page-events, build-lifecycle]
level: advanced
status: docs-checked
description: "MkDocs plugin event groups, build order (one-time, global, template, page) and how event_priority and CombinedEvent control handler ordering."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Event kinds and handlers (method `on_<name>`):

- One-time, once per `mkdocs` invocation: `on_startup`, `on_shutdown`, `on_serve`. Under `mkdocs serve`, global events run once per build while these do not.
- Global, once per build: `on_config`, `on_pre_build`, `on_files`, `on_nav`, `on_env`, `on_post_build`, `on_build_error`.
- Template, per non-page template (`extra_templates` and theme `static_templates`), after `on_env`, before page events: `on_pre_template`, `on_template_context`, `on_post_template`.
- Page, per Markdown page, after template events and before `on_post_build`: `on_pre_page`, `on_page_read_source`, `on_page_markdown`, `on_page_content`, `on_page_context`, `on_post_page`.

`on_build_error` fires for any exception.

Ordering: handlers for an event run in `plugins` list order. Since 1.4 a handler can set a priority; higher priority runs first, default 0, ties keep config order.

```python
@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs): ...
```

1.6 adds `CombinedEvent` to register one handler at several priorities.

## Checked

2026-11-04. Confirmed against the MkDocs Plugins guide (Events: one-time, global, template and page events and their order; Event Priorities, `CombinedEvent` new in 1.6; on_build_error) and the `event_priority` hook example in "Configuration". Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
