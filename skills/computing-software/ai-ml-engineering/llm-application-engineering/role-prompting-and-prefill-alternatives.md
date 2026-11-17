---
id: computing-software.ai-ml-engineering.llm-application-engineering.role-prompting-and-prefill-alternatives
name: role-prompting-and-prefill-alternatives
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, prompt-engineering, role-prompting, prefill, system-prompt, output-format-control]
level: practitioner
status: docs-checked
description: "Use system-prompt roles well and control output format now that assistant prefill returns 400 on Claude 4.6+ models: use structured outputs and instructions."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts
  - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role prompting and prefill (and what replaces prefill)

## Role prompting via the system prompt
```python
client.messages.create(
    model="claude-opus-5-5", max_tokens=4096,
    system="You are the general counsel of a 200-person SaaS company reviewing vendor contracts. "
           "You flag risk in plain language for non-lawyers and cite clause numbers.",
    messages=[{"role": "user", "content": f"<contract>{text}</contract>\nReview the liability terms."}],
)
```
- Setting a role in the system prompt focuses behaviour and tone; even a single sentence makes a difference.
- Put the role and durable rules in `system`; put the task and data in the user turn.
- Explain the why behind constraints ("the output is read aloud, so no markdown") - Anthropic's guide says giving the motivation behind instructions helps the model deliver more targeted responses.

## Prefill: what it was and its status
Prefill meant ending `messages` with a partial assistant turn (e.g., `{"role": "assistant", "content": "{"}`) to force JSON or skip preamble. **Starting with Claude 4.6 models, a prefilled last assistant turn is no longer supported and returns a 400.** Earlier models still support it; assistant messages elsewhere in the conversation are not affected.

## Replacements
| Old prefill use | Now |
|---|---|
| Force JSON / classification | Structured outputs (`output_config.format` with `type: "json_schema"`, or `client.messages.parse()`); for classification, a tool with an enum field of valid labels |
| Skip preamble ("Here is...") | Direct instruction in the system prompt to respond without preamble; or XML tags, structured outputs or tool calling; strip stray preamble in post-processing |
| Steer around refusals | Clear prompting in the user message |
| Continue a cut-off response | Move the continuation to the user message, include the end of the interrupted text and ask to continue; or retry the request |
| Refresh injected context | Put reminders in the user turn, hydrate through tools, or do it during compaction |

Migrating code: search for message lists ending with `role: "assistant"` before `create()` calls and replace with one of the above; add a test that the request is accepted on the target model.

## Verify
- [ ] No request to Claude 4.6+ models ends with an assistant message (lint or test).
- [ ] Format compliance rate measured after migration.

## Checked
2026-11-01. Confirmed against Anthropic's Prompting best practices page (reached from the system-prompts and prefill URLs): role in system prompt, motivation behind instructions, 400 on prefilled last assistant turn from Claude 4.6, migration scenarios, claude-opus-5-5 model id) and the Structured outputs page (output_config.format, json_schema, client.messages.parse). Removed: mid-conversation system messages, Sonnet and Haiku 5.5 ids, Haiku 4.5 example, effort trimming preamble, the strict tool replacement and the 100 percent schema validity claim.
Method: documentation only; no commands were run.
