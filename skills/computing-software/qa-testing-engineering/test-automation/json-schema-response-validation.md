---
id: computing-software.qa-testing-engineering.test-automation.json-schema-response-validation
name: json-schema-response-validation
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [json-schema-assertions, json-schema, api-testing, contract-testing, ajv, jsonschema]
level: practitioner
status: verified
description: "Validate API responses against JSON Schema: writing strict schemas, ajv and Python jsonschema assertions, OpenAPI-derived schemas, additionalProperties and formats."
sources:
  - https://json-schema.org/understanding-json-schema
  - https://ajv.js.org/
  - https://python-jsonschema.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON Schema response validation

**Goal:** every API test checks the full shape of the response (types, required fields, formats, no surprises) in one assertion, catching contract drift that field-by-field assertions miss.

## A strict schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "status", "total", "createdAt"],
  "additionalProperties": false,
  "properties": {
    "id": { "type": "string", "pattern": "^ord_[a-z0-9]{12}$" },
    "status": { "enum": ["PENDING", "PAID", "CANCELLED"] },
    "total": { "type": "number", "minimum": 0 },
    "createdAt": { "type": "string", "format": "date-time" },
    "items": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/item" } }
  },
  "$defs": { "item": { "type": "object", "required": ["sku", "qty"],
    "properties": { "sku": { "type": "string" }, "qty": { "type": "integer", "minimum": 1 } } } }
}
```

## JavaScript (ajv)

```js
import Ajv from 'ajv/dist/2020.js';   // the .js suffix is needed in native Node ESM import addFormats from 'ajv-formats';
const ajv = new Ajv({ allErrors: true, strict: true }); addFormats(ajv);
const validate = ajv.compile(orderSchema);
expect(validate(body), JSON.stringify(validate.errors, null, 2)).toBe(true);
```

## Python (jsonschema)

```python
from jsonschema import Draft202012Validator, FormatChecker
Draft202012Validator(order_schema, format_checker=FormatChecker()).validate(resp.json())
```

## Gotchas
- `format` is annotation-only by default. Python: `FormatChecker()` alone did NOT check `date-time` (an invalid `"not-a-date"` passed, jsonschema 4.x) until `rfc3339-validator` was installed; install `jsonschema[format]` (or that package) and confirm a bad date fails. ajv: with `strict: true` and no `addFormats(ajv)`, `compile` throws `unknown format "date-time" ignored in schema`; with strict off the format is silently ignored. Always include one negative test per format.
- Without `additionalProperties: false` unexpected fields pass; decide deliberately (strict for your own APIs, lenient for third parties).
- Reuse schemas from the OpenAPI spec (`components.schemas`) rather than hand-copying; OpenAPI 3.1 is JSON Schema 2020-12 compatible, 3.0 has differences (`nullable`).
- Schema validation complements value assertions; it does not prove the numbers are right.

## Verify
A response with a removed required field, a wrong type, or an extra field fails the test with a readable error path.
