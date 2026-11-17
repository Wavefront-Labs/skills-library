---
id: computing-software.ai-ml-engineering.langchain.langsmith-prompt-management
name: langsmith-prompt-management
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langsmith, langsmith-prompts, prompt-hub, prompt-versioning, push-prompt, pull-prompt, prompt-tags]
level: practitioner
status: docs-checked
description: "Manage LangSmith prompts from code: push_prompt, pull_prompt by name, commit hash or tag, include_model, public vs private pulls and the in-memory prompt cache."
sources:
  - https://docs.langchain.com/langsmith/manage-prompts-programmatically
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompt management in LangSmith

**Goal:** prompts live in LangSmith, are pulled by name, commit hash or tag, and are cached in process so the hub is not hit on every request.

## Setup
`pip install -U langsmith` (version 0.1.99 or later) and set `LANGSMITH_API_KEY` (Settings, API Keys, Create API Key). The `langchainhub` package is deprecated; functionality now lives in `langsmith`. In Python, the LangSmith SDK is recommended for full functionality; going through LangChain only supports pushing and pulling. Older code and APIs may say "repo" for a prompt.

## Push and pull
```python
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
client = Client()
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
url = client.push_prompt("joke-generator", object=prompt)    # returns a link to the prompt in the UI

p = client.pull_prompt("joke-generator")                       # latest
p = client.pull_prompt("joke-generator:12344e88")              # a specific commit hash or commit tag
chain = client.pull_prompt("joke-generator-with-model", include_model=True)
```
- Pushing a chain of prompt plus model stores the model with the prompt; pulling with `include_model=True` returns a RunnableSequence if the stored prompt includes a model. Set the environment variables the model's provider needs.
- Pulling a private prompt needs no owner handle; pulling a public prompt from the LangChain Hub needs the author's handle, for example `efriis/my-first-prompt`.

## Prompt cache
The SDK has a built-in in-memory prompt cache: a global singleton shared by all clients for the lifetime of the process, using stale-while-revalidate (fast response, background refresh). Defaults: `max_size` 100 prompts, `ttl_seconds` 300.
- Repeated `pull_prompt` calls return the cached version; metrics are on `prompt_cache_singleton.metrics` (hits, misses, hit_rate).
- Configure globally with `configure_global_prompt_cache(...)` before creating clients.
- Disable per client with `Client(disable_prompt_cache=True)` (a global max size of zero also disables it); bypass for one pull with `skip_cache=True`.
- Offline use: pull prompts while online, export with `prompt_cache_singleton.dump("prompts_cache.json")`, load the file in the offline environment, and set `ttl_seconds` to `None` so entries never expire and background refresh is off.

## Checked
Method: docs-checked 2026-11-09 against https://docs.langchain.com/langsmith/manage-prompts-programmatically (lines 1-70, 296-335 and the cache section read; other sections grepped). Dropped commit-tag promotion workflow, push_prompt tags/description arguments, webhook CI, input-variable and visibility gotchas, and the Claude temperature note, none of which that page confirms; the concepts source was not read.
