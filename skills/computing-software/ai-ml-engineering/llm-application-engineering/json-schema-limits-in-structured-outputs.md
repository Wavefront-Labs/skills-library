---
id: computing-software.ai-ml-engineering.llm-application-engineering.json-schema-limits-in-structured-outputs
name: json-schema-limits-in-structured-outputs
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, json-schema-limitations, structured-outputs, strict-tool-use, schema-design, claude]
level: practitioner
status: docs-checked
description: "Design schemas structured outputs accept: supported JSON Schema features, unsupported constraints and recursion, additionalProperties rules, and post-parse validation."
sources:
  - https://docs.claude.com/en/docs/build-with-claude/structured-outputs
  - https://platform.openai.com/docs/guides/structured-outputs#supported-schemas
  - https://json-schema.org/understanding-json-schema
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Supported JSON Schema features and limits

**Goal:** schemas compile on the first request, outputs are guaranteed to parse, and business rules the grammar cannot express are still enforced.

## How constrained decoding works
The provider compiles your schema into a grammar and only allows tokens that keep the output valid. Anything that cannot be expressed as a grammar is rejected or ignored, so not all of JSON Schema is supported.

## Claude structured outputs (`output_config.format` with `type: "json_schema"`, or `strict: true` tools)
Supported: object, array, string, number, integer, boolean, null; `enum`, `const`; `anyOf` and `allOf` (not with `$ref`); `$ref`/`$defs` (internal only); `required`; `default`; string `format` values such as `date-time`, `date`, `time`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`; simple `pattern` regexes; array `minItems` of 0 or 1.
Not supported: recursive schemas; numeric constraints (`minimum`, `maximum`, `multipleOf`); string length (`minLength`, `maxLength`); richer array constraints; `additionalProperties` other than `false` (every object must set `additionalProperties: false`); complex regex features (backreferences, lookahead/lookbehind, word boundaries).
The SDK helpers (`client.messages.parse` with Pydantic/Zod) strip unsupported constraints from the schema sent to the API, mention them in descriptions, and validate the response against the full model afterwards.

## OpenAI strict mode differences
All properties must be listed in `required`; represent optional fields as a union with `null`. `additionalProperties: false` required. A schema may have up to 5000 object properties with up to 10 levels of nesting, and up to 1000 enum values across all enum properties.

## Designing around limits
- Keep schemas shallow and explicit; flatten deep nesting.
- Replace recursion with bounded depth (`children_level1`, `children_level2`) or a flat list with `parent_id`.
- Use `enum` for closed categories instead of free strings plus instructions.
- Put numeric and length rules in `description` and validate after parsing:
```python
from pydantic import BaseModel, Field
class Refund(BaseModel):
    amount: float = Field(ge=0, le=5000, description="Refund in EUR, 0-5000")
    reason: str = Field(max_length=200)
resp = client.messages.parse(model="claude-sonnet-5-5", max_tokens=1024,
                             messages=[...], output_format=Refund)
refund = resp.parsed_output        # validated against the full Pydantic model
```
On validation failure, retry once with the error message or route to review.
- Many optional fields and large `anyOf` unions increase grammar size and compile time; Claude allows at most 24 optional parameters and 16 parameters with union types per request, counted across all strict schemas.

## Operational notes
- The first request with a new schema pays grammar compilation latency; compiled grammars are cached for 24 hours from last use, so keep schemas stable (no per-request generated schemas).
- Structured output does not make content correct - only well-formed. Check `stop_reason` (`max_tokens` truncation, `refusal`) before parsing.
- Citations cannot be combined with `output_config.format` on Claude.

## Verify
- [ ] Every object has `additionalProperties: false`; no recursion.
- [ ] Constraints moved to post-parse validation with tests.
- [ ] Schema is static across requests (cache hits on compilation).

## Checked
Date: 2026-10-28.
- Confirmed in the Claude structured outputs page: supported and unsupported JSON Schema features, string formats, minItems 0 or 1, regex limits, 24 optional / 16 union-type limits, 24-hour grammar cache, `parsed_output`, refusal and max_tokens stop reasons, citations conflict.
- Confirmed in the OpenAI Structured Outputs guide: all fields required with null unions, 5000 properties, 10 nesting levels, 1000 enum values.
- Corrected: allOf is not supported with $ref; added the numeric limits; removed the vague "check docs" wording.
Method: documentation only; no commands were run.
