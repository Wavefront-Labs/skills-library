---
id: computing-software.ai-ml-engineering.litellm.litellm-custom-prompt-template-and-tokenizer
name: litellm-custom-prompt-template-and-tokenizer
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, prompt-template, custom-tokenizer, token-counter]
level: advanced
status: docs-checked
description: "Set a custom chat prompt template per model, or a custom Hugging Face tokenizer for /utils/token_counter."
sources:
  - https://docs.litellm.ai/docs/proxy/configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tell the proxy how to format messages for a model whose prompt template it does not know, and which tokenizer to count tokens with.
Prompt templates: LiteLLM by default checks whether a model has a prompt template (for example a Hugging Face chat template in tokenizer_config.json) and applies it. Override it per model in config.yaml:

```
model_list:
  - model_name: mistral-7b
    litellm_params:
      model: "huggingface/mistralai/Mistral-7B-Instruct-v0.1"
      api_base: "<your-api-base>"
      api_key: "<your-api-key>" # optional, for hf inference endpoints
      initial_prompt_value: "\n"
      roles: {"system":{"pre_message":"<|im_start|>system\n", "post_message":"<|im_end|>"}, "assistant":{"pre_message":"<|im_start|>assistant\n","post_message":"<|im_end|>"}, "user":{"pre_message":"<|im_start|>user\n","post_message":"<|im_end|>"}}
      final_prompt_value: "\n"
      bos_token: " "
      eos_token: " "
      max_tokens: 4096
```

Start with `litellm --config /path/to/config.yaml`.

Custom tokenizer for the /utils/token_counter endpoint:

```
model_list:
  - model_name: openai-deepseek
    litellm_params:
      model: deepseek/deepseek-chat
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      custom_tokenizer:
        identifier: deepseek-ai/DeepSeek-V3-Base
        revision: main
        auth_token: os.environ/HUGGINGFACE_API_KEY
```

Spec: `identifier` (str, Hugging Face model id), `revision` (str, usually `main`), `auth_token` (optional Hugging Face token).
The roles map sets `pre_message` and `post_message` strings per role, while `initial_prompt_value` and `final_prompt_value` wrap the whole prompt.

## Checked

2026-11-03. Confirmed on the LiteLLM proxy config page (docs.litellm.ai/docs/proxy/configs): the default prompt-template lookup, initial_prompt_value, roles, final_prompt_value, bos_token and eos_token, and custom_tokenizer with identifier, revision and auth_token for /utils/token_counter.

Method: documentation only; no commands were run.
