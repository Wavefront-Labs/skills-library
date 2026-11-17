---
id: computing-software.qa-testing-engineering.jest-pytest.react-testing-library-and-user-event
name: react-testing-library-and-user-event
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [react-testing-library, user-event, testing-library-queries, jest, component-testing]
level: practitioner
status: verified
description: "Test React components with Testing Library: query priority (getByRole first), find vs query variants, user-event setup, async waits, and jest-dom matchers."
sources:
  - https://testing-library.com/docs/queries/about#priority
  - https://testing-library.com/docs/user-event/intro
  - https://github.com/testing-library/jest-dom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Testing Library queries and user-event

**Goal:** tests that interact like users and survive refactors of component internals.

Setup: `@testing-library/react` v16 needs `@testing-library/dom` and `react`/`react-dom` installed as peer dependencies; in Jest also `jest-environment-jsdom` and a Babel or ts-jest transform for JSX (ran with RTL 16.3, user-event 14.6, jest-dom 6.9, React 19, Jest 30).

## Example
```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

test('shows validation error and submits valid email', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<SignupForm onSubmit={onSubmit} />);

  await user.click(screen.getByRole('button', { name: /sign up/i }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Email is required');

  await user.type(screen.getByLabelText(/email/i), 'ada@example.test');
  await user.click(screen.getByRole('button', { name: /sign up/i }));
  expect(onSubmit).toHaveBeenCalledWith({ email: 'ada@example.test' });
});
```

## Query priority
1. `getByRole` (with `name`), `getByLabelText`, `getByPlaceholderText`, `getByText`, `getByDisplayValue`.
2. `getByAltText`, `getByTitle`.
3. `getByTestId` last resort.
If `getByRole` cannot find it, the element may be inaccessible: a signal to fix the component.

## Variants
| | 0 matches | >1 matches | async |
|---|---|---|---|
| `getBy` | throw | throw | no |
| `queryBy` | null | throw | no |
| `findBy` | reject | reject | yes (waits, default 1000 ms; ran: rejected after 1001 ms) |
| `*AllBy` | | returns array | |
Use `queryBy` only to assert absence: `expect(screen.queryByRole('alert')).not.toBeInTheDocument()`.

## Async
- `findBy*` for elements that appear later.
- `waitFor(() => expect(...))` for non-element conditions; no side effects inside.
- `waitForElementToBeRemoved(() => screen.queryByText('Loading...'))`.

## user-event vs fireEvent
user-event v14 simulates full interactions (focus, keydown/press/up, input, click with pointer events) and is async; call `userEvent.setup()` per test. With fake timers pass `userEvent.setup({ advanceTimers: jest.advanceTimersByTime })` (ran). `fireEvent` dispatches a single DOM event; use only when user-event cannot express it.

## Gotchas
- "not wrapped in act(...)" warnings mean a state update happened after the test moved on; await the resulting UI with findBy.
- `screen.debug()` / `logRoles(container)` (exported from `@testing-library/react`) to see what queries can find.
- Mock network with MSW rather than mocking fetch per test.

## Verify
Tests use role/label queries, no implementation details (state, class names), and pass after refactoring component internals.
