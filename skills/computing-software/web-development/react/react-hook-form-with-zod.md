---
id: computing-software.web-development.react.react-hook-form-with-zod
name: react-hook-form-with-zod
category: computing-software
field: web-development
product: react
tags: [react, react-hook-form, zod, form-validation, zodresolver, usefieldarray, controller, web-development, zod-validation]
level: practitioner
status: docs-checked
description: "Building forms with React Hook Form and zod: typed schemas, zodResolver, register vs Controller, field arrays, server errors and accessible messages."
sources:
  - https://react-hook-form.com/docs/useform
  - https://react-hook-form.com/docs/usefieldarray
  - https://react-hook-form.com/docs/usewatch
  - https://github.com/react-hook-form/resolvers
  - https://zod.dev/api
  - https://zod.dev/error-customization
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Forms with React Hook Form + zod

**Goal:** large, validated forms with minimal re-renders and one schema shared by client and server.

## 1. Schema and form
```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const Schema = z.object({
  email: z.email("Enter a valid email"),
  age: z.number().int().min(18, "Must be 18+"),
});
type Values = z.infer<typeof Schema>;

export function SignupForm() {
  const { register, handleSubmit, setError, formState: { errors, isSubmitting } } =
    useForm<Values>({ resolver: zodResolver(Schema), mode: "onBlur" });

  const onSubmit = async (v: Values) => {
    const res = await fetch("/api/signup", { method: "POST", body: JSON.stringify(v) });
    if (res.status === 409) setError("email", { message: "Email already registered" });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">Email</label>
      <input id="email" {...register("email")} aria-invalid={!!errors.email} aria-describedby="email-err" />
      {errors.email && <p id="email-err" role="alert">{errors.email.message}</p>}
      <input type="number" {...register("age", { valueAsNumber: true })} />
      <button disabled={isSubmitting}>Sign up</button>
    </form>
  );
}
```

## 2. register vs Controller
`register` wires native inputs uncontrolled (fast). Controlled UI-library components (MUI, react-select, date pickers) need `<Controller name="date" control={control} render={({ field }) => <DatePicker {...field} />} />`.

## 3. Dynamic lists
```tsx
const { fields, append, remove } = useFieldArray({ control, name: "items" });
{fields.map((f, i) => <input key={f.id} {...register(`items.${i}.name`)} />)}
```
Use `f.id` as the key, never the index (v7; the v8 beta renames it to `field.key`).

## 4. Gotchas
- `defaultValues` are cached; to load async data call `reset(data)` or use the `values` prop (which resets the form whenever the data changes).
- Number inputs give strings: use `valueAsNumber: true` with `z.number()`. A `z.coerce.number()` schema has input type `unknown` in zod 4.
- `watch()` at the top re-renders on every change; prefer `useWatch({ name })` in a child.
- Modes: `onSubmit` (default), `onBlur`, `onChange`, `onTouched`, `all`; `reValidateMode` (default `onChange`) applies after the first submit.

## 5. Server is the authority
Reuse `Schema.safeParse` in the API/server action; map server field errors back with `setError`. Client validation is UX only.

## Verify
- [ ] Errors are announced (role alert / aria-describedby) and focus moves to the first invalid field (`shouldFocusError` default true).
- [ ] React DevTools: typing in one field doesn't re-render the whole form.
- [ ] Server rejects invalid payloads sent directly with curl.

## Checked

Checked 2026-10-25 against the react-hook-form documentation repository (react-hook-form 7.91.0 stable, 8.0.0-beta.5 pre-release), @hookform/resolvers (6.0.0, 2026-10-19; its zod README) and the zod 4 docs (4.6.7). Confirmed: `mode` values and `onSubmit` default; `reValidateMode` values and `onChange` default; `shouldFocusError` default true; `defaultValues` are cached and `reset` or `values` update them; `useFieldArray` supplies `field.id` for the key (renamed `key` in v8); `useWatch` isolates re-renders; `valueAsNumber` on `register`; `Controller` for controlled external inputs; resolver README uses `valueAsNumber` with `z.number()`; top-level `z.email()` and a string error message as the last argument; coerced schemas have input type `unknown`. Changed the example to `z.email()`, `z.number()` with `valueAsNumber`, and removed the `z.coerce` guidance.

Method: documentation only; no commands were run.
