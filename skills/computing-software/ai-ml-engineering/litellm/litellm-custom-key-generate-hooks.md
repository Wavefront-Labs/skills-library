---
id: computing-software.ai-ml-engineering.litellm.litellm-custom-key-generate-hooks
name: litellm-custom-key-generate-hooks
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, custom-key-generate, custom-key-update, custom-key-policy]
level: sme
status: docs-checked
description: "Enforce your own rules on key creation and edits with custom_key_generate, custom_key_update and custom_key_policy functions."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hooks are Python async functions referenced from general_settings as `<file>.<function>` (path relative to config.yaml).

`custom_key_generate` receives `data` (GenerateKeyRequest) and returns `{"decision": True}` or `{"decision": False, "message": "..."}`:

```
general_settings:
  custom_key_generate: custom_auth.custom_generate_key_fn
```

Failure mode: it only runs on /key/generate. Edits via /key/update, /key/bulk_update, /team/key/bulk_update and the Admin UI edit flow skip it, so a user can create a compliant key and edit it out of compliance.

`custom_key_update` gets `data` (UpdateKeyRequest), same return contract; rejected updates fail with 403. Update requests contain only changed fields, so an unset field means leave as is. Use `data.model_fields_set` to tell an omitted field from one explicitly set to None.

```
general_settings:
  custom_key_update: custom_auth.custom_update_key_fn
```

`custom_key_policy` is one hook for every operation. It receives `policy_request` with `operation` ("generate", "update" or "regenerate"), `existing_key` (None on generate) and `effective_key` (the row as it will be written, with `expires` as an absolute UTC datetime or None). Denied operations fail with 403 carrying the message.

```
general_settings:
  custom_key_policy: custom_auth.custom_key_policy_fn
```

It runs on /key/generate, /key/service-account/generate, /key/update, the bulk updates and /key/{key}/regenerate, after validation. If all three are set, generate/update hooks run first, then the policy.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (custom key generate, update and policy sections)
