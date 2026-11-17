---
id: computing-software.web-development.litestar.litestar-templating
name: litestar-templating
category: computing-software
field: web-development
product: litestar
tags: [litestar, templating, template, jinja, mako, minijinja, template-config, csrf]
level: practitioner
status: docs-checked
description: "Register Jinja, Mako or MiniJinja in Litestar with TemplateConfig, return Template responses, use request and csrf_input in templates and register template callables."
sources: [https://docs.litestar.dev/latest/usage/templating.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar templating

Goal: render HTML from Jinja2, Mako or MiniJinja templates in route handlers.

## Method

1. Install an engine extra (Litestar does not bundle the libraries): `pip install 'litestar[jinja]'`, `'litestar[mako]'` or `'litestar[minijinja]'`. Jinja is included in `litestar[standard]`.
2. Register the engine:

```python
from pathlib import Path
from litestar import Litestar
from litestar.plugins.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

app = Litestar(
    route_handlers=[],
    template_config=TemplateConfig(directory=Path("templates"), engine=JinjaTemplateEngine),
)
```

   `directory` may be a directory or a list of directories.
3. Own environment: `TemplateConfig(instance=JinjaTemplateEngine.from_environment(my_custom_env))`. `instance` cannot be combined with `directory`; you are then responsible for building the engine.
4. Other engines: implement `TemplateEngineProtocol` with `__init__(self, directory)` and `get_template(self, template_name)`.
5. The engine instance is available as `TemplateConfig.engine`.
6. Return a `litestar.response.Template`: `Template(template_name="test.html", context={"hello": "world"})`, or an inline string with `Template(template_str="...", context={...})`. A missing file raises `TemplateNotFoundException`. The handler return annotation is `Template`.
7. In templates, the current request is available as `request`, so `request.app.state.some_key` reaches app state.
8. CSRF: configure CSRF protection first, then put the hidden input in a form. It must be marked safe or it is escaped. Jinja and MiniJinja use the `safe` filter, Mako uses `${csrf_input | n}`:

```html
<form action="https://myserverurl.com/some-endpoint" method="post">
    {{ csrf_input | safe }}
</form>
```
9. Built-in callables: `url_for` (same signature as `route_reverse`), `csrf_token` (for non-HTML templates or a `<meta>` tag), and `url_for("static", file_name="style.css")` for files from `create_static_files_router`.
10. Custom callable: `engine.register_template_callable(key="check_context_key", template_callable=fn)` where `fn(ctx)` takes the context mapping. Register it by passing `engine_callback=register_template_callables` to `TemplateConfig`.

## Verify

Per the page, run the callable example with `uvicorn template_functions:app` and open http://127.0.0.1:8000 to see the rendered result.

## Checked

2026-11-07. Read the full cited page(s) (usage/templating.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
