---
id: computing-software.software-engineering.mobile-development.react-native-testing-library-and-jest
name: react-native-testing-library-and-jest
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-testing-library, testing-library, component-testing, jest, screen-queries, user-event, fire-event, waitfor, tobeonthescreen, renderhook, unit-testing, jsdom, mobile-testing, test-driven]
level: practitioner
status: draft
description: "Test React Native components with React Native Testing Library and Jest: render/screen, the query families, userEvent versus fireEvent, waitFor, the built-in matchers, and what not to test."
sources: ["https://oss.callstack.com/react-native-testing-library/", "https://oss.callstack.com/react-native-testing-library/docs/api", "https://oss.callstack.com/react-native-testing-library/docs/api/jest-matchers", "https://callstack.github.io/react-native-testing-library/docs/getting-started"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# React Native Testing Library and Jest

**Goal:** test what a component does for its user - rendered output, state, and interaction - not
its internals, using `@testing-library/react-native`.

The guiding principle is the testing-library one: *the more your tests resemble the way your
software is used, the more confidence they can give you.* In practice that means finding elements
the way an assistive technology user would (role, accessible name, text) and driving them with
user-like events, so a refactor of internals does not break a single test.

```tsx
import { render, screen, userEvent } from '@testing-library/react-native';

test('shows the total after adding an item', async () => {
  const user = userEvent.setup();
  render(<Cart items={[{ id: '1', name: 'Coffee', price: 450 }]} />);

  await user.press(screen.getByRole('button', { name: 'Add Coffee' }));

  expect(screen.getByText('Total: $4.50')).toBeOnTheScreen();
});
```

## render and screen
`render(ui)` mounts a component and returns helpers; prefer the global `screen` object for queries
so tests do not destructure a fresh handle per render. `screen` also exposes `rerender`, `unmount`,
`debug` (pretty-print the current tree), `toJSON`, and `root`. `renderHook` tests a hook in
isolation. `cleanup` between tests is automatic via the Jest setup.

## The query families
| Variant | No match | Many matches | Use for |
|---|---|---|---|
| `getBy*` | throws | throws | the assertion succeeded-path, when exactly one element must exist |
| `queryBy*` | returns `null` | throws | asserting absence: `expect(queryBy...).toBeNull()` |
| `findBy*` | waits (returns a Promise) | throws | elements that appear after an async update |
| `*AllBy*` | returns `[]` | returns array | lists and multi-match cases |

Matchers: `byRole` (preferred - role plus `name` option), `byText`, `byTestId`, `byPlaceholderText`,
`byDisplayValue`, `byLabelText`. Reach a subtree with `within(element).getBy...`.

`getByTestId` is the fallback, not the default: it tests nothing a user can perceive and survives
any refactor, which is the opposite of what you want. Prefer role and accessible name.

## userEvent versus fireEvent
`userEvent` simulates interactions **realistically** - `press`, `type`, with proper event
sequences; `fireEvent` fires any single component event in a simplified way. Reach for
`userEvent.setup()` and the interaction helpers first, and drop to `fireEvent` only for events
with no user-event equivalent (a custom callback prop on a view). Realistic event ordering is the
reason: components with focus, keyboard or state transitions behave under `userEvent` the way they
behave for a person, which is the whole point.

## Async
- `findBy*` for a single element that appears later.
- `waitFor(() => ...)` for any condition; `waitForElementToBeRemoved` for the opposite.
- Everything async is wrapped in `act()` internally - if a test warns about updates outside `act`,
  the component is updating from an unawaited promise or timer the test did not control.

## Built-in Jest matchers
Available with no extra setup once the library is imported:

| Matcher | Asserts |
|---|---|
| `toBeOnTheScreen()` | the element is attached to the rendered tree (fails if it unmounted mid-test) - the replacement for web's `toBeInTheDocument` |
| `toBeVisible()` | visible: not `display: none`, not `opacity: 0`, not hidden from accessibility (ancestors count) |
| `toBeEnabled()` / `toBeDisabled()` | from `accessibilityState.disabled` / `aria-disabled`; also `TextInput` `editable={false}`, `Text`/`Switch` `disabled` |
| `toBeChecked()` / `toBePartiallyChecked()` | `Switch` host elements or checkbox/radio/switch roles |
| `toBeSelected()`, `toBeExpanded()` / `toBeCollapsed()`, `toBeBusy()` | the corresponding accessibility state |
| `toHaveTextContent(text)` | text content, string or RegExp, with `exact`/`normalizer` options |
| `toHaveDisplayValue(value)` | `TextInput` display value |
| `toHaveAccessibleName(name)` | accessible name; with no argument, that one exists at all |
| `toHaveAccessibilityValue({ min, max, now, text })` | only the keys you pass are checked |
| `toHaveStyle(style)`, `toHaveProp(name, value?)` | style/props - **`toHaveProp` is a documented last resort** |
| `toContainElement(el)`, `toBeEmptyElement()` | tree containment / emptiness |

Two subtleties worth knowing: opposite matchers exist deliberately (`toBeDisabled` rather than
`not.toBeEnabled`) to avoid double negation; and **disabled state is not inherited from ancestors**
in React Native, so assert on the element that owns it - the button, not the text inside it.

## What not to test
- **Implementation details**: internal state names, private method calls, the `container` for DOM
  inspection, or `toHaveProp` when a user-observable matcher exists. The docs position prop
  assertions as the escape hatch, not the tool of first resort.
- **The library itself**: do not assert that a `Text` renders text by snapshotting the whole tree -
  `toHaveTextContent` says it in one line and survives refactors.
- **Native modules** without mocks: mock the module boundary (`jest.mock(...)`) and assert on the
  behaviour it drives, not on the module having been called.

`configure` adjusts defaults (e.g. async timeouts) and `resetToDefaults` restores them;
`isHiddenFromAccessibility` is the query-level check for accessibility-hidden elements.

## Failure modes
- **"Found multiple elements"** - a `getBy*` matched several nodes. Make the matcher more specific
  (`byRole` with `name`) or use the `*AllBy*` variant deliberately.
- **"Not wrapped in act(...)"** - an unawaited promise or timer updates the tree after the test
  finished awaiting. `await` everything; fake timers for debounce/setTimeout.
- **Test passes but the app does not** - events fired with `fireEvent` that a real user cannot
  produce, or assertions on props instead of output. Re-express the test through `userEvent` and
  role/text queries.
- **Element exists but `toBeVisible` fails** - an ancestor has `opacity: 0` or is
  accessibility-hidden. The matcher is tree-aware on purpose.
- **Disabled assertion on a child passes when the control is disabled** - disabled is not
  inherited; assert on the control.

## Verify
- [ ] The Jest preset is configured (jest-expo, or `@testing-library/react-native`'s preset for
      bare RN) and `npx jest` runs green.
- [ ] The majority of queries are `byRole`/`byText`; `getByTestId` appears only where nothing
      user-perceivable distinguishes the element.
- [ ] Every async assertion uses `findBy*` or `waitFor`, with no sleeps.
- [ ] No test asserts on `container` or uses `toHaveProp` as its first tool.
- [ ] A deliberately broken component fails at least one test for the right reason.

*API names and the full matcher list checked against the v14 docs on 2026-10-31; not executed here,
so `status: draft`.*
