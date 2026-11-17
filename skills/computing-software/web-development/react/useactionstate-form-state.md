---
id: computing-software.web-development.react.useactionstate-form-state
name: useactionstate-form-state
category: computing-software
field: web-development
product: react
tags: [react, useactionstate, form-actions, react-19, server-actions, progressive-enhancement, web-development]
level: practitioner
status: verified
description: "Managing form submission state in React 19 with useActionState: action signature, returned errors, pending flag, permalink for progressive enhancement."
sources:
  - https://react.dev/reference/react/useActionState
  - https://react.dev/reference/react-dom/components/form
  - https://nextjs.org/docs/app/guides/forms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useActionState for form state

**Goal:** submit forms through actions with result/error state and pending flag, no hand-rolled `isLoading` booleans.

## 1. Signature
```jsx
const [state, formAction, isPending] = useActionState(action, initialState, permalink?);
// action(previousState, formData) => newState  (may be async)
```
(Named `useFormState` in earlier canary builds; the React 19 migration recipe includes a `replace-use-form-state` codemod. `react-dom` 19.3.1 still exports `useFormState`.)

## 2. Example
```jsx
async function subscribe(prev, formData) {
  const email = formData.get("email");
  if (!email?.includes("@")) return { error: "Enter a valid email", email };
  const res = await fetch("/api/subscribe", { method: "POST", body: formData });
  return res.ok ? { ok: true } : { error: "Try again later", email };
}

function Subscribe() {
  const [state, formAction, isPending] = useActionState(subscribe, { error: null });
  return (
    <form action={formAction}>
      <input name="email" type="email" defaultValue={state.email} aria-describedby="err" />
      <button disabled={isPending}>{isPending ? "Subscribing..." : "Subscribe"}</button>
      {state.error && <p id="err" role="alert">{state.error}</p>}
    </form>
  );
}
```

## 3. Behaviour to know
- Submissions are queued: each action call receives the state returned by the previous one (checked: calls `a` then `b` saw `""` then `"a"`).
- React resets uncontrolled form fields after a successful action - return submitted values and use `defaultValue` so a failed validation doesn't wipe the input.
- Throwing an error goes to the nearest error boundary; **return** expected validation errors instead.
- Calling `formAction` outside a form or Action prop needs `startTransition(() => formAction(fd))`; otherwise React logs "An async function with useActionState was called outside of a transition" in development (checked).

## 4. With server actions (Next.js / RSC)
```tsx
// actions.ts
"use server";
export async function createPost(prev: State, fd: FormData): Promise<State> {
  const parsed = schema.safeParse(Object.fromEntries(fd));
  if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
  await db.post.create({ data: parsed.data });
  redirect("/posts");
}
```
The form works before hydration (progressive enhancement). `permalink` sets the URL the form navigates to if submitted before JS loads, for pages whose action renders elsewhere.

## 5. Validate on the server regardless
Client checks are UX; the action must re-validate and authorise (server actions are public POST endpoints).

## Verify
- [ ] Failed validation keeps typed values and shows an accessible error.
- [ ] Double-click submit doesn't double-submit (button disabled while pending).
- [ ] With JS disabled (server actions), the form still submits and shows errors.
