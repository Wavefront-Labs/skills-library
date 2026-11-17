---
id: computing-software.ai-ml-engineering.langchain.pydantic-output-parser-and-output-fixing
name: pydantic-output-parser-and-output-fixing
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, with-structured-output, pydanticoutputparser, outputfixingparser, output-parsers, retry-parser]
level: practitioner
status: docs-checked
description: "Parse LLM output into typed objects: prefer with_structured_output, fall back to PydanticOutputParser, and repair failures with OutputFixingParser or RetryOutputParser."
sources:
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/output_parser_fixing.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/output_parser_retry.ipynb
  - https://raw.githubusercontent.com/langchain-ai/langchain/v0.3/docs/docs/how_to/structured_output.ipynb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output parsers and OutputFixingParser

## First choice: native structured output
```python
structured = llm.with_structured_output(Joke, include_raw=True)
r = structured.invoke(text)   # {"raw": ..., "parsed": ..., "parsing_error": ...}
```
- `with_structured_output(schema)` accepts a Pydantic class, a TypedDict or a JSON Schema dict.
- `include_raw=True` avoids raising: the output holds the raw message, the `parsed` value if successful, and any `parsing_error`.
- For models that support more than one method (tool calling and JSON mode) pick with `method=`, for example `with_structured_output(None, method="json_schema")`.
- Streaming of structured output works when the schema is a TypedDict or JSON Schema dict (dict output types).

## Text parsers (models without native structured output)
```python
from langchain_core.output_parsers import PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Actor)
prompt = PromptTemplate(template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"], partial_variables={"format_instructions": parser.get_format_instructions()})
chain = prompt | llm | parser
```
`parser.parse(bad)` raises `OutputParserException` (from `langchain_core.exceptions`), for example "Invalid json output" for single-quoted pseudo-JSON, or a Pydantic "Field required" validation error.

## Repair
```python
from langchain.output_parsers import OutputFixingParser, RetryOutputParser   # v0.3 import path
fixing = OutputFixingParser.from_llm(parser=parser, llm=llm)
retry = RetryOutputParser.from_llm(parser=parser, llm=llm)
retry.parse_with_prompt(bad_response, prompt_value)
```
- `OutputFixingParser` wraps another parser and asks an LLM to fix malformed output. It works for formatting mistakes, such as single quotes instead of JSON.
- It cannot know values that are missing: for `{"action": "search"}` with a required `action_input` it guessed `'input'`. `RetryOutputParser` receives the original prompt as well as the bad output (`parse_with_prompt(completion, prompt_value)`) and produced a sensible value in the docs example.
- In a chain, use `RunnableParallel(completion=completion_chain, prompt_value=prompt) | RunnableLambda(lambda x: retry_parser.parse_with_prompt(**x))`.

## Gotchas
- Repairs can invent values, as the fixing example shows; do not use repair loops to coerce safety-relevant decisions; fail closed.
- Log how often repair happens; a high rate means the prompt or schema needs work (practice advice).

## Verify
- [ ] Test feeds malformed output to the parser chain and asserts a repaired object or a handled error.
- [ ] Parse-failure and repair rates tracked per prompt version.

## Checked
Date: 2026-11-09.
- Confirmed in the v0.3 how-tos output_parser_fixing, output_parser_retry and structured_output: with_structured_output schema types, include_raw output shape, method= argument and method="json_schema", dict-schema streaming, PydanticOutputParser and get_format_instructions, OutputParserException, OutputFixingParser and RetryOutputParser behaviour and import path, parse_with_prompt, chain pattern.
- Removed as unconfirmed: the langchain_classic import path, the RetryWithErrorOutputParser name, max_retries on OutputFixingParser, llm_output attribute of the exception, with_fallbacks/with_retry alternative, "Pydantic parsers emit only at the end" and the JsonOutputParser partial-objects advice, and the claim that method="json_schema" means strict mode.
Method: documentation only; no commands were run.
