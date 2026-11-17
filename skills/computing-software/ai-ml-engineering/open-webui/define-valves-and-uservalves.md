---
id: computing-software.ai-ml-engineering.open-webui.define-valves-and-uservalves
name: define-valves-and-uservalves
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [valves-events, valves, uservalves, pydantic, secrets, encryption, open-webui]
level: practitioner
status: docs-checked
description: "Declare Valves and UserValves in Open WebUI plugins with password, select, multiselect and slider inputs, and encrypt stored values."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/development/valves
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make plugin settings editable in the UI instead of hardcoding keys.

## Where
Nested `Valves` (and `UserValves`) Pydantic `BaseModel` classes inside a `Pipe`, `Filter`, `Action` or `Tools` class. An Event class may have `Valves` but never `UserValves` (no user). Function Valves are admin-only; Tool Valves are also editable by the tool owner and anyone with write grant. UserValves are edited by any user in a chat under Model controls > Controls > Valves (lists enabled tools and functions only).
```python
from pydantic import BaseModel, Field
from typing import Literal

class Filter:
    class Valves(BaseModel):
        test_valve: int = Field(default=4, description="A numeric valve")
        choice_option: Literal["choiceA", "choiceB"] = Field(default="choiceA")
        priority: int = Field(default=0)   # orders Filters, lower first
    class UserValves(BaseModel):
        test_user_valve: bool = Field(default=False, description="On/off switch")
    def __init__(self):
        self.valves = self.Valves()
    def inlet(self, body: dict, __user__: dict):
        v = __user__["valves"].test_user_valve    # attribute access
        v = dict(__user__["valves"])["test_user_valve"]   # also fine
        # __user__["valves"]["x"] raises TypeError: pydantic models are not subscriptable
        return body
```
The type hint picks the control. Renderer order: `Literal`/enum = select, `bool` = switch, multiselect, range slider, any other non-string = plain text box ignoring `input.type`. So `password` and `select` only work on `str` fields.

## Input types via `json_schema_extra={"input": {...}}`
- Password (masked): `{"type": "password"}`.
- Select: `{"type": "select", "options": ["low","medium","high"]}` or `[{"value": "debug", "label": "Debug"}]`.
- Dynamic select: `"options": "get_model_options"` naming a classmethod `get_model_options(cls, __user__=None) -> list[dict]`; called synchronously each time the dialog opens and must return a list (an `async def` leaves the field empty with a log warning).
- Multi-select: `list[str]` field with `{"type": "multiselect", "options": [...]}`; value stays a real list (plain list valves are comma-split text).
- Slider: `float` with `ge=0, le=2` and `{"type": "range", "step": 0.1}`. Always set `ge` and `le` (default range 0-100, default step 1).

## Storage
Values are plaintext JSON in the database; password input only masks the UI. Set `ENABLE_VALVE_ENCRYPTION=true` to encrypt Tool and Function Valve values with Fernet using a key derived from `WEBUI_SECRET_KEY` (a key exactly 44 characters long is used verbatim and must be url-safe base64 of 32 bytes). Rotating the secret makes stored valve values unreadable; re-enter them.

## Changing code later
Saving (or setting an older version as Production) validates stored values against the new fields; incompatible ones refuse the save with `Current Valves are incompatible with this code: <field>: <message>`. Only fields with stored values are checked. Valve labels can be translated per language from the globe selector in the editor.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/extensibility/plugin/development/valves (read in full): where Valves and UserValves can be declared, who edits them, the attribute access example and TypeError, control selection order, password, select, dynamic select (sync only), multiselect and slider rules and defaults, plaintext storage, ENABLE_VALVE_ENCRYPTION with Fernet and the 44-character key rule, the incompatible-valves save error and label translation. Nothing removed.
Method: documentation only; no commands were run.
