---
id: computing-software.ai-ml-engineering.langchain.routing-with-runnablebranch
name: routing-with-runnablebranch
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, runnablebranch, langchain-routing, lcel, semantic-routing, router-chains]
level: practitioner
status: verified
description: "Route inputs to different chains in LCEL: classifier-then-dispatch with RunnableLambda (preferred), RunnableBranch conditions, semantic routing by embeddings and fallbacks."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
  - https://docs.langchain.com/oss/python/langchain/structured-output
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Routing with RunnableBranch and custom routers

**Pattern:** classify the request, then dispatch to a specialized chain (different prompt, model or tool set).

## Step 1: structured classification
```python
from typing import Literal
from pydantic import BaseModel
from langchain.chat_models import init_chat_model

class Route(BaseModel):
    destination: Literal["billing", "technical", "general"]

router_llm = init_chat_model("anthropic:<small-model-id>", temperature=0).with_structured_output(Route)
classify = router_prompt | router_llm
```
A small fast model is usually enough for routing.

## Step 2a: dispatch with a function (recommended)
```python
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
chains = {"billing": billing_chain, "technical": tech_chain, "general": general_chain}
def dispatch(x):
    return chains[x["route"].destination]          # returning a runnable invokes it with the same input (run)
full = RunnablePassthrough.assign(route=classify) | RunnableLambda(dispatch)
```

## Step 2b: RunnableBranch
```python
from langchain_core.runnables import RunnableBranch
branch = RunnableBranch(
    (lambda x: x["route"].destination == "billing", billing_chain),
    (lambda x: x["route"].destination == "technical", tech_chain),
    general_chain)                                   # default (required: fewer than two branches raised ValueError, run)
```
Conditions are checked in order; the first true one runs. Readable for a few cases, but the function approach scales better and is easier to test.

## Semantic routing (no LLM call)
Embed a handful of example utterances per route, embed the query, pick the route with the highest cosine similarity above a threshold, else default. Cheaper and faster; less flexible.

## Production concerns
- Log the chosen route for analysis; build an eval set of labeled requests and measure routing accuracy.
- Always have a default route; invalid structured output should fall back (`.with_fallbacks`).
- If routes need multi-turn state or loops, use a LangGraph conditional edge instead.

## Verify
- [ ] Routing accuracy on 100+ labeled examples; confusion matrix between routes.
