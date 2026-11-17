---
id: computing-software.ai-ml-engineering.llama-cpp.completion-streaming-and-response
name: completion-streaming-and-response
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, streaming, sse, stop-type, timings]
level: practitioner
status: docs-checked
description: "Read /completion responses: SSE streaming, stop_type values, token counts, timings and prompt progress."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming and response fields

Set `"stream": true` to receive each token as it is predicted, using the Server-Sent Events standard (a different response format). In streaming mode only `content`, `tokens` and `stop` are returned until the end of the completion. The browser `EventSource` interface cannot be used because it lacks POST support, so use `fetch` or another client.

Response fields:

- `content`: completion text, excluding `stopping_word` if any; in streaming mode the next token as a string.
- `tokens`: the same as raw token ids, populated only with `"return_tokens": true` or `"stream": true`.
- `stop`: boolean for use with `stream` to check whether generation has stopped (unrelated to the `stop` words array in the request).
- `stop_type`: `none` (generating), `eos` (EOS token), `limit` (`n_predict` tokens generated before a stop word or EOS), or `word` (a stopping word from the `stop` array).
- `stopping_word`: the word that stopped generation, or `""`.
- `tokens_evaluated`: tokens evaluated in total from the prompt; `tokens_cached`: prompt tokens re-used from the previous completion.
- `truncated`: true if the context size was exceeded during generation, i.e. prompt tokens plus predicted tokens exceeded `n_ctx`.
- `timings`: hash of timing information, such as `predicted_per_second`.
- `generation_settings`: the request options (except `prompt`) plus `n_ctx` and `model`; values may differ from what you sent (bad values filtered, strings converted to tokens).
- `model`: the model alias (use `/props` for the path); `prompt`: the processed prompt, with special tokens possibly added.
- `completion_probabilities`: token probabilities with `n_probs` set; with `post_sampling_probs` true, `logprob` becomes `prob` and `top_logprobs` becomes `top_probs`.

Extra request fields:

- `timings_per_token`: include prompt-processing and generation speed in each response (default false).
- `return_progress`: in stream mode, adds `prompt_progress` with `total`, `cache`, `processed` and `time_ms`. Overall progress is `processed/total`; timed progress is `(processed-cache)/(total-cache)`; `time_ms` is elapsed milliseconds since prompt processing began.
- `sse_ping_interval`: seconds between SSE comment pings while the stream is silent; overrides the server `--sse-ping-interval` for the request; `-1` disables; default is the server setting.

## Checked

Date: 2026-11-08. Confirmed against the POST /completion section of the llama-server README. Removed: the unsupported figure "default 30" for `--sse-ping-interval`.

Method: docs-only read of cited pages, 2026-11-08
