---
id: computing-software.ai-ml-engineering.langchain.prompt-template-partial-variables-and-formats
name: prompt-template-partial-variables-and-formats
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, partial-variables, prompt-templates, mustache, jinja2, f-string]
level: practitioner
status: verified
description: "Pre-fill LangChain prompt variables with .partial() and partial_variables, compute values at format time, and choose f-string, mustache or jinja2 template formats safely."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Partial variables and template formats

**Goal:** prompts get some variables early (config, dates, format instructions) and the rest at call time, with a template syntax that cannot be abused.

## Partial with values
```python
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You write in {tone}. {format_instructions}"),
    ("human", "{question}"),
])
support_prompt = prompt.partial(tone="plain English", format_instructions=parser.get_format_instructions())
support_prompt.invoke({"question": "Why was I charged twice?"})
```
`.partial()` returns a new template; the original is unchanged, so one base prompt can produce per-tenant variants. `input_variables` on the result shows what callers still must supply - assert it in tests (run: base had `fi, question, tone`; the partial had only `question`).

## Partial with functions
Values that must be fresh per call (dates, feature flags) are callables evaluated at format time:
```python
from datetime import datetime, timezone
prompt = prompt.partial(today=lambda: datetime.now(timezone.utc).date().isoformat())
```
Constructor form: `PromptTemplate(template=..., input_variables=["question"], partial_variables={"today": get_today})`.
A time-varying partial early in the system prompt breaks provider prompt caching; put dynamic values after the stable prefix.

## Template formats
| Format | Syntax | Use when |
|---|---|---|
| `f-string` (default) | `{var}`; literal braces as `{{ }}` | Most prompts. JSON examples need every brace doubled. |
| `mustache` | `{{var}}`, sections `{{#items}}..{{/items}}` | Prompts containing JSON or code; loops over lists. |
| `jinja2` | `{{ var }}`, `{% for %}` | Complex logic; never from untrusted sources. Needs `pip install jinja2`. |

`ChatPromptTemplate.from_messages(msgs, template_format="mustache")` applies to every message. A JSON example inside an f-string template is the most common `KeyError` / "missing variables" bug: switch to mustache or double the braces.

## Security
Treat templates as code. Never build a template from user input (`PromptTemplate.from_template(user_text)`): with jinja2 the author can run expressions (run: `{{ 7*7 }}` rendered `49`; langchain-core uses a sandboxed environment that raised `SecurityError` on `().__class__`, but treat the sandbox as a second line of defence), and with any format the user controls variable names. User content goes into variables, never into the template string. Loading prompts from a hub or registry is fine only from sources you control.

## Verify
- [ ] `template.input_variables` equals exactly the runtime fields the caller provides.
- [ ] Rendering with a sample input produces no stray `{` placeholders.
- [ ] No template is constructed from user-controlled text.
