---
id: computing-software.web-development.react.useformstatus-pending-ui
name: useformstatus-pending-ui
category: computing-software
field: web-development
product: react
tags: [react, useformstatus, form-actions, pending-state, submit-button, react-19, web-development]
level: practitioner
status: verified
description: "Using useFormStatus in React 19 to build reusable submit buttons and pending UI that read the parent form's state, with its placement rules."
sources:
  - https://react.dev/reference/react-dom/hooks/useFormStatus
  - https://react.dev/reference/react-dom/components/form
  - https://nextjs.org/docs/app/guides/forms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useFormStatus for pending UI

**Goal:** a design-system `<SubmitButton>` that knows when its form is submitting, with no props threaded through.

## 1. The hook
```jsx
import { useFormStatus } from "react-dom";      // react-dom, not react

function SubmitButton({ children }) {
  const { pending, data, method, action } = useFormStatus();
  return (
    <button type="submit" disabled={pending} aria-disabled={pending}>
      {pending ? "Saving..." : children}
    </button>
  );
}
```

## 2. Placement rule
It reports the status of the **parent `<form>`** whose `action` is a function. It must be called in a component rendered inside that form - calling it in the component that renders the `<form>` always returns `pending: false` (checked: parent `false`; child `false`, `true`, `false` across a submit; the object has `pending`, `data`, `method`, `action`).
```jsx
<form action={saveAction}>
  <input name="title" />
  <SubmitButton>Save</SubmitButton>     // works
</form>
```

## 3. Using `data`
`data` is the `FormData` being submitted - show what's in flight:
```jsx
const { pending, data } = useFormStatus();
return pending ? <p>Adding {data?.get("name")}...</p> : null;
```

## 4. useFormStatus vs useActionState
- `useFormStatus`: read-only pending info for any descendant; reusable components.
- `useActionState`: owns the result/errors and also returns `isPending`, but only in the component that defines the action.
Use both: action state in the form component, status in the button.

## 5. Accessibility
- Keep the button focusable while pending (`aria-disabled` + ignore clicks) if you want screen readers to announce the label change; `disabled` removes it from focus. (jsdom check: a `disabled` button cannot take focus, an `aria-disabled` one can.)
- Announce completion/errors with a live region (`role="status"` / `role="alert"`).

## 6. Not for
Forms submitted with `onSubmit` + fetch (no action) - there's no status to read; use local state or the mutation library's `isPending`.

## Verify
- [ ] Button shows pending text and blocks double submission on a slow network.
- [ ] Same `SubmitButton` works in multiple forms without props.
- [ ] Screen reader announces the result after submission.
