---
id: computing-software.systems-network-administration.home-assistant.script-fields-response
name: script-fields-response
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [fields, response, stop]
level: practitioner
status: docs-checked
description: "Give a Home Assistant script input fields with selectors and return a response variable to the caller using the Stop building block."
sources:
  - https://www.home-assistant.io/docs/script/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a script reusable with inputs and a return value.

Add fields in the script editor:

1. Open the script and select Menu > Add fields.
2. Under Fields, select Add field.
3. Enter a Name. The Field key is filled in from it; this is the variable name you use in templates.
4. Optional: turn on Required.
5. Under Selector, choose the kind of input, such as a number or an entity.
6. Optional: set a Default value.
7. Save.

When the script is run directly, its fields appear as inputs in the action. The field key is then available in templates as a variable, for example `{{ minutes }}` for a field with key `minutes`.

Return data to the caller:

1. In the script, add a Stop building block.
2. In The name of the variable to use as response, enter the variable name.
3. In the caller, run the script itself (not Turn on script) and give a name to store the response.

The returned variable must contain keys and values (a mapping). The Turn on script action returns no response, so run the script itself when you need the result.

If the script has fields or uses variables in templates, the caller must supply the values; it does not inherit the caller's variables. Required and Default are used by the editor only; Home Assistant does not check them when the script runs, so give templates a fallback such as `{{ minutes | default(5) }}`.

## Checked

2026-11-04. Confirmed against the Scripts page. Replaced the placeholder field name with a documented example and the script.turn_on wording with Turn on script; added the note that Required and Default are editor-only.

Method: documentation only; no commands were run.
