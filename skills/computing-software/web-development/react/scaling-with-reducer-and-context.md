---
id: computing-software.web-development.react.scaling-with-reducer-and-context
name: scaling-with-reducer-and-context
category: computing-software
field: web-development
product: react
tags: [react, reducer-context, usereducer, usecontext, context-provider, state-management, prop-drilling, web-development]
level: practitioner
status: verified
description: "Scaling React state with useReducer plus context: action design, separate state and dispatch contexts, custom provider hooks and avoiding re-render storms."
sources:
  - https://react.dev/learn/scaling-up-with-reducer-and-context
  - https://react.dev/learn/extracting-state-logic-into-a-reducer
  - https://react.dev/reference/react/useContext#optimizing-re-renders-when-passing-objects-and-functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling up with reducer + context

**Goal:** share complex state across a subtree without prop drilling or a state library.

## 1. Reducer: describe what happened
```jsx
function tasksReducer(tasks, action) {
  switch (action.type) {
    case "added":   return [...tasks, { id: action.id, text: action.text, done: false }];
    case "changed": return tasks.map(t => t.id === action.task.id ? action.task : t);
    case "deleted": return tasks.filter(t => t.id !== action.id);
    default: throw new Error(`Unknown action: ${action.type}`);
  }
}
```
Actions are events (`"added"`), not setters (`"setTasks"`). Reducers are pure: no fetch, no `Date.now()`/random ids (generate in the handler, pass in the action).

## 2. Two contexts
```jsx
const TasksContext = createContext(null);
const TasksDispatchContext = createContext(null);

export function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  return (
    <TasksContext value={tasks}>
      <TasksDispatchContext value={dispatch}>{children}</TasksDispatchContext>
    </TasksContext>
  );
}
export const useTasks = () => useContext(TasksContext);
export const useTasksDispatch = () => useContext(TasksDispatchContext);
```
`dispatch` is stable (checked: same function identity across renders), so components that only dispatch never re-render on state changes. (`<Ctx value>` works as a provider in React 19, checked; use `<Ctx.Provider value>` before 19.)

## 3. Guard the hook
```jsx
export function useTasks() {
  const v = useContext(TasksContext);
  if (v === null) throw new Error("useTasks must be used inside <TasksProvider>");
  return v;
}
```

## 4. Re-render cost
Every consumer re-renders when the context value changes. Mitigate:
- Split contexts by update frequency (auth vs. live cursor position).
- Memoise object values: `useMemo(() => ({ user, logout }), [user])`.
- For high-frequency or large global state, use an external store (Zustand, Redux Toolkit, `useSyncExternalStore`) with selectors.

## 5. When not to
Server data → TanStack Query / loaders. Two components → lift state. Theme/locale/auth → plain context is ideal.

## Verify
- [ ] Reducer has a unit test per action and throws on unknown types.
- [ ] Profiler: dispatch-only components don't re-render on state change.
- [ ] Hooks throw a clear error outside the provider.
