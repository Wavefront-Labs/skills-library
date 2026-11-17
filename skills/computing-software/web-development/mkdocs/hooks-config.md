---
id: computing-software.web-development.mkdocs.hooks-config
name: hooks-config
category: computing-software
field: web-development
product: mkdocs
tags: [hooks, plugin-events, event-priority, one-off-scripts]
level: advanced
status: docs-checked
description: "Run one-off build customizations with the hooks config (1.4+): Python files exposing plugin event handlers without self, plus priority and import notes."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`hooks` (new in 1.4) lists Python files (paths relative to `mkdocs.yml`) loaded as plugin instances.

```yaml
hooks:
  - my_hooks.py
```

`my_hooks.py` defines plugin event handlers as plain functions (no `self`):

```python
def on_page_markdown(markdown, **kwargs):
    return markdown.replace('a', 'z')
```

Advanced: warn on non-HTTPS links, fatal under `--strict`.

```python
import logging, re
import mkdocs.plugins

log = logging.getLogger('mkdocs')

@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, **kwargs):
    path = page.file.src_uri
    for m in re.finditer(r'\bhttp://[^) ]+', markdown):
        log.warning(f"Documentation file '{path}' contains a non-HTTPS link: {m[0]}")
```

Notes:
- Hooks add no abilities over plugins; they just skip installing a package.
- During `mkdocs serve` the hook module is not reloaded on each build.
- 1.6+: `import foo` works for a `foo.py` adjacent to the hook file.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (hooks): new in 1.4, paths relative to `mkdocs.yml`, handlers without `self`, both examples, not reloaded in serve, `import foo` in 1.6. Removed: a generic verify line.

Method: documentation only; no commands were run.
