---
id: computing-software.ai-ml-engineering.mlflow.mlflow-prompt-registry
name: mlflow-prompt-registry
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-genai, prompt-registry, prompt-versioning, prompt-aliases, genai]
level: practitioner
status: gated
description: "Version prompts in the MLflow Prompt Registry: register_prompt with templates, immutable versions and commit messages, aliases for environments, load_prompt and lineage to runs."
sources:
  - https://mlflow.org/docs/latest/genai/prompt-registry/
  - https://mlflow.org/docs/latest/genai/prompt-registry/create-and-edit-prompts/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.genai.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow Prompt Registry

**Goal:** treat prompts like versioned artifacts: change history, review, aliases for prod/staging, and links to the evaluation runs that justified each version.

## Register
```python
import mlflow
p = mlflow.genai.register_prompt(
    name="support-answer",
    template=("You are a support agent for {{product}}.\n"
              "Answer using only the context.\n<context>{{context}}</context>\nQuestion: {{question}}"),
    commit_message="Require context-only answers",
    tags={"owner": "support-ml"},
)
print(p.version)
```
- Variables use double braces `{{name}}`. Chat-style prompts can be registered as a list of role/content messages.
- Versions are immutable; every `register_prompt` call creates a new version with a commit message (tested: re-registering an identical template still created version 3), and `p.variables` lists the `{{names}}` found (tested). `prompt.format()` raises `Missing variables: {...}` unless `allow_partial=True`; chat prompts (list of messages) format to a list of message dicts.

## Load and use
```python
prompt = mlflow.genai.load_prompt("prompts:/support-answer@production")   # or prompts:/support-answer/3
text = prompt.format(product="Acme Cloud", context=ctx, question=q)
```
Set aliases to promote: `mlflow.genai.set_prompt_alias("support-answer", alias="production", version=3)`. Apps load by alias, so promotion and rollback are registry operations, not deploys.

## Lineage
Prompts loaded during a traced/evaluated run are linked to it, so you can see which prompt version produced which evaluation scores (lineage links and `mlflow.genai.evaluate` gating were not run here (gated: unconfirmed, source is paywalled or blocked)). Combine with `mlflow.genai.evaluate` to gate alias moves: new version must match or beat the current production version on the eval set.

## Practices
- Keep model name and generation parameters with the prompt (as tags or a config) - a prompt tuned for one model often regresses on another.
- Code review for prompt changes: diff versions in the UI, link the eval run in the commit message.
- Cache loaded prompts in the app (with a refresh interval) rather than calling the registry per request; `load_prompt(..., cache_ttl_seconds=0)` is accepted to bypass the client cache (tested).

## Verify
- [ ] Production app loads prompts by alias, with caching.
- [ ] Every alias move linked to an evaluation run.
- [ ] Rollback by alias tested.
