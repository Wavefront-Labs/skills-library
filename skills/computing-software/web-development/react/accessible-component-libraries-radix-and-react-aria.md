---
id: computing-software.web-development.react.accessible-component-libraries-radix-and-react-aria
name: accessible-component-libraries-radix-and-react-aria
category: computing-software
field: web-development
product: react
tags: [radix-ui, react-aria, headless-components, accessible-components, react]
level: practitioner
status: docs-checked
description: "Accessible headless React libraries: Radix Primitives and React Aria Components, styling via data attributes, asChild composition, and testing."
sources:
  - https://www.radix-ui.com/primitives/docs/overview/getting-started
  - https://www.radix-ui.com/primitives/docs/guides/composition
  - https://www.radix-ui.com/primitives/docs/guides/styling
  - https://github.com/adobe/react-spectrum/blob/main/packages/dev/s2-docs/pages/react-aria/ComboBox.mdx
  - https://github.com/adobe/react-spectrum/blob/main/packages/dev/s2-docs/pages/react-aria/styling.mdx
  - https://github.com/adobe/react-spectrum/tree/main/packages/tailwindcss-react-aria-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessible component libraries: Radix and React Aria

Building comboboxes, menus, dialogs and date pickers accessibly from scratch takes weeks per widget. Headless libraries give you correct keyboard, focus and ARIA behaviour; you supply the styles.

## 1. Radix Primitives
```jsx
import * as Dialog from "@radix-ui/react-dialog";
<Dialog.Root>
  <Dialog.Trigger asChild><Button>Edit profile</Button></Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/40 data-[state=open]:animate-fade-in" />
    <Dialog.Content className="...">
      <Dialog.Title>Edit profile</Dialog.Title>
      <Dialog.Description>Changes are saved when you click Save.</Dialog.Description>
      <Dialog.Close asChild><button aria-label="Close">×</button></Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```
- Style with `data-state="open|closed"`, `data-side`, `data-highlighted`, `data-disabled`.
- `asChild` merges behaviour onto your own component (it must forward ref and spread props).
- `Dialog.Title` and `Dialog.Description` drive the screen-reader announcements: keep a Title (visually hide it if needed). The current Radix source warns in development only when a dialog has more than one title.
- The getting-started guide installs the unified package (`npm install radix-ui@latest`, then `import { Dialog } from "radix-ui"`); the example above uses the per-primitive `@radix-ui/react-dialog` package.

## 2. React Aria Components (Adobe)
```jsx
import { ComboBox, Label, Input, Button, Popover, ListBox, ListBoxItem } from "react-aria-components";
<ComboBox>
  <Label>Country</Label>
  <div><Input /><Button>▼</Button></div>
  <Popover><ListBox>{countries.map(c => <ListBoxItem key={c.id} id={c.id}>{c.name}</ListBoxItem>)}</ListBox></Popover>
</ComboBox>
```
- Exports date and range pickers, tables, trees, drag and drop hooks and an `I18nProvider` for locale handling. Selection props are on the ComboBox page for your installed version; an item's `id` is the value it reports.
- Style via render props or `data-*` attributes (`data-focus-visible`, `data-selected`); the `tailwindcss-react-aria-components` plugin maps those attributes to Tailwind variants (version 2.x for Tailwind v4, 1.x for v3).
- Hooks layer (`react-aria`) for fully custom markup.

## 3. Choosing
| Need | Pick |
|---|---|
| Dialogs, menus, popovers and other common app widgets | Radix |
| Date and range pickers, tables, trees, drag and drop, locale handling | React Aria |
| A component set for React or Vue | Headless UI |
| Framework-agnostic logic (React, Solid, Vue, Svelte) built on Zag.js state machines | Ark UI |

## 4. Don't undo the accessibility
- Keep focus-visible styles; don't remove portals without handling stacking and focus.
- Give icon-only triggers accessible names.
- Test anyway: keyboard pass, screen reader smoke test, axe in CI. Libraries can't fix wrong labels or missing headings.

## Verify
- [ ] Each widget passes APG keyboard expectations and has names, roles and states in the accessibility tree; styles use data attributes rather than reimplementing state.

## Checked

Checked 2026-10-25 against the radix-ui/website docs (updated 2026-10-07), the radix-ui/primitives Dialog source, the adobe/react-spectrum docs and exports (react-aria-components 1.22) and the Ark UI and Headless UI READMEs. Confirmed: `asChild` composition and the requirement to spread props and forward a ref; `data-state`, `data-side`, `data-highlighted` and `data-disabled` attributes; the unified `radix-ui` install; the Dialog dev warning is for multiple titles, not a missing title; React Aria Components exports ComboBox, Popover, ListBox, Label, Input, Button, I18nProvider, DateRangePicker, Table and Tree; styling through render props and `data-*` attributes; the Tailwind plugin and its version split; Ark UI is built on Zag.js for React, Solid, Vue and Svelte; Headless UI ships React and Vue packages. Removed unconfirmed claims about relative screen-reader coverage, shadcn/ui and the Headless UI "smaller set".

Method: documentation only; no commands were run.
