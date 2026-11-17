---
id: computing-software.web-development.litestar.litestar-htmx
name: litestar-htmx
category: computing-software
field: web-development
product: litestar
tags: [litestar, htmx, htmxplugin, htmxrequest, htmxtemplate, hx-response, templates]
level: practitioner
status: docs-checked
description: "Integrate HTMX with Litestar using HTMXPlugin, HTMXRequest and the HTMXTemplate, redirect, refresh, swap, retarget and event response classes."
sources: [https://docs.litestar.dev/latest/usage/htmx.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar HTMX integration

Goal: serve HTMX-driven partials and control the client through response classes. Assumes you know HTMX.

## Method

1. Install the extra: `litestar[htmx]`.
2. Register `HTMXPlugin()` in `plugins=[...]` (from `litestar.plugins.htmx`) to set the default request class for all routes. Alternatively set `request_class=HTMXRequest` on the app, router, controller or a route. Template config uses `TemplateConfig(directory=..., engine=JinjaTemplateEngine)`.
3. Take `request: HTMXRequest` in a handler. `request.htmx` is truthy when the `HX-Request` header is present and is an `HTMXDetails` instance (for example `request.htmx.current_url`).
4. Return `HTMXTemplate(template_name="partial.html", context=context, ...)` for HTML snippets. The handler return annotation is `Template`, not `HTMXTemplate`. Optional parameters: `push_url`, `re_swap` (for example `"outerHTML"`), `re_target` (for example `"#new-target"`), `trigger_event`, `params`, `after`.
5. `trigger_event`, `params` and `after` are linked: when triggering an event, `after` is required and must be `receive`, `settle` or `swap`.
6. Responses that do not change the DOM:
   - `HXStopPolling()` stops polling.
   - `ClientRedirect(redirect_to="/contact-us")` redirects with a page reload.
   - `ClientRefresh()` forces a full refresh.
7. Responses that may change the DOM:
   - `HXLocation(redirect_to=..., target="#target", swap="outerHTML", hx_headers={...}, values={...})` redirects without reload (optional `source` and `event` as well).
   - `PushUrl(content="Success!", push_url="/about")`; `push_url=False` prevents updating history.
   - `ReplaceUrl(content=..., replace_url="/contact-us")`; `False` prevents updating the location bar.
   - `Reswap(content=..., method="beforebegin")`.
   - `Retarget(content=..., target="#new-target")`.
   - `TriggerEvent(content=..., name="showMessage", params={...}, after="receive")`.
   Annotate the handler with the same class name it returns.

## Verify

Check that a handler returning `HTMXTemplate` is annotated `-> Template`, as the page's note requires, and that `trigger_event` is paired with `after`.

## Checked

2026-11-07. Read the full cited page(s) (usage/htmx.html) and the example files they include, and confirmed the claims in this skill against that text. Removed an unsourced gotcha about inline template strings and an invented verify step.

Method: documentation only; no commands were run.
