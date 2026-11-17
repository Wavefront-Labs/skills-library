---
id: computing-software.ai-ml-engineering.langchain.agent-structured-response-format
name: agent-structured-response-format
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, response-format, create-agent, structured-output, toolstrategy, providerstrategy, pydantic]
level: practitioner
status: verified
description: "Make create_agent return validated structured results with response_format: ToolStrategy vs ProviderStrategy, Pydantic/TypedDict schemas, error handling and retries."
sources:
  - https://docs.langchain.com/oss/python/langchain/structured-output
  - https://docs.langchain.com/oss/python/langchain/agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent structured responses (response_format)

**Goal:** an agent that uses tools freely, then ends with a typed object your code can consume, instead of parsing free text.

## Usage
```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy

class TicketTriage(BaseModel):
    category: str = Field(description="billing | bug | feature | other")
    priority: int = Field(ge=1, le=4)
    summary: str

agent = create_agent("anthropic:<model-id>", tools=[lookup_customer, search_kb],
                     response_format=TicketTriage)            # auto-selects a strategy
out = agent.invoke({"messages": [{"role": "user", "content": ticket_text}]})
triage: TicketTriage = out["structured_response"]
```

## Strategies
- `ProviderStrategy(TicketTriage)`: uses the provider's native structured output (JSON-schema constrained decoding) where supported. Most reliable.
- `ToolStrategy(TicketTriage)`: exposes the schema as a final "tool" the model calls; works with any tool-calling model. `handle_errors=` is `True` by default (validation failures go back to the model as an error ToolMessage and it retries; run: priority=9 on a `le=4` field gave one retry), a `str` (fixed retry message), an exception type or tuple (retry only those), a callable returning a message, or `False` (raises `StructuredOutputValidationError`, run).
- Passing the schema directly lets LangChain pick ProviderStrategy when the model and provider support native structured output (docs name OpenAI, Anthropic, xAI), else ToolStrategy. A raw JSON-schema dict is not auto-detected; wrap it in a strategy. `ProviderStrategy` has an optional `strict` flag (langchain>=1.2, some providers, off by default).

## Schema design
- Field descriptions are instructions; enumerate allowed values (`Literal[...]`) rather than free strings.
- Keep schemas small and flat; deeply nested optional structures increase failures.
- `ToolStrategy(Union[A, B])` lets the agent choose a response shape (e.g. answer vs clarification request; run). The docs show Union only with ToolStrategy.

## Gotchas
- The structured response is produced at the end of the loop; intermediate messages remain in `out["messages"]` for debugging.
- With ToolStrategy, Pydantic validation (ge/le etc.) runs on the tool-call arguments after generation, so keep `handle_errors` on (the default). Whether a provider's native schema enforcement covers every constraint varies; keep the Pydantic model as the source of truth.

## Verify
- [ ] Run against an eval set; measure schema-valid rate and field accuracy, not just "it parsed".
