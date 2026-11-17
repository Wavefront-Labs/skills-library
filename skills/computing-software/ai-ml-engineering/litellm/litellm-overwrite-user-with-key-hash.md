---
id: computing-software.ai-ml-engineering.litellm.litellm-overwrite-user-with-key-hash
name: litellm-overwrite-user-with-key-hash
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, overwrite-user-with-key-hash, end-user-id, abuse-detection]
level: advanced
status: docs-checked
description: "Force the outgoing user field on chat completions to the calling key hash so provider abuse tracking maps to your keys."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v1.95.0. Many providers use the request's end-user identifier (the `user` field) for abuse detection and to trace activity back to an end user, so one user's misuse is less likely to disrupt access for the whole organisation. Because that field is client-controlled, the proxy can overwrite it.

Enable:

```
litellm_settings:
  overwrite_user_with_key_hash: true
```

When on, the proxy force-sets the outgoing `user` on chat/completions requests to the calling key's identity, always overriding any user in the request body and setting it even when the client omits it. For a virtual key the value is the key's sha256 token hash.

Example: a request with `"user": "anything-the-client-sends"` and a virtual key reaches the provider with `user` set to the key's sha256 hash (for example 98e983...6401) rather than the client value.

Notes from the docs:

- Off by default.
- Only affects keys the proxy itself validated (virtual keys and the master key).
- Behaves the same whether the virtual key has a user or sits under a team; the stamp is always the key hash.
- Whether the user value reaches the provider on the wire is each provider's existing behaviour: some forward user as-is, some map it onto their own end-user field, some drop it. This setting only controls the value the proxy sends.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (overwrite_user_with_key_hash section)
