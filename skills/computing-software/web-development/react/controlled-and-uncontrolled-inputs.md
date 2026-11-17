---
id: computing-software.web-development.react.controlled-and-uncontrolled-inputs
name: controlled-and-uncontrolled-inputs
category: computing-software
field: web-development
product: react
tags: [react, controlled-components, uncontrolled-components, forms, defaultvalue, formdata, inputs, web-development]
level: practitioner
status: verified
description: "Choosing controlled or uncontrolled inputs in React: value/onChange wiring, defaultValue with FormData, switching warnings, selects, checkboxes and file inputs."
sources:
  - https://react.dev/reference/react-dom/components/input
  - https://react.dev/learn/sharing-state-between-components#controlled-and-uncontrolled-components
  - https://developer.mozilla.org/en-US/docs/Web/API/FormData
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlled vs uncontrolled inputs

**Goal:** pick the input model per field and wire it without warnings or lost keystrokes.

## 1. Controlled: React owns the value
```jsx
const [email, setEmail] = useState("");
<input type="email" value={email} onChange={e => setEmail(e.target.value)} />
```
Use when you need live validation, formatting, conditional UI, or to set the value programmatically. `value` without `onChange` renders read-only (and warns) - add `readOnly` if intended.

## 2. Uncontrolled: the DOM owns the value
```jsx
function Signup() {
  function handleSubmit(e) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget));
    save(data);
  }
  return <form onSubmit={handleSubmit}><input name="email" defaultValue="" /></form>;
}
```
Fewer re-renders, works with React 19 form actions (`<form action={fn}>` receives `FormData`). Read imperatively via `ref` when needed. `<input type="file">` is always uncontrolled (React docs: its value can only be set by the user).

## 3. "Changing an uncontrolled input to be controlled"
Caused by `value={undefined}` then a string. Initialise with `""`, not `undefined`/`null`: `value={user.name ?? ""}`.

## 4. Other control types
- Checkbox: `checked` + `onChange={e => setOn(e.target.checked)}` (not `value`). Uncontrolled: `defaultChecked`.
- Select: `<select value={v} onChange>`; multiple: `value={["a","b"]}` and read `Array.from(e.target.selectedOptions, o => o.value)`.
- Textarea: `value`, not children.
- Number inputs: keep the state as a string while typing and parse on submit, so half-typed values are not rewritten under the user.

## 5. Cursor jumps
Rewriting the value in `onChange` (uppercasing, formatting) sets `input.value` programmatically, which moves the caret to the end (reproduced in jsdom: typing at position 2 of `abc` and uppercasing left the caret at the end). Restore the selection yourself (a layout effect with `setSelectionRange`) or format on blur.

## 6. Resetting
Uncontrolled: `form.reset()` or remount with a new `key`. Controlled: set state back to initial values. React 19 resets uncontrolled fields automatically after a successful form action.

## 7. Big forms
Many controlled fields re-render the whole form per keystroke. Use uncontrolled + a library (React Hook Form) or split field components.

## Verify
- [ ] No console warnings about controlled/uncontrolled switching.
- [ ] Typing fast in formatted fields keeps the caret in place.
- [ ] Form works with JS disabled where using native form submission/actions.
