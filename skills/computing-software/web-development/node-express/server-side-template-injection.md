---
id: computing-software.web-development.node-express.server-side-template-injection
name: server-side-template-injection
category: computing-software
field: web-development
product: node-express
tags: [injection, ssti, template-injection, jinja2, nunjucks, security]
level: practitioner
status: docs-checked
description: "Preventing server-side template injection: never compiling user input as templates, sandbox limits in Jinja2/Nunjucks/Handlebars, detection payloads, and safe alternatives."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Template_Injection_Prevention_Cheat_Sheet.html
  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Injection/18-Server-side_Template_Injection
  - https://jinja.palletsprojects.com/en/stable/sandbox/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side template injection (SSTI)

## 1. The bug
User input becomes **template source**, not template data:
```python
render_template_string(f"<h1>Hello {name}</h1>")        # name = "{{ config.items() }}" or RCE gadgets
```
```js
nunjucks.renderString(`Hi ${req.query.name}`, {});
ejs.render(userTemplate, data);                          // arbitrary JS
```
Depending on the engine and configuration, impact ranges from reading sensitive data and files to remote code execution.
Common origins: "customisable" email/notification templates, CMS themes, string-built templates for i18n, error pages rendering the URL into template source.

## 2. Fix
- Pass user input as **data**: `render_template_string("<h1>Hello {{ name }}</h1>", name=name)`; `nunjucks.renderString("Hi {{ name }}", { name })`.
- Templates come from files in the repo, never from requests or the DB writable by users.

## 3. When users must author templates
- Use an engine that limits expression power, such as the logic-less Mustache; any helpers or lambdas you register still run as application code.
- Jinja2 `SandboxedEnvironment` (or `ImmutableSandboxedEnvironment`) restricts access to unsafe attributes; a sandbox does not limit CPU or memory, so combine it with process isolation and limited context.
- Twig treats templates as trusted code: use its sandbox with a strict `SecurityPolicy` and never allow `template_from_string()`. FreeMarker needs the `?new` resolver set to `ALLOWS_NOTHING_RESOLVER`, `?api` disabled and restricted member access. Do not render untrusted templates with Nunjucks, EJS or Pug.
- Pass a minimal context (plain dict of strings), resource limits (timeouts, output size), and render in an isolated worker/container.

## 4. Detection
Send expression probes such as `a{{7*7}}`, `${var}` and `<%var%>`; a response containing `49` for `{{7*7}}` shows the input is evaluated as template code (WSTG).

## Verify
Grep for `render_template_string`, `renderString(`, `Template(` / `compile(` with request data, `ejs.render(`; probe customisable-template features with math payloads in staging.

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24) and the OWASP Web Security Testing Guide (OWASP/wstg). Confirmed: SSTI is untrusted input evaluated as template source, and impact ranges from data and file reads to remote code execution; Jinja2 SandboxedEnvironment and ImmutableSandboxedEnvironment; Mustache as a logic-less engine; registered helpers still run as application code; Twig sandbox with a strict SecurityPolicy and no template_from_string; FreeMarker ?new resolver ALLOWS_NOTHING_RESOLVER and ?api disabled; WSTG probes a{{7*7}}, ${var}, <%var%> and the {{7*7}} to 49 example.

Method: documentation only; no commands were run.
