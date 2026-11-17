---
id: computing-software.ai-ml-engineering.litellm.litellm-guardrails-stream-scope
name: litellm-guardrails-stream-scope
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, guardrails, stream-scope, logging-only-scope]
level: advanced
status: docs-checked
description: "Limit a guardrail to streaming or non-streaming requests with stream_scope and to one direction with logging_only_scope."
sources:
  - https://docs.litellm.ai/docs/proxy/guardrails/quick_start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`stream_scope` (under the guardrail's litellm_params) chooses which request shapes a guardrail evaluates:

- `streaming`: only when the client asked for a streamed response
- `non_streaming`: only regular request/response calls
- `both`: every request (default when unset)

A guardrail with several modes can scope each mode separately with a map keyed by mode name; a mode left out of the map defaults to both. Realtime audio input transcription counts as streaming. Bedrock pass-through requests report streaming state from the invoked Bedrock action.

Validation: any other value, or a map whose keys are not mode names, is rejected with 422 on create and update.

`logging_only_scope` narrows a `logging_only` scan:

- `input`: scan only the request
- `output`: scan only the response
- unset/null (default): scan both

`both` is not a value; it is logged and ignored at startup and rejected with 422 on create and update. A scope without `logging_only` in mode returns 400 on create. The scan never blocks or changes the client call; each verdict, including a would-block verdict, is recorded in `guardrail_information` on the spend log.

`logging_only_continue_on_input_failure`: by default, if the input scan fails, the output scan is skipped. Set it to true to log the input failure as a warning and still scan the response. It is ignored when logging_only_scope is set.

`mode: [pre_call, logging_only]` with a scope only narrows the logging_only scan; the pre_call mode still blocks.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/guardrails/quick_start (stream_scope and logging_only_scope sections)
