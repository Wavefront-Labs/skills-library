---
id: computing-software.ai-ml-engineering.llm-application-engineering.tool-schema-and-description-design
name: tool-schema-and-description-design
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-use, function-calling, tool-schema-design, tool-descriptions, agent-tools]
level: practitioner
status: docs-checked
description: "Design LLM tools the model uses correctly: consolidated task-level tools, detailed descriptions, strict JSON schemas, meaningful names and responses, and evaluating tool choice."
sources:
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use
  - https://platform.openai.com/docs/guides/function-calling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tool schema and description design

## Principles
1. **Task-level tools, not API mirrors.** One `schedule_meeting(attendees, duration, window)` beats `list_users` + `list_events` + `create_event` that the model must orchestrate. Anthropic's docs say fewer, more capable tools reduce selection ambiguity.
2. **Descriptions are prompts.** Be detailed: what it does, when to use it (and when not), what each parameter means, units/formats, limits, what it returns, side effects.
3. **Unambiguous names and namespacing:** prefix by service or resource (Anthropic's examples: `asana_search`, `jira_search`, `github_list_prs`); prefix versus suffix naming can affect tool-use evals, so test it.
4. **Constrain inputs:** enums, formats, required fields; set `strict: true` on Claude tool definitions to enable schema validation of tool inputs.
5. **Return what the model needs next:** return high-signal fields with meaningful names rather than cryptic ids (resolving UUIDs to readable names improved Claude's retrieval precision in Anthropic's tests), and offer a `response_format` enum (`concise` or `detailed`). Pagination, filtering and truncation with sensible defaults keep responses small.

```python
tools = [{
    "name": "billing_issue_refund",
    "description": ("Issue a refund for a single paid invoice. Use only after confirming the invoice id with "
                    "billing_get_invoice and only when the customer explicitly asked for a refund. Amount is in the "
                    "invoice currency, minor units excluded (e.g. 12.50). Partial refunds allowed up to the paid "
                    "amount. Returns refund id and status; status 'pending_review' means a human must approve."),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string", "description": "Invoice id like INV-2026-000123"},
            "amount": {"type": "number", "description": "Refund amount, > 0 and <= amount paid"},
            "reason": {"type": "string", "enum": ["duplicate", "service_issue", "goodwill", "other"]},
        },
        "required": ["invoice_id", "amount", "reason"],
    },
}]
```

## Many tools
Many tools cost context. Load on demand (Claude tool search with `defer_loading: true`).

## Evaluate tools like prompts
Build realistic evaluation tasks, each paired with a verifiable outcome. Track accuracy plus runtime, number of tool calls, token use and tool errors. Read the raw transcripts (tool calls and responses) to find where the agent got confused, then rewrite descriptions. Anthropic notes you can paste evaluation transcripts into Claude Code to have it refactor tool descriptions.

## Verify
- [ ] Every tool has a detailed description covering when to use it and what it returns.
- [ ] Eval reports accuracy and tool errors per change to descriptions.

## Checked
2026-11-01. Confirmed against Anthropic's Writing tools for agents post (consolidation, `schedule_event` example, namespacing, `response_format`, readable identifiers, pagination/truncation, evaluation metrics, transcript analysis) and the define-tools page (`strict: true`, consolidation, namespacing, `defer_loading`). Removed: sentence count, OpenAI strict claim, `additionalProperties` advice, MCP-per-domain advice, wrong-tool metrics.
Method: documentation only; no commands were run.
