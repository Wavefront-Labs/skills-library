---
id: computing-software.ai-ml-engineering.langchain.messagesplaceholder-and-few-shot-chat-prompts
name: messagesplaceholder-and-few-shot-chat-prompts
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, chatprompttemplate, messagesplaceholder, fewshotchatmessageprompttemplate, few-shot, example-selector]
level: practitioner
status: verified
description: "Insert chat history with MessagesPlaceholder and add static or similarity-selected few-shot examples with FewShotChatMessagePromptTemplate, plus brace-escaping pitfalls."
sources:
  - https://docs.langchain.com/oss/python/langchain/overview
  - https://reference.langchain.com/python/langchain-core
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MessagesPlaceholder and few-shot chat prompts

## Chat history slot
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a billing assistant."),
    MessagesPlaceholder("history", optional=True),      # list[BaseMessage] or (role, text) tuples
    ("human", "{question}"),
])
prompt.invoke({"question": "Refund status?", "history": [("human", "hi"), ("ai", "Hello!")]})
```
Shorthand: `("placeholder", "{history}")` is equivalent to an optional placeholder. `n_messages=20` keeps only the last N (run: `n_messages=2` of 3 kept the last 2) - prefer `trim_messages` (token-based) for real budgets.

## Static few-shot examples
```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate
example_prompt = ChatPromptTemplate.from_messages([("human", "{input}"), ("ai", "{output}")])
few_shot = FewShotChatMessagePromptTemplate(examples=[
    {"input": "Card charged twice", "output": "category: duplicate_charge"},
    {"input": "Where is my invoice?", "output": "category: invoice_request"},
], example_prompt=example_prompt)
prompt = ChatPromptTemplate.from_messages([("system", "Classify the ticket."), few_shot, ("human", "{input}")])
```
Examples render as real human/ai turns, which models follow more reliably than examples pasted in the system prompt.

## Dynamic example selection
```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
selector = SemanticSimilarityExampleSelector.from_examples(
    examples, embeddings, InMemoryVectorStore, k=3, input_keys=["input"])
few_shot = FewShotChatMessagePromptTemplate(example_selector=selector, example_prompt=example_prompt,
                                            input_variables=["input"])
```
Embed only the input field (`input_keys`) or the outputs bias similarity. Use `MaxMarginalRelevanceExampleSelector` when similar examples are near-duplicates.

## Gotchas
- Literal braces in templates (JSON examples) must be doubled `{{ }}` in f-string templates (run: unescaped `{"a": 1}` raised `KeyError` for a missing variable `"a"`; doubled and mustache both rendered `{"a": 1}`), or use `template_format="mustache"` / `"jinja2"` (only for trusted templates - jinja2 can execute code).
- User text inserted via variables is not interpreted as template syntax (run: `{y} {{z}}` came through verbatim); untrusted text used as the *template itself* is.
- Too many examples cost tokens on every call and hurt prompt caching if they vary per request: keep the selected set stable per category or place them after the cached prefix.

## Verify
- [ ] `prompt.invoke(...).to_messages()` printed in a test shows the expected turns.
- [ ] Eval accuracy with selected examples beats zero-shot and static examples on a held-out set.
