---
id: computing-software.web-development.storybook.args-use-args-hook
name: args-use-args-hook
category: computing-software
field: web-development
product: storybook
tags: [use-args, update-args, story-state, storybook-hooks, preview-api]
level: advanced
status: docs-checked
description: "Update args from inside a story with the useArgs hook so interactive components stay in sync with Controls."
sources:
  - https://storybook.js.org/docs/writing-stories/args
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Updating args from a story with useArgs

Goal: let a component change its own arg (toggle, input) and reflect it in Controls. The docs show this for React.

```tsx
import { useArgs } from 'storybook/preview-api';

export const Switch = meta.story({
  args: { checked: false },
  render: function Render(args) {
    const [{ checked }, updateArgs] = useArgs();
    return (
      <Toggle
        {...args}
        checked={checked}
        onChange={(e) => updateArgs({ checked: e.target.checked })}
      />
    );
  },
});
```

Rules:
- Import from `storybook/preview-api` in stories and decorators. Addons running in the manager use `useArgs` from `storybook/manager-api` instead.
- Do not mix React hooks with Storybook's hook API in the same render function. Use Storybook's equivalents (such as `useState`, `useEffect`, `useRef` from `storybook/preview-api`) instead of React's.

Verify: toggling the component updates the matching control in the panel.

## Checked
Date: 2026-11-04. Read the Args page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: `useArgs` usage inside `render: function Render(args)`, the mixing-hooks warning, manager-api note.
Fixed: the list of Storybook hook equivalents now matches the page. Removed the unconfirmed claim that hooks are exposed on the decorator context as `hooks` from this skill.
Method: documentation only; no commands were run.
