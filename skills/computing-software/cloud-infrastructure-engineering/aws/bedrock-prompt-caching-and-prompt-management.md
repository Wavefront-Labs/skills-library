---
id: computing-software.cloud-infrastructure-engineering.aws.bedrock-prompt-caching-and-prompt-management
name: bedrock-prompt-caching-and-prompt-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, bedrock, prompt-caching, prompt-management, cache-checkpoints, converse-api, cost-optimization]
level: advanced
status: docs-checked
description: "Cut Bedrock latency and input cost with prompt caching (cache checkpoints in Converse and InvokeModel, TTL, usage fields) and version prompts with Bedrock Prompt management."
sources: ["https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html", "https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html", "https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bedrock prompt caching and prompt management

## 1. Prompt caching
Optional feature that reduces latency and input token cost for supported models when long contexts repeat. Two types:
- **Implicit**: Bedrock and the model try to reuse eligible prefixes; no cache controls needed; best effort, so an identical
  prompt does not guarantee a hit. Keep static content first and dynamic content last.
- **Explicit**: you add model-specific cache controls or checkpoints. A checkpoint can only be created if the whole prefix
  before it meets the model's minimum token count (the page says minimums currently range from 512 to 4,096 depending on the
  model, counted cumulatively across tools, system and messages). The prefix must stay static; changes cause cache misses.
- TTL resets on every hit; many models use a 5-minute TTL. Some models also support 1 hour (the page's model table lists
  which); for models that only support 5 minutes, omit `ttl` because including it can cause a `ValidationException`.
- Billing: tokens written to cache are billed at the model's cache-write rate (can be higher than standard input), tokens read at
  the cache-read rate, all others at the standard rate; see the Bedrock pricing page. Support does not guarantee a hit, so check
  the usage fields in the response.
- Only on-demand inference endpoints; not supported with the batch inference API. It can be used with cross-region inference,
  which at times of high demand may lead to more cache writes (a request served elsewhere can write a new entry instead of reading).
- The model table on the page also lists maximum checkpoints per request (4 for the Anthropic and Amazon Nova rows) and
  which request fields accept them; check it for your model rather than relying on this skill.

## 2. Converse API with cache checkpoints
```python
import boto3
brt = boto3.client("bedrock-runtime")
resp = brt.converse(
    modelId="<model-or-inference-profile-id>",
    system=[{"text": LONG_SYSTEM_PROMPT},
            {"cachePoint": {"type": "default"}}],
    messages=[{"role": "user", "content": [
        {"text": LARGE_REFERENCE_DOCUMENT},
        {"cachePoint": {"type": "default"}},
        {"text": "Question: ..."}]}])
u = resp["usage"]
print(u.get("cacheReadInputTokens"), u.get("cacheWriteInputTokens"))
```
- Checkpoints go in `system`, `messages` or `toolConfig.tools` (a `{"cachePoint": {"type": "default"}}` entry after the tools).
  They are processed tools, then system, then messages; the minimum is evaluated on the cumulative total, and changing an
  earlier section invalidates the cache for later ones. Put stable content first and the variable part after the last checkpoint.
- 1-hour TTL on supported models: `{"cachePoint": {"type": "default", "ttl": "1h"}}`. A 1-hour entry must appear before any
  5-minute entries in the same request.
- For Anthropic models via `InvokeModel`/Messages format use `cache_control` blocks; with up to 4 checkpoints for Claude. Newer
  Claude models also support a single top-level `{"cache_control": {"type": "ephemeral"}}` ("automatic caching", it uses one
  checkpoint slot); other models return a `ValidationException` for it. The lookback checks only about 20 content blocks before a checkpoint.
- The Converse response reports `cacheReadInputTokens`, `cacheWriteInputTokens` and `cacheDetails` (TTL used). Implicit reuse on
  Amazon Nova models is not reported in those fields and not billed as cache reads. OpenAI models on Bedrock use different
  fields (`cached_tokens`, `cache_write_tokens`) and breakpoint syntax; see the page.

## 3. Prompt management
Create, save and version prompts with variables, a chosen model, inference profile or agent, and inference settings; compare
variants while testing; integrate a prompt by specifying it in model inference or by adding a prompt node to a Bedrock Flow.
```bash
aws bedrock-agent create-prompt --name <PROMPT_NAME> --default-variant v1 --variants file://variants.json
aws bedrock-agent create-prompt-version --prompt-identifier <PROMPT_ID>
```
The variant JSON uses (per the API model) `name`, `templateType` (`TEXT` or `CHAT`), `templateConfiguration.text.text` with
`inputVariables`, `modelId`, and `inferenceConfiguration.text` (`maxTokens`, `temperature` 0 to 1). When you enable caching in
Prompt management you can cache system prompts, instructions and messages, depending on the model.

Invoke a managed prompt through Converse with `modelId` set to the **prompt version ARN** (of the form
`arn:aws:bedrock:<REGION>:<ACCOUNT_ID>:prompt/<PROMPT_ID>:<VERSION>`) and the values in `promptVariables`; you can append `messages`.
With a managed prompt you cannot send `additionalModelRequestFields`, `inferenceConfig`, `system` or `toolConfig`; define them in
Prompt management instead.

## Gotchas
- Do not rely on caching for correctness; hits are not guaranteed and a request served by a different server (for example in
  another Region) writes a new entry.
- Changing the prefix (timestamps, IDs in the cached part) causes misses.

## Verify
- [ ] The second identical-prefix request shows `cacheReadInputTokens` greater than zero (on explicit-caching models).
- [ ] Production traffic uses a prompt **version** ARN, and switching versions works as rollback in a test.

## Checked
Date: 2026-11-07. Read: prompt-caching (a few very long paragraphs were cut off after about 900 characters; types, billing, supported-model table, Anthropic, OpenAI and Getting started
sections), prompt-management overview (key definitions and workflow; the child pages such as "Create a prompt" and
"Deploy a prompt" were not opened), and the Converse API reference only for the prompt-management paragraph, the
`promptVariables` field and the response usage fields (the full request/response schema was not read). Botocore models checked
for `CachePointBlock` (`type` default, `ttl` 5m/1h) and the `bedrock-agent` CreatePrompt structure; check_commands passed.
Removed because no page read states them: "around 1,024 tokens for many models", "cached tokens billed at a large discount",
"cache writes cost slightly more", the exact "about 5 minutes" statement for all models, the CloudWatch hit-ratio metric, the
Cost Explorer verify step, the IAM-control and Agents-reference claims, and the sample refund-policy prompt text.
Method: documentation only; no commands were run.
