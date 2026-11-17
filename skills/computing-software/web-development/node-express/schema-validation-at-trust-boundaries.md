---
id: computing-software.web-development.node-express.schema-validation-at-trust-boundaries
name: schema-validation-at-trust-boundaries
category: computing-software
field: web-development
product: node-express
tags: [injection, input-validation, schema-validation, zod, pydantic, strong-parameters]
level: practitioner
status: verified
description: "Validating all input at trust boundaries with schemas: zod in Express, pydantic in Python, Rails strong params, allowlists, size limits, and returning useful 400 errors."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
  - https://zod.dev/
  - https://docs.pydantic.dev/latest/
  - https://guides.rubyonrails.org/action_controller_overview.html#strong-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema validation at trust boundaries

Trust boundary = anywhere data enters: HTTP body/query/headers/params, webhooks, queue messages, files, third-party API responses, env vars. Validate there once, then work with typed data.

## 1. Express + zod
```js
import { z } from "zod";
const CreateOrder = z.object({
  sku: z.string().regex(/^[A-Z0-9-]{3,32}$/),
  qty: z.coerce.number().int().min(1).max(100),
  note: z.string().max(500).optional(),
  shipping: z.enum(["standard", "express"]),
}).strict();                                         // reject unknown keys (mass assignment); in zod 4 `z.strictObject({...})` is the preferred spelling

const validate = schema => (req, res, next) => {
  const r = schema.safeParse(req.body);
  if (!r.success) return res.status(400).json({ type: "about:blank", title: "Invalid request", errors: r.error.issues.map(i => ({ path: i.path.join("."), message: i.message })) });
  req.valid = r.data; next();
};
app.post("/orders", express.json({ limit: "100kb" }), validate(CreateOrder), createOrder);
```
Alternatives: Valibot, TypeBox/Ajv (JSON Schema, also drives OpenAPI), Joi, `express-validator`. Fastify validates JSON Schema natively.

## 2. Python + pydantic (FastAPI does this automatically)
```python
class CreateOrder(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku: constr(pattern=r"^[A-Z0-9-]{3,32}$")
    qty: conint(ge=1, le=100)
```
Django: forms/DRF serializers. Rails: `params.require(:order).permit(:sku, :qty, :note)` plus model validations.

## 3. Rules
- **Allowlist** shapes, types, lengths, ranges, enums. Do not try to blocklist "bad characters".
- Reject unknown fields (prevents mass assignment of `role`, `isAdmin`).
- Bound everything: body size limits, array lengths, string lengths, nesting depth - unbounded input is a DoS vector.
- Normalise before validating (Unicode NFC, trim) if comparisons matter.
- Validation does not replace output encoding or parameterised queries - it is a separate layer.
- Validate responses from third-party APIs too; they change and get compromised.
- Client-side validation is UX only.

## Verify
Contract tests sending wrong types, extra fields, oversized strings and arrays get 400 with field-level messages; fuzz with Schemathesis against the OpenAPI spec.
