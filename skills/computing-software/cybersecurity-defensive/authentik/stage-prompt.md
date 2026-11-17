---
id: computing-software.cybersecurity-defensive.authentik.stage-prompt
name: stage-prompt
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, prompt-stage, field-types, prompt-data, validation-policies, dynamic-choices]
level: practitioner
status: docs-checked
description: "Configure authentik Prompt stage fields, types, field keys, dynamic choices via expressions and validation policies, and write answers to users with User Write."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/prompt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: collect user input and store it under `prompt_data` in the flow context.

## Field types
Text, Text (read-only), Text area, Text area (read-only), Username (uniqueness check), Email, Password (multiple password fields in one stage must match), Number, Checkbox, Radio Button Group, Dropdown, Date, Date-time, File (stored as a data URI), Separator, Hidden, Static, authentik: Locale.

Field attributes: `field_key`, label, required, placeholder (for choice fields the available choices), initial value (the default choice), order, and the options **Interpret placeholder as expression** / **Interpret initial value as expression**.

## Choices
For Radio Button Group and Dropdown the placeholder defines valid choices: a string, list, or objects with `label` and `value`. Only defined choices are accepted, and the default must be one of them. Expression form:
```python
return [
    "first option",
    42,
    {"label": "another option", "value": "some value"},
]
```
Expressions have access to `prompt_context`; context overrides are `<field_key>__choices` (choices) and `<field_key>` (initial value).

## Storing data
The Prompt stage never updates the user. Bind a User Write stage after it. Field keys `username`, `name`, `email` and `attributes.<name>` (including nested `attributes.settings.locale`) are stored; any other key such as `department` stays only in `prompt_data`. Read it in policies:
```python
request.context.get("prompt_data", {}).get("<field_key>")
```

## Validation
Bind validation policies directly to the Prompt stage, for example to compare two password fields:
```python
if request.context["prompt_data"]["password"] == request.context["prompt_data"]["password_repeat"]:
    return True

ak_message("Passwords don't match.")
return False
```

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/prompt/.
Removed as not confirmed by that page: case-sensitive username claim.
Method: documentation only; no commands were run.
