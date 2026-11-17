---
id: computing-software.data-engineering.prefect.variables
name: variables
category: computing-software
field: data-engineering
product: prefect
tags: [variables, json, unset, configuration, cli]
level: intro
status: docs-checked
description: "Store and read Prefect variables with the SDK and CLI, with naming rules, the 5000 character value limit and the no-secrets rule."
sources:
  - https://docs.prefect.io/v3/concepts/variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share small mutable JSON values between runs.

Variables are named, mutable JSON values scoped to a self-hosted server or one Cloud workspace. They suit infrequent writes and frequent reads and can be cached. They are not encrypted; names and values are visible to anyone with access, so use Secret blocks for sensitive data.

Rules:
- name: at most 255 characters; lowercase letters, numbers, `_` and `-`; no spaces; unique
- value: JSON-serializable, 5000 characters or fewer when serialized
- tags are optional

Interfaces: UI (the + button on the Variables page), SDK, REST API, Terraform, and CLI: `prefect variable set | get | unset | ls | inspect`.

```python
from prefect.variables import Variable

Variable.set("my_variable", "my_value")
value = Variable.get("my_variable")
Variable.set("my_variable", "new", overwrite=True)
Variable.unset("my_variable")
```

Variables are usually loaded at flow runtime but can also be referenced from configuration such as deployment steps (`{{ prefect.variables.variable_name }}` in `prefect.yaml`).

## Checked
2026-11-08. Confirmed against the Variables concept page and the prefect.yaml guide: JSON values, scope, not encrypted, name rules (255 characters, lowercase, digits, underscore, dash), 5000 character value limit, optional tags, the five CLI subcommands, SDK set/get/overwrite/unset and the {{ prefect.variables.variable_name }} syntax. Nothing removed.
Method: documentation only; no commands were run.
