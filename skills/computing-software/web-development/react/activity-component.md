---
id: computing-software.web-development.react.activity-component
name: activity-component
category: computing-software
field: web-development
product: react
tags: [activity-component, offscreen-rendering, state-preservation, tabs, react]
level: advanced
status: docs-checked
description: "Using React's Activity component to hide UI while preserving state and DOM: visible vs hidden modes, effect cleanup when hidden, pre-rendering likely screens, and pitfalls."
sources:
  - https://react.dev/reference/react/Activity
  - https://react.dev/blog/2025/10/01/react-19-2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Activity: hidden-but-preserved UI

`<Activity>` (stable in React 19.2) lets you hide part of the tree without unmounting it. State and DOM are kept; effects are cleaned up while hidden and re-created when shown.

## 1. Basic use
```jsx
import { Activity } from "react";
<Activity mode={tab === "inbox" ? "visible" : "hidden"}><Inbox /></Activity>
<Activity mode={tab === "drafts" ? "visible" : "hidden"}><Drafts /></Activity>
```
Compared with `{tab === "inbox" && <Inbox />}`: switching back keeps component state and the DOM (for example an unsent textarea draft), so it is instant.

## 2. What "hidden" does
- Children are hidden with `display: none`.
- Effects are destroyed (their cleanup runs, so active subscriptions are released) and are set up again when the content becomes visible. Media elements are not stopped for you (see pitfalls).
- Hidden subtrees still re-render when props change, at a lower priority than visible content.
- Component state persists.

## 3. Pre-rendering
Render a likely-next screen in `hidden` mode so it can load data, CSS and images in the background before the user navigates. A hidden Activity renders its children at a lower priority than visible content and does not mount their Effects until it becomes visible.

## 4. Pitfalls
- Memory: every hidden subtree keeps its DOM and state, so use it for a small number of panels.
- Components whose Effects lack proper cleanup can misbehave: Effects are destroyed when hidden and set up again when shown.
- `<video>`/`<audio>` keep their DOM, so playback continues while hidden. Pause it in an Effect cleanup; the React docs use `useLayoutEffect` because the cleanup is tied to the UI being visually hidden.
- Hidden DOM stays in the document with `display: none`, so duplicate ids and global DOM queries still see it. A hidden Activity whose children render only text produces no DOM output.

## 5. Alternatives
- CSS `hidden`/`display: none` without Activity keeps effects running (timers, subscriptions) - usually undesirable.
- Lifting state up or into a store when you only need data preserved, not DOM.

## Verify
- [ ] Switching tabs preserves state; subscriptions stop when hidden (network/websocket panel); memory stable after many switches; audio stops when hidden.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), pages Activity and the React 19.2 post. Confirmed: Activity shipped in 19.2 with `visible` and `hidden` modes; hidden children get `display: none`, have Effects destroyed and still re-render at lower priority; DOM and state are preserved; initial hidden renders do not mount Effects; video keeps playing unless an Effect cleanup pauses it. Removed unconfirmed claims about focus loss, item-count limits and refs.

Method: documentation only; no commands were run.
