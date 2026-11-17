---
id: computing-software.ai-ml-engineering.llm-application-engineering.streaming-llm-responses-over-sse
name: streaming-llm-responses-over-sse
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, llm-streaming, sse-streaming, server-sent-events, proxy-buffering, time-to-first-token, cancellation]
level: practitioner
status: docs-checked
description: "Stream LLM output to users: provider stream events, relaying SSE through your backend, proxy buffering, cancellation, partial tool JSON and mid-stream errors."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/streaming
  - https://html.spec.whatwg.org/multipage/server-sent-events.html
  - https://nginx.org/en/docs/http/ngx_http_proxy_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming LLM responses over SSE

**Goal:** users see tokens as they're generated (low perceived latency), and long generations don't hit HTTP timeouts.

## Provider events (Claude)
Stream event sequence: `message_start` -> for each content block `content_block_start`, many `content_block_delta` (`text_delta` for text, `input_json_delta` for tool arguments), `content_block_stop` -> `message_delta` (stop reason, final usage) -> `message_stop`. `ping` events may appear anywhere in the stream; an `error` event (for example `overloaded_error`, the streaming equivalent of HTTP 529) can arrive mid-stream. Token counts in the `message_delta` usage are cumulative. SDK helpers accumulate this for you:
```python
with client.messages.stream(model=MODEL, max_tokens=4096, messages=msgs) as stream:
    for text in stream.text_stream:
        yield text
    final = stream.get_final_message()       # full message + usage for logging
```

## Relay to the browser (FastAPI example)
```python
from fastapi.responses import StreamingResponse
@app.post("/chat")
async def chat(req: ChatReq, request: Request):
    async def gen():
        async with aclient.messages.stream(model=MODEL, max_tokens=4096, messages=req.messages) as s:
            async for text in s.text_stream:
                if await request.is_disconnected():
                    break                                  # stop paying for tokens nobody reads
                yield f"data: {json.dumps({'t': text})}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
```

## Infrastructure pitfalls
- **Buffering proxies** (nginx, some load balancers, API gateways, CDNs) hold the whole response - users see nothing until the end. nginx: `proxy_buffering off;`, or send the `X-Accel-Buffering: no` response header (nginx honours it unless `proxy_ignore_headers` disables it).
- Idle timeouts: long thinking phases send few bytes; an SSE comment line (starts with a colon, for example `: keepalive`) is ignored by clients and can be sent periodically so proxies do not close an idle connection.

## Correctness
- Tool-call arguments stream as partial JSON strings (`input_json_delta`); accumulate and parse once `content_block_stop` arrives, or use the SDK streaming helpers, and validate before executing.
- Moderation/guardrails on streamed output: either buffer sentences and check them before release, or accept post-hoc retraction - decide explicitly.
- Log the final assembled message and usage, not the deltas.

## Verify
- [ ] First token visible in the browser within the TTFT budget through the full production path (CDN, gateway).
- [ ] Closing the tab stops the upstream generation.
- [ ] Mid-stream errors shown to the user and logged.

## Checked
2026-11-01. Confirmed on the Claude streaming page, the WHATWG Server-Sent Events spec and the nginx proxy module page: event sequence, `ping` and in-stream `overloaded_error`, cumulative usage, `text_stream`/`get_final_message` helpers, partial-JSON tool deltas parsed at `content_block_stop`, SSE comment syntax, `proxy_buffering` and `X-Accel-Buffering`. Removed: OpenAI Responses event names and source, gzip advice, the 15 second keep-alive interval, serverless streaming claim. The FastAPI relay is an illustrative pattern, not a documented API.
Method: documentation only; no commands were run.
