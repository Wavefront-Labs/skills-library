---
id: computing-software.web-development.frontend-development.history-pushstate-and-popstate
name: history-pushstate-and-popstate
category: computing-software
field: web-development
product: frontend-development
tags: [history-api, pushstate, popstate, spa-routing, history, javascript]
level: practitioner
status: docs-checked
description: "Building client-side routing on the History API: pushState vs replaceState, handling popstate, state objects, link interception, and server fallback configuration."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/History/pushState
  - https://developer.mozilla.org/en-US/docs/Web/API/History_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/popstate_event
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pushState, replaceState and popstate

## 1. Minimal router
```js
function render(url) { /* match url.pathname -> view */ }
document.addEventListener("click", e => {
  const a = e.target.closest("a[href]");
  if (!a || a.target || a.hasAttribute("download") || e.button !== 0 ||
      e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.origin !== location.origin) return;  // let the browser handle it
  e.preventDefault();
  history.pushState({ scrollY: 0 }, "", a.href);   // second argument is unused
  render(new URL(a.href));
});
addEventListener("popstate", e => render(new URL(location.href)));   // back/forward
render(new URL(location.href));
```

## 2. Semantics
- `pushState(state, "", url)` adds an entry; `replaceState` overwrites the current one (use for filter changes you don't want in Back history, redirects, normalising URLs).
- Neither fires `popstate` and neither loads anything - you render.
- `popstate` fires when the user navigates session history (back, forward, `history.back()`), not on push/replace.
- `state` must be serializable, and some browsers persist it to disk with a size limit and throw if exceeded; store IDs/scroll, not big data.
- The new URL must be same-origin or `SecurityError` is thrown. The second argument is unused: pass an empty string and set `document.title` yourself.

## 3. Server side
Every client route must return the app shell on a hard load, or refresh gives 404: configure your host's rewrite or fallback rule for the shell page (see the hosting skill for your platform). Still return a real 404 status for unknown routes where possible.

## 4. Pitfalls
- Calling `pushState` per keystroke floods the history. Use `replaceState` for live inputs, push on commit.
- After navigation you must update title, move focus and handle scroll (see scroll restoration).
- Rendering race: if a slow route resolves after the user navigated again, discard it (navigation id or AbortController).
- Modifier-click and middle-click must keep opening new tabs - hence the checks above.

## Verify
Back/forward through several routes restores the right view; hard refresh on a deep link works; Cmd/Ctrl+click opens a new tab.

## Checked

2026-10-26. MDN pushState (state must be serializable and may hit a browser size limit; same-origin URL, SecurityError; unused second parameter) and the popstate event page (fired on session-history navigation, not by pushState or replaceState). Removed the unconfirmed nginx, Netlify, Safari rate-limit and hash-change statements.

Method: documentation only; no commands were run.
