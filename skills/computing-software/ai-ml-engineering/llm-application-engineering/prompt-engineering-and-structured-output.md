---
id: computing-software.ai-ml-engineering.llm-application-engineering.prompt-engineering-and-structured-output
name: prompt-engineering-and-structured-output
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm, prompt-engineering, structured-output, json-mode, function-calling, json-schema, few-shot, chain-of-thought, system-prompt, output-parsing, pydantic, grammar-constrained-decoding, prompt-injection]
level: practitioner
status: docs-checked
description: "Get reliable structured output from LLMs: JSON schema/function-calling vs free-text parsing, few-shot selection, and the prompt failure modes that silently corrupt output."
sources:
  - https://platform.claude.com/docs/en/build-with-claude/structured-outputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompt engineering for reliable, structured LLM output

**Goal:** get output you can parse and act on programmatically, not prose you regex against, and know why a prompt that worked in testing fails occasionally in production.

## 1. Prefer the API's structured-output mechanism over prompted JSON
Claude's docs: without structured outputs, even with careful prompting you can see invalid JSON syntax, missing required fields, inconsistent types and schema violations needing retries. Structured outputs use constrained decoding to guarantee schema-compliant responses.
- **JSON outputs:** put a JSON schema in `output_config.format` with `type: "json_schema"`; the JSON arrives in the response's text content block. SDK helpers accept a Pydantic model (`client.messages.parse(..., output_format=Model)`, result in `parsed_output`) or a Zod schema in TypeScript.
- **Strict tool use:** `strict: true` on a tool guarantees schema validation of tool names and inputs. Both features can be used together in one request.
- **Schema limits:** a subset of JSON Schema. Objects need `additionalProperties: false`; numeric constraints (`minimum`, `maximum`, `multipleOf`), string length constraints and `minItems` beyond 0 or 1 are unsupported (SDK helpers move them into descriptions and validate the response locally); recursive schemas, complex types in enums and external `$ref` are unsupported (local `$ref`/`$def` are supported); regex lookarounds, backreferences and word boundaries are unsupported. Unsupported features return a 400.
- **Complexity limits:** at most 20 strict tools per request, 24 optional parameters and 16 union-typed parameters across all strict schemas; reduce by making parameters required and flattening nesting. Changing `output_config.format` invalidates the prompt cache for that conversation.
- **Incompatible:** citations (400 error) and message prefilling.
- **Property order:** required properties are emitted first, then optional ones; mark all required if order matters.
- If a provider or local model lacks this, grammar-constrained decoding libraries are an alternative to retry-on-parse-failure (practitioner advice, not in the page read).

## 2. Even with guaranteed schemas, handle the documented invalid cases
- **`stop_reason: "refusal"`:** HTTP 200, billed, and the output may not match the schema.
- **`stop_reason: "max_tokens"`:** output truncated and incomplete; retry with a higher `max_tokens`. Always check `stop_reason` before treating a parse failure as a prompt problem.
- **Enum casing:** capitalization of `enum` and `const` strings is not guaranteed; compare case-insensitively and avoid values that differ only by case.
- A schema property asking for the model's step-by-step reasoning can trigger a `reasoning_extraction` refusal; ask for a short explanation instead.
- Validate semantics in code anyway (business rules, cross-field checks); a schema guarantees shape, not truth (practitioner advice).

## 3. Prompt structure (practitioner advice, not from the page read)
- System prompt: role, constraints and output format; put the most critical constraint near the end if you cannot enforce a schema.
- Few-shot: a handful of examples beat zero for format-following; include edge cases (empty, null, boundary), and avoid so many that the model copies example values.
- Do chain-of-thought in thinking blocks or a separate call rather than inside a strict single-field JSON string; the docs note grammars apply only to the direct output, not to thinking, so thinking stays free.
- State constraints affirmatively ("do Y") where possible.

## 4. Failure modes after launch (practitioner advice)
- **Prompt drift from model updates:** pin an exact model ID and re-run your eval set before any version change.
- **Instruction dilution** in very long prompts: repeat critical constraints near the task.
- **Injection via user content or retrieved documents:** schemas limit what the model can emit but do not stop injected instructions; treat extracted fields and tool arguments derived from untrusted text as untrusted downstream, and delimit untrusted text from instructions.

## Verify
- [ ] Output is produced via a schema-enforcing mechanism, not "please respond in JSON" alone.
- [ ] `stop_reason` checked on every call (refusal and max_tokens handled).
- [ ] Enum comparisons are case-insensitive; semantic validation runs in code.
- [ ] Model ID pinned; eval set re-run after any version change.
- [ ] Untrusted text is delimited from instructions and extracted fields are treated as untrusted.

## Checked
Method: docs-checked 2026-11-09 against the Claude Structured outputs page (platform.claude.com; usage, SDK transformation, limitations, invalid outputs, complexity limits and compatibility sections read). Dropped: the OpenAI structured outputs and instructor sources (not read), the "1-5% failure rate of prompted JSON" figure, "few-shot gains diminish past 5-8 examples", and the claim that JSON-mode providers emit invalid enum values. Sections 3 and 4 are practitioner guidance, not source-backed.
