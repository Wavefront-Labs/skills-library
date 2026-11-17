---
id: computing-software.networking-hardware-and-wireless.caddy.templates-directive
name: templates-directive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [templates, server-side-templates, mime, delimiters, markdown, caddyfile, extensions]
level: practitioner
status: docs-checked
description: "Caddyfile templates directive: mime types, delimiters, root, extensions and the user-content security warning."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run template actions in response bodies for simple dynamic pages.

The directive executes the response body as a template document. Features include HTTP subrequests, HTML file includes, Markdown rendering, JSON parsing, basic data structures, randomness and time. The built-in functions are documented under the templates module.

Syntax: `templates [<matcher>] { mime <types...>  between <open_delim> <close_delim>  root <path>  extensions { <name> { ... } } }`.
- `mime`: Content-Types that will be evaluated; others pass through. Default `text/html text/plain`.
- `between`: opening and closing action delimiters; change them if they clash with your document. Default is double braces.
- `root`: site root for file-system functions; defaults to the `root` directive's value or the working directory.
- `extensions`: registers custom functions from modules in the `http.handlers.templates.functions.*` namespace; mainly for plugins (the page's example uses a hit-counter plugin with `style bright_green` and `pad_digits 6`).

Examples: `root /srv`, `templates`, `file_server` enables templates for a static site. For a templated static string, set the type first: `header Content-Type text/plain`, `templates`, then `respond` containing a `now | date "2006"` action.

Security: templates run on the response body from any origin, including proxied apps. If users can post content containing template-looking text, they could evaluate templates and reach the environment, local files and the network. Enable only for trusted or sanitised content, never raw user-generated content.

## Checked

2026-11-08. Read the templates directive page in full. Confirmed: syntax block, defaults for `mime` and `between`, `root` fallback, `extensions` namespace and plugin purpose, the three example configs, and the security warning. Removed the unread claim that the template engine is Go templates.

Method: documentation only; no commands were run.


