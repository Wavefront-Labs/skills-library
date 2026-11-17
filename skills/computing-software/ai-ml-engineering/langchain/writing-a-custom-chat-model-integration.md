---
id: computing-software.ai-ml-engineering.langchain.writing-a-custom-chat-model-integration
name: writing-a-custom-chat-model-integration
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, custom-chat-model, basechatmodel, integration, langchain-tests, streaming]
level: practitioner
status: docs-checked
description: "Implement a LangChain chat model for an in-house endpoint: BaseChatModel _generate/_stream, usage metadata, stop tokens, secrets and the langchain-tests suites."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/custom_chat_model.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/contributing/how_to/integrations/standard_tests.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing a custom chat model integration

**Goal:** an internal LLM gateway or unsupported provider behaves like any other LangChain chat model. Subclassing `BaseChatModel` makes it a Runnable with batch via a thread pool, async support, and the `astream_events` API.

## What to implement
| Member | Required |
|---|---|
| `_generate(messages, stop, run_manager, **kwargs) -> ChatResult` | yes |
| `_llm_type` property (unique id, used for logging) | yes |
| `_identifying_params` property (parameterisation for tracing) | optional; include `model_name` |
| `_stream` | optional (streaming) |
| `_agenerate`, `_astream` | optional (native async) |

```python
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult

class GatewayChat(BaseChatModel):
    model_name: str = Field(alias="model")
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        text, n_in, n_out = call_gateway(...)            # your transport
        msg = AIMessage(content=text,
                        response_metadata={"model_name": self.model_name},
                        usage_metadata={"input_tokens": n_in, "output_tokens": n_out, "total_tokens": n_in + n_out})
        return ChatResult(generations=[ChatGeneration(message=msg)])
    def _stream(self, messages, stop=None, run_manager=None, **kwargs):
        for token in stream_gateway(...):
            chunk = ChatGenerationChunk(message=AIMessageChunk(content=token))
            if run_manager:
                run_manager.on_llm_new_token(token, chunk=chunk)   # optional in newer versions
            yield chunk
    @property
    def _llm_type(self): return "internal-gateway"
    @property
    def _identifying_params(self): return {"model_name": self.model_name}
```
- If `_stream` is not implemented, streaming requests are handled by `_generate`.
- `_astream` falls back to running the sync `_stream` in a thread via `run_in_executor` (or to `_agenerate` if `_stream` is absent). Native async is better because it has less overhead.
- Message chunk classes (`AIMessageChunk`, ...) are additive: `AIMessageChunk(content="Hello") + AIMessageChunk(content=" World!")` gives `Hello World!`.
- Put `usage_metadata` (input, output, total tokens) on the message; the docs say the model name in identifying params lets monitoring tools such as LangSmith apply per-token pricing.

## Contribution checklist from the docs
- Document all init arguments in docstrings; link the service API in the class docstring.
- Test `invoke`, `ainvoke`, `batch`, `stream` for the methods you override.
- Stop tokens: respect them, and include the stop token in the response (documented as good practice, "not enforced across models").
- API keys: use Pydantic `SecretStr` so they are not printed.
- Provide native `_agenerate` and `_astream`.

## Standard tests
Install `langchain-core` and `langchain-tests` (pin the `langchain-tests` version, since new tests in new releases can break CI). Subclass `ChatModelUnitTests` (`langchain_tests.unit_tests`) and `ChatModelIntegrationTests` (`langchain_tests.integration_tests`), overriding the `chat_model_class` and `chat_model_params` properties. Optional capabilities are toggled by overriding properties such as `supports_image_inputs`: a supported feature must pass, an unsupported one must be skipped. Run unit tests offline with `pytest --disable-socket --allow-unix-socket --asyncio-mode=auto tests/unit_tests` and integration tests with `pytest --asyncio-mode=auto tests/integration_tests`. The standard tests API reference lists suites and troubleshooting for each test.

## Verify
- [ ] Unit and integration standard suites pass.
- [ ] A LangSmith trace shows token usage and model name for the custom model.
- [ ] `.stream()` yields incremental chunks, not one block.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 custom_chat_model how-to and the standard_tests contributing page: required and optional members, streaming and async fallbacks, additive chunks, usage_metadata and identifying params rationale, contribution checklist, standard-test base classes, properties, pinning advice and pytest commands.
- Removed as unconfirmed: the bind_tools/convert_to_openai_tool recipe and the claim that with_structured_output then works through tool calling, tool_call_chunks details, multimodal block mapping rules, `lc_secrets`, the `has_tool_calling` flag name, the list of live integration checks, and the BaseChatModel API reference source (not read).
Method: documentation only; no commands were run.
