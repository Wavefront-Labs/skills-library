---
id: computing-software.cybersecurity-defensive.application-security.server-side-template-injection-prevention
name: server-side-template-injection-prevention
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [input-validation, template-injection, ssti, jinja2-sandbox, freemarker, twig, cwe-1336]
level: practitioner
status: docs-checked
description: "Prevent server-side template injection: never build templates from input, pass data as context, sandbox user-authored templates, engine settings, and tests."
sources: ["https://portswigger.net/web-security/server-side-template-injection", "https://cwe.mitre.org/data/definitions/1336.html", "https://jinja.palletsprojects.com/en/stable/sandbox/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side template injection (SSTI) prevention

SSTI happens when user input becomes part of the template source rather than data rendered by it.
Template engines are powerful languages; injection usually leads to remote code execution.

## The bug
```python
# vulnerable: user input concatenated into the template source
Environment().from_string("Hello " + name).render()
# safe: input passed as data
Environment().from_string("Hello {{ name }}").render(name=name)
```
The same pattern applies to every template engine that can compile a template from a string.

## Rules
1. Templates come from files in the codebase, never from request data, database fields editable by users,
   or concatenation.
2. Pass user data only through the context/model.
3. If users must author templates (email templates, CMS): use a logic-less engine (Mustache/Handlebars
   without helpers that execute code) or a sandbox:
   - Jinja2 `SandboxedEnvironment` (see the Jinja sandbox documentation; keep Jinja2 updated).
   - For other engines, use the engine's own documented sandbox or restricted mode.
4. Render user-authored templates in an isolated worker with no secrets or network access, with time and
   memory limits.

## Find it
Search the code for template engines compiling strings, such as `Environment().from_string`. Review any feature where users customise text with placeholders.

## Test
Fuzz in test environments with a polyglot of template special characters (PortSwigger gives `${{<%[%'"}}%\`), then an arithmetic probe such as `${7*7}`: evaluated output instead of the literal text means the input is being evaluated.

## Verify
Unit tests render the arithmetic probes as literal text in every user-facing template path; sandbox tests
confirm that unsafe attribute and callable access is blocked.

## Checked

2026-10-28. Confirmed: PortSwigger SSTI page (input as template source vs data, logic-less engines such as Mustache, polyglot fuzz string, `${7*7}` probe); Jinja sandbox documentation (`SandboxedEnvironment`, `from_string`); CWE-1336. Removed: `render_template_string`, the FreeMarker, Twig, Thymeleaf and Spring view-name specifics, `<%= 7*7 %>` and `#{7*7}` probes, `__class__`/`getClass()` and the claim that sandbox escapes have been found (none were in the fetched pages).
Method: documentation only; no commands were run.
