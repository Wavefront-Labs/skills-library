---
id: computing-software.software-engineering.typescript.runtime-validation-with-zod
name: runtime-validation-with-zod
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-quality, zod, schema-validation, runtime-validation, type-inference, parsing]
level: practitioner
status: verified
description: "Validate untrusted data at TypeScript boundaries with Zod: schemas as the source of types, parse vs safeParse, coercion, transforms, error formatting and env/config parsing."
sources:
  - https://zod.dev/
  - https://zod.dev/api
  - https://zod.dev/error-formatting
  - https://standardschema.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime validation at boundaries with Zod

**Goal:** data entering the program (HTTP bodies, query strings, env vars, JSON files, third-party APIs) is checked at runtime once, producing typed values for the rest of the code.

## 1. Schema as the single source of truth
```ts
import { z } from "zod";
export const CreateOrder = z.object({
  customerId: z.string().uuid(),
  lines: z.array(z.object({
    sku: z.string().min(1),
    qty: z.number().int().positive(),
  })).min(1),
  note: z.string().max(500).optional(),
  currency: z.enum(["EUR", "USD"]).default("EUR"),
});
export type CreateOrder = z.infer<typeof CreateOrder>;            // output type (after defaults)
export type CreateOrderInput = z.input<typeof CreateOrder>;
```
Do not also hand-write an interface for the same shape. (Every snippet below ran on Zod 4.6.7 and type-checked with `tsc --strict`.)

## 2. Parse at the edge
```ts
app.post("/orders", (req, res) => {
  const r = CreateOrder.safeParse(req.body);
  if (!r.success) return res.status(400).json({ errors: z.flattenError(r.error).fieldErrors });   // Zod 4
  const order = await createOrder(r.data);   // fully typed, unknown keys stripped
});
```
- `parse` throws `ZodError`; `safeParse` returns a result (prefer it in request handlers).
- Objects **strip unknown keys** by default; `z.strictObject` rejects them, `z.looseObject` keeps them.
- Async refinements require `parseAsync`/`safeParseAsync`.

## 3. Coercion and transforms
```ts
const Query = z.object({
  page: z.coerce.number().int().min(1).default(1),       // "2" -> 2
  since: z.coerce.date().optional(),
  tags: z.string().transform(s => s.split(",")).optional(),
});
const Env = z.object({
  DATABASE_URL: z.url(),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(["development", "test", "production"]),
});
export const env = Env.parse(process.env);              // fail fast at startup
```
Beware `z.coerce.boolean()`: any non-empty string, including `"false"`, becomes `true`; use `z.stringbool()` (Zod 4) or an enum.

## 4. Composition
`.extend()`, `.pick()`, `.omit()`, `.partial()` for PATCH bodies, `z.discriminatedUnion("type", [...])` for tagged payloads, `.refine()`/`.superRefine()` for cross-field rules (`end > start`), `.brand<"UserId">()` for nominal types.

## 5. Ecosystem
tRPC, React Hook Form (`zodResolver`), Fastify/Hono validators, and OpenAPI generators (`zod-openapi`) consume Zod schemas. The Standard Schema interface lets libraries accept Zod, Valibot or ArkType interchangeably.

## Gotchas
- Validating outgoing data or internal calls everywhere wastes CPU; validate at trust boundaries.
- Zod 3 vs 4 API differences (`z.string().email()` vs `z.email()`, error customisation, `.flatten()` vs `z.flattenError()`; both flatten forms still existed on 4.6.7); check which major you run.
- Large schemas slow TypeScript; avoid deeply recursive inferred types in hot editor paths, or annotate.
- `z.any()`/`z.unknown()` at the leaves silently re-opens the hole you closed.

## Verify
- Tests post malformed payloads (missing fields, wrong types, extra keys) and expect 400 with field-level messages; valid payloads reach the handler with defaults applied.
