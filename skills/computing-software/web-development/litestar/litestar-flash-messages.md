---
id: computing-software.web-development.litestar.litestar-flash-messages
name: litestar-flash-messages
category: computing-software
field: web-development
product: litestar
tags: [litestar, flash-messages, flash-plugin, sessions, templating, jinja2, notifications]
level: practitioner
status: docs-checked
description: "Register Litestar's FlashPlugin with a session middleware and template config, flash messages from handlers, and render them with get_flashes."
sources: [https://docs.litestar.dev/latest/usage/plugins/flash_messages.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar flash messages

Goal: show one-time messages (success, warning, error) after a user action. Added in Litestar 2.7.0.

## Method

- Flash messages need a valid session configuration, so enable a session middleware, here `ServerSideSessionConfig().middleware`.
- Create a `TemplateConfig` and wrap it in `FlashConfig`, then register `FlashPlugin`. The docs show examples for Jinja2, Mako and MiniJinja engines.

```python
from litestar import Litestar
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.plugins.flash import FlashConfig, FlashPlugin
from litestar.plugins.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

template_config = TemplateConfig(engine=JinjaTemplateEngine, directory="templates")
flash_plugin = FlashPlugin(config=FlashConfig(template_config=template_config))

app = Litestar(
    plugins=[flash_plugin],
    middleware=[ServerSideSessionConfig().middleware],
)
```

- In a handler call `flash(request, message, category=...)` (from `litestar.plugins.flash`); it stores the message in the request context for the template.
- In the template iterate `get_flashes()`; each item has `.message` and `.category`.

```python
@get()
async def index(request: Request) -> Template:
    flash(request, "Oh no! I've been flashed!", category="error")
    return Template(
        template_str="""
    <h1>Flash Message Example</h1>
    {% for message in get_flashes() %}
    <p>{{ message.message }} (Category:{{ message.category }})</p>
    {% endfor %}
    """
    )

app = Litestar(
    plugins=[flash_plugin],
    route_handlers=[index],
    template_config=template_config,
    middleware=[ServerSideSessionConfig().middleware],
)
```

## Verify

Requesting `/` in the example renders a paragraph with "Oh no! I've been flashed!" and Category:error. The same approach applies to Mako and MiniJinja.

## Checked

2026-11-07. Read the full cited page(s) (usage/plugins/flash_messages.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
