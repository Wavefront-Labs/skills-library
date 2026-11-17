---
id: computing-software.ai-ml-engineering.litellm.litellm-block-unblock-keys
name: litellm-block-unblock-keys
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, key-block, key-unblock, disable-key]
level: intro
status: docs-checked
description: "Disable and re-enable a LiteLLM virtual key with POST /key/block and POST /key/unblock."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: switch a key off without deleting it.

Block:

```
curl -L -X POST 'http://0.0.0.0:4000/key/block' \
-H 'Authorization: Bearer LITELLM_MASTER_KEY' \
-H 'Content-Type: application/json' \
-d '{"key": "KEY-TO-BLOCK"}'
```

The response includes `"blocked": true`.

Unblock:

```
curl -L -X POST 'http://0.0.0.0:4000/key/unblock' \
-H 'Authorization: Bearer LITELLM_MASTER_KEY' \
-H 'Content-Type: application/json' \
-d '{"key": "KEY-TO-UNBLOCK"}'
```

The response includes `"blocked": false`.

The docs' examples authenticate both calls with the master key. Pass the key value being changed in the JSON body as `key`.

Related key lifecycle controls from the same page:

- `duration` on /key/generate sets how long a key lives (for example "30min").
- Rotation: POST /key/<key>/regenerate or scheduled auto-rotation (see the rotation skill).
- Check state afterwards with `GET /key/info?key=<user-key>`, which returns the key's spend, expiry and model list.
- Regenerating a key with no `grace_period` revokes the old key immediately.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (enable/disable keys, rotation, duration); removed unconfirmed permanent-retirement advice
