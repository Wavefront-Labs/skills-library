---
id: computing-software.web-development.react.form-action-prop-and-requestformreset
name: form-action-prop-and-requestformreset
category: computing-software
field: web-development
product: react
tags: [form-action-prop, react-19-forms, requestformreset, server-functions, progressive-enhancement]
level: practitioner
status: verified
description: "React 19 form actions: functions as form action, automatic reset and requestFormReset, formAction on buttons, pending state, and progressive enhancement."
sources:
  - https://react.dev/reference/react-dom/components/form
  - https://react.dev/reference/react-dom/requestFormReset
  - https://react.dev/reference/react-dom/hooks/useFormStatus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# form action prop and requestFormReset

## 1. Functions as actions
```jsx
function NewsletterForm() {
  async function subscribe(formData) {
    await api.subscribe(formData.get("email"));
  }
  return (
    <form action={subscribe}>
      <input name="email" type="email" required autoComplete="email" />
      <SubmitButton />
    </form>);
}
```
- React calls the function with `FormData` inside a transition; no `e.preventDefault()` or `onSubmit` needed.
- After a successful action, **uncontrolled fields are reset automatically** (the React 19 post says so; checked, and the reset happens even when the action returns validation errors). Controlled inputs keep their state (checked).
- Errors thrown propagate to the nearest error boundary - catch and return state with `useActionState` for user-facing validation.

## 2. Per-button actions
```jsx
<form action={save}>
  <input name="title" />
  <button type="submit">Save</button>
  <button type="submit" formAction={saveDraft}>Save draft</button>
</form>
```

## 3. Pending UI
`useFormStatus()` inside a child of the form returns `{ pending, data, method, action }`. Disable the submit button and show progress while `pending`.

## 4. Resetting manually
```jsx
import { requestFormReset } from "react-dom";
function onCancel(e) { startTransition(() => requestFormReset(e.currentTarget.form)); }
```
`requestFormReset(form)` is the React DOM API for resetting a form manually (React 19 post); called inside `startTransition` it restored the field to its `defaultValue` (checked).

## 5. Server functions and progressive enhancement
Passing a `"use server"` function (Next.js, other RSC frameworks) makes the form work **before JavaScript loads**: it posts to the server endpoint and the page re-renders. Combine with `useActionState(action, initial, permalink)` to return validation errors and keep the form usable without JS.

## 6. Pitfalls
- Values you need to keep after success (failed validation) must be returned from the action and rendered as `defaultValue`, because the form resets.
- File inputs: `formData.get("file")` gives a `File`; server functions have body size limits (Next.js: `experimental.serverActions.bodySizeLimit`, default 1MB, in `next.config.js`).
- Pick one submission path per form: `action` or `onSubmit` with `preventDefault`.

## Verify
- [ ] Form submits and resets after success; validation errors preserve user input; buttons disabled while pending; works with JS disabled where server functions are used.
