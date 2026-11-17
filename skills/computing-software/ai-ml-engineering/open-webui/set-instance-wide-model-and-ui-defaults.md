---
id: computing-software.ai-ml-engineering.open-webui.set-instance-wide-model-and-ui-defaults
name: set-instance-wide-model-and-ui-defaults
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [env-configuration, persistent-config, default-models, ui-visibility, interface-defaults, model-params]
level: practitioner
status: docs-checked
description: "Preset default models, pinned models, model parameters, interface settings and hidden controls for every Open WebUI user with environment variables."
sources:
  - https://docs.openwebui.com/reference/env-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give every account sensible starting models, parameters and UI without per-user setup. All variables below are ConfigVars: after the first launch the stored value wins over the environment (set `ENABLE_PERSISTENT_CONFIG=false` to make environment values win on every start). Most are also editable in Settings > Admin.

## Models
- `DEFAULT_MODELS`: comma-separated model IDs pre-selected on a new chat. Missing or hidden models are dropped and replaced by these. A user's own default, a `model`/`models` URL parameter and per-group default models take precedence.
- `DEFAULT_PINNED_MODELS`: comma-separated IDs, for example `gpt-5.6-sol,claude-opus-5`. Seeds a user's pin list once; afterwards the user's pins win.
- `MODEL_ORDER_LIST`: JSON array such as `["gpt-5.6-sol","qwen3.6:27b"]`. Listed models come first, others follow. Invalid JSON is logged and ignored.

## Parameters and metadata (JSON strings)
- `DEFAULT_MODEL_PARAMS`, default `{}`, for example `{"temperature":0.7,"function_calling":"native"}`. Baseline applied at chat completion; per-model overrides win, and a parameter in the request body keeps the caller's value. `custom_params` entries merge by name with a model's own.
- `DEFAULT_MODEL_METADATA`, default `{}`, for example `{"capabilities":{"vision":true,"web_search":true}}`. Capabilities merge (per-model wins); other fields apply only when the model has none.
- On a parse failure both log the error and fall back to `{}`.

## Interface
- `DEFAULT_INTERFACE_SETTINGS`: JSON object of starting values for Settings > Interface, for example `{"chatBubble": false, "title": {"auto": false}}`. A user's own choice wins; untouched options keep following the default. Ignored if not a JSON object.
- `UI_VISIBILITY`: JSON object hiding controls from non-admins, for example `{"chat.fork": false, "models.pin": false, "settings.usage": false}`. Admins always see everything, `true` or a missing ID shows the control, and a non-boolean value logs an error and shows every control. Hiding only removes the control; the feature keeps working. ID families: `model_editor.capabilities.*`, `model_editor.defaults.*`, `model_editor.tools.*`, `chat.*` (for example `chat.archive`, `chat.tags`, `chat.artifacts`), `models.*`, `settings.*` (for example `settings.chat_bubble`).
- `DEFAULT_LOCALE`: language for a browser's first visit (empty means browser language, `en-US` fallback). `?lang=` and the Settings choice win; changing it later affects only browsers that never opened the app.

## Example
```bash
DEFAULT_MODELS="qwen3.6:27b"
DEFAULT_MODEL_PARAMS='{"temperature":0.7}'
UI_VISIBILITY='{"chat.fork": false}'
```

## Gotchas
- Defaults set on a group replace `DEFAULT_MODELS` for that group's members.
- Quote JSON values so the shell keeps them intact.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: reference/env-configuration (the default-model, default-parameters and UI variables). Removed: a Verify section the docs do not contain and a reference to a missing sibling skill; the persistent-config behaviour is now stated directly.
Method: documentation only; no commands were run.
